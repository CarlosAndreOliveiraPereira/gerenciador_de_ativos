<?php
require_once '../config/database.php';

header('Content-Type: application/json');

function send_json_response($success, $message, $statusCode = 200) {
    http_response_code($statusCode);
    echo json_encode(['success' => $success, 'message' => $message]);
    exit;
}

$data = json_decode(file_get_contents('php://input'), true);

// 1. Validação de Entrada
if (empty($data['token']) || empty($data['password']) || empty($data['confirm_password'])) {
    send_json_response(false, 'Todos os campos são obrigatórios.', 400);
}

$token = $data['token'];
$password = $data['password'];
$confirm_password = $data['confirm_password'];

if ($password !== $confirm_password) {
    send_json_response(false, 'As senhas não coincidem.', 400);
}

if (strlen($password) < 8) {
    send_json_response(false, 'A nova senha deve ter pelo menos 8 caracteres.', 400);
}

// 2. Lógica de Redefinição de Senha
try {
    // 2.1. Encontrar o usuário pelo token e verificar a validade
    $query = "SELECT id, password_reset_expires_at FROM users WHERE password_reset_token = :token";
    $stmt = $pdo->prepare($query);
    $stmt->bindParam(':token', $token, PDO::PARAM_STR);
    $stmt->execute();
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$user) {
        send_json_response(false, 'Token de recuperação inválido ou não encontrado.', 404);
    }

    $now = new DateTime();
    $expires_at = new DateTime($user['password_reset_expires_at']);

    if ($now > $expires_at) {
        send_json_response(false, 'O token de recuperação de senha expirou. Por favor, solicite um novo.', 401);
    }

    // 2.2. Se o token for válido, atualizar a senha e invalidar o token
    $new_password_hash = password_hash($password, PASSWORD_DEFAULT);

    $update_query = "UPDATE users SET
                        password_hash = :password_hash,
                        password_reset_token = NULL,
                        password_reset_expires_at = NULL
                     WHERE id = :id";

    $update_stmt = $pdo->prepare($update_query);
    $update_stmt->bindParam(':password_hash', $new_password_hash, PDO::PARAM_STR);
    $update_stmt->bindParam(':id', $user['id'], PDO::PARAM_INT);
    $update_stmt->execute();

    send_json_response(true, 'Sua senha foi redefinida com sucesso! Você já pode fazer login.');

} catch (Exception $e) {
    // Para depuração: error_log($e->getMessage());
    send_json_response(false, 'Ocorreu um erro no servidor ao tentar redefinir a senha.', 500);
}
?>