<?php
session_start();
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
if (!$data || empty($data['email']) || empty($data['password'])) {
    send_json_response(false, 'E-mail e senha são obrigatórios.', 400);
}

if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
    send_json_response(false, 'Formato de e-mail inválido.', 400);
}

$email = $data['email'];
$password = $data['password'];

// 2. Lógica de Login com Tratamento de Erros
try {
    $stmt = $pdo->prepare("SELECT id, name, password_hash FROM users WHERE email = :email");
    $stmt->bindParam(':email', $email, PDO::PARAM_STR);
    $stmt->execute();
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($user && password_verify($password, $user['password_hash'])) {
        // Login bem-sucedido
        session_regenerate_id(true); // Previne fixação de sessão
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['user_name'] = $user['name'];
        send_json_response(true, 'Login realizado com sucesso!');
    } else {
        // Credenciais inválidas
        send_json_response(false, 'E-mail ou senha inválidos.', 401);
    }
} catch (PDOException $e) {
    // Erro interno do servidor
    // Idealmente, logar o erro em vez de exibi-lo
    send_json_response(false, 'Ocorreu um erro no servidor. Tente novamente mais tarde.', 500);
}
?>