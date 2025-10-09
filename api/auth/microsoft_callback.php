<?php
session_start();
require_once '../config/database.php';

// Função para enviar resposta de erro e sair
function send_error_redirect($message) {
    // Idealmente, redirecionar para uma página de erro com a mensagem
    // Por simplicidade, vamos apenas encerrar com a mensagem.
    die("Erro de autenticação: " . htmlspecialchars($message));
}

// 1. Validar o 'state' para proteção contra CSRF
if (empty($_GET['state']) || !isset($_SESSION['oauth2state']) || $_GET['state'] !== $_SESSION['oauth2state']) {
    unset($_SESSION['oauth2state']);
    send_error_redirect('Estado da sessão inválido.');
}

// 2. Trocar o código de autorização por um Access Token
$token_endpoint = 'https://login.microsoftonline.com/' . MICROSOFT_TENANT_ID . '/oauth2/v2.0/token';
$token_params = [
    'client_id' => MICROSOFT_CLIENT_ID,
    'client_secret' => MICROSOFT_CLIENT_SECRET,
    'redirect_uri' => MICROSOFT_REDIRECT_URI,
    'scope' => 'openid profile email User.Read',
    'grant_type' => 'authorization_code',
    'code' => $_GET['code'],
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
    send_error_redirect('Falha ao obter o token de acesso da Microsoft.');
}

// 3. Usar o Access Token para obter informações do usuário (Microsoft Graph API)
$graph_endpoint = 'https://graph.microsoft.com/v1.0/me';
$headers = [
    'Authorization: Bearer ' . $token_data['access_token'],
    'Content-Type: application/json'
];

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $graph_endpoint);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$graph_response = curl_exec($ch);
curl_close($ch);

$user_data = json_decode($graph_response, true);
if (empty($user_data['mail']) || empty($user_data['displayName'])) {
    send_error_redirect('Não foi possível obter os dados do usuário da Microsoft.');
}

$user_email = strtolower($user_data['mail']);
$user_name = $user_data['displayName'];

// 4. Validar o domínio do e-mail
if (substr($user_email, -17) !== '@grupomysa.com.br') {
    send_error_redirect('Acesso permitido apenas para usuários com o domínio @grupomysa.com.br.');
}

// 5. Verificar se o usuário existe no banco de dados ou criá-lo
try {
    $stmt = $pdo->prepare("SELECT id, name FROM users WHERE email = :email");
    $stmt->bindParam(':email', $user_email, PDO::PARAM_STR);
    $stmt->execute();
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($user) {
        // Usuário existe, usa o ID existente
        $user_id = $user['id'];
    } else {
        // Usuário não existe, cria um novo registro
        // Como não temos mais senha, podemos inserir um hash vazio ou um valor placeholder
        $placeholder_hash = password_hash(bin2hex(random_bytes(32)), PASSWORD_DEFAULT);

        $insert_stmt = $pdo->prepare("INSERT INTO users (name, email, password_hash) VALUES (:name, :email, :password_hash)");
        $insert_stmt->bindParam(':name', $user_name, PDO::PARAM_STR);
        $insert_stmt->bindParam(':email', $user_email, PDO::PARAM_STR);
        $insert_stmt->bindParam(':password_hash', $placeholder_hash, PDO::PARAM_STR);
        $insert_stmt->execute();
        $user_id = $pdo->lastInsertId();
    }

    // 6. Iniciar a sessão do usuário
    session_regenerate_id(true);
    $_SESSION['user_id'] = $user_id;
    $_SESSION['user_name'] = $user_name;
    unset($_SESSION['oauth2state']);

    // 7. Redirecionar para o dashboard
    header('Location: ../../html/dashboard.html');
    exit();

} catch (PDOException $e) {
    send_error_redirect('Erro de banco de dados: ' . $e->getMessage());
}
?>