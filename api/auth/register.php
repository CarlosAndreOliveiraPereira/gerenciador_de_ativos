<?php
require_once '../config/database.php';

header('Content-Type: application/json');

// Função para enviar resposta JSON e sair
function send_json_response($success, $message, $statusCode = 200) {
    http_response_code($statusCode);
    echo json_encode(['success' => $success, 'message' => $message]);
    exit;
}

$data = json_decode(file_get_contents('php://input'), true);

// 1. Validação de Entrada
if (!$data || empty($data['name']) || empty($data['email']) || empty($data['password'])) {
    send_json_response(false, 'Todos os campos são obrigatórios.', 400);
}

$name = trim($data['name']);
$email = $data['email'];
$password = $data['password'];

if (strlen($name) < 2) {
    send_json_response(false, 'O nome deve ter pelo menos 2 caracteres.', 400);
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    send_json_response(false, 'Formato de e-mail inválido.', 400);
}

// Validação de domínio de e-mail
if (substr($email, -17) !== '@grupomysa.com.br') {
    send_json_response(false, 'O e-mail deve pertencer ao domínio @grupomysa.com.br.', 400);
}

if (strlen($password) < 8) {
    send_json_response(false, 'A senha deve ter pelo menos 8 caracteres.', 400);
}

// Função para obter o token de acesso da Microsoft (App-Only)
function get_microsoft_access_token() {
    $token_endpoint = 'https://login.microsoftonline.com/' . MICROSOFT_TENANT_ID . '/oauth2/v2.0/token';
    $token_params = [
        'client_id' => MICROSOFT_CLIENT_ID,
        'client_secret' => MICROSOFT_CLIENT_SECRET,
        'scope' => 'https://graph.microsoft.com/.default',
        'grant_type' => 'client_credentials',
    ];

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $token_endpoint);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($token_params));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);

    $token_data = json_decode($response, true);
    if (!isset($token_data['access_token'])) {
        error_log("Microsoft Graph API: Falha ao obter o token de acesso.");
        return null;
    }
    return $token_data['access_token'];
}

// 2. Validar existência do e-mail na Microsoft
$access_token = get_microsoft_access_token();
if (!$access_token) {
    send_json_response(false, 'Ocorreu um erro interno ao validar o e-mail. Por favor, contate o administrador.', 500);
}

$graph_endpoint = 'https://graph.microsoft.com/v1.0/users/' . urlencode($email);
$headers = ['Authorization: Bearer ' . $access_token];

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $graph_endpoint);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($http_code === 404) {
    send_json_response(false, 'O e-mail fornecido não foi encontrado no diretório da empresa.', 400);
} elseif ($http_code !== 200) {
    error_log("Microsoft Graph API: Erro HTTP " . $http_code . " ao verificar o usuário " . $email);
    send_json_response(false, 'Ocorreu um erro ao verificar o e-mail com a Microsoft. Por favor, contate o administrador.', 500);
}

// 3. Lógica de Registro com Tratamento de Erros
try {
    $password_hash = password_hash($password, PASSWORD_DEFAULT);

    $stmt = $pdo->prepare("INSERT INTO users (name, email, password_hash) VALUES (:name, :email, :password_hash)");
    $stmt->bindParam(':name', $name, PDO::PARAM_STR);
    $stmt->bindParam(':email', $email, PDO::PARAM_STR);
    $stmt->bindParam(':password_hash', $password_hash, PDO::PARAM_STR);
    $stmt->execute();

    send_json_response(true, 'Usuário cadastrado com sucesso!', 201);

} catch (PDOException $e) {
    if ($e->errorInfo[1] == 1062) {
        send_json_response(false, 'Este e-mail já está em uso.', 409);
    } else {
        send_json_response(false, 'Ocorreu um erro no servidor ao tentar registrar.', 500);
    }
}
?>