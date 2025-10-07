<?php
session_start();
require_once '../config/database.php';

header('Content-Type: application/json');

// Função para enviar resposta JSON e sair
function send_json_response($success, $data) {
    http_response_code($data['statusCode'] ?? 200);
    unset($data['statusCode']);
    echo json_encode(['success' => $success] + $data);
    exit;
}

// Verifica se o usuário já passou pela primeira etapa do login
if (!isset($_SESSION['mfa_user_id'])) {
    send_json_response(false, ['message' => 'A verificação de login não foi iniciada.', 'statusCode' => 401]);
}

$data = json_decode(file_get_contents('php://input'), true);
$user_id = $_SESSION['mfa_user_id'];
$mfa_code = $data['mfa_code'] ?? '';

if (empty($mfa_code) || !preg_match('/^[0-9]{6}$/', $mfa_code)) {
    send_json_response(false, ['message' => 'O código MFA deve ter 6 dígitos.', 'statusCode' => 400]);
}

try {
    $stmt = $pdo->prepare("SELECT name, mfa_code, mfa_code_expires_at FROM users WHERE id = :id");
    $stmt->bindParam(':id', $user_id, PDO::PARAM_INT);
    $stmt->execute();
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$user) {
        send_json_response(false, ['message' => 'Usuário não encontrado.', 'statusCode' => 404]);
    }

    $now = new DateTime();
    $expires_at = new DateTime($user['mfa_code_expires_at']);

    // Verifica se o código é válido e não expirou
    if ($user['mfa_code'] === $mfa_code && $now < $expires_at) {
        // Sucesso! Finaliza o login.

        // 1. Limpa o código MFA do banco de dados
        $clear_stmt = $pdo->prepare("UPDATE users SET mfa_code = NULL, mfa_code_expires_at = NULL WHERE id = :id");
        $clear_stmt->bindParam(':id', $user_id, PDO::PARAM_INT);
        $clear_stmt->execute();

        // 2. Regenera a sessão e armazena os dados finais do usuário
        session_regenerate_id(true);
        unset($_SESSION['mfa_user_id']);
        $_SESSION['user_id'] = $user_id;
        $_SESSION['user_name'] = $user['name'];

        send_json_response(true, ['message' => 'Login verificado com sucesso!']);
    } else {
        // Código inválido ou expirado
        send_json_response(false, ['message' => 'Código de verificação inválido ou expirado.', 'statusCode' => 401]);
    }

} catch (Exception $e) {
    // Para depuração: error_log($e->getMessage());
    send_json_response(false, ['message' => 'Ocorreu um erro no servidor.', 'statusCode' => 500]);
}
?>