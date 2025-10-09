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

$data = json_decode(file_get_contents('php://input'), true);

if (!$data || empty($data['email']) || empty($data['password'])) {
    send_json_response(false, ['message' => 'E-mail e senha são obrigatórios.', 'statusCode' => 400]);
}

if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
    send_json_response(false, ['message' => 'Formato de e-mail inválido.', 'statusCode' => 400]);
}

$email = $data['email'];
$password = $data['password'];

try {
    $stmt = $pdo->prepare("SELECT id, name, password_hash FROM users WHERE email = :email");
    $stmt->bindParam(':email', $email, PDO::PARAM_STR);
    $stmt->execute();
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($user && password_verify($password, $user['password_hash'])) {
        // Senha correta, iniciar fluxo MFA
        $mfa_code = str_pad(random_int(0, 999999), 6, '0', STR_PAD_LEFT);
        $mfa_expires_at = (new DateTime('+10 minutes'))->format('Y-m-d H:i:s');

        $update_stmt = $pdo->prepare("UPDATE users SET mfa_code = :mfa_code, mfa_code_expires_at = :expires WHERE id = :id");
        $update_stmt->bindParam(':mfa_code', $mfa_code, PDO::PARAM_STR);
        $update_stmt->bindParam(':expires', $mfa_expires_at, PDO::PARAM_STR);
        $update_stmt->bindParam(':id', $user['id'], PDO::PARAM_INT);
        $update_stmt->execute();

        // ** SIMULAÇÃO DE ENVIO DE E-MAIL **
        // Em um ambiente de produção, aqui você enviaria o e-mail:
        // mail($email, 'Seu código de login', "Seu código de verificação é: $mfa_code");

        // Armazena temporariamente o ID do usuário para a próxima etapa
        $_SESSION['mfa_user_id'] = $user['id'];

        // Retorna sucesso e a necessidade de MFA.
        // Em produção, NUNCA envie o código na resposta. Isto é apenas para facilitar o teste.
        send_json_response(true, [
            'mfa_required' => true,
            'message' => "Enviamos um código de verificação para o seu e-mail. Código para teste: $mfa_code"
        ]);

    } else {
        send_json_response(false, ['message' => 'E-mail ou senha inválidos.', 'statusCode' => 401]);
    }
} catch (Exception $e) {
    // Para depuração: error_log($e->getMessage());
    send_json_response(false, ['message' => 'Ocorreu um erro no servidor.', 'statusCode' => 500]);
}
?>