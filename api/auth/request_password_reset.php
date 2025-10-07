<?php
require_once '../config/database.php';

header('Content-Type: application/json');

function send_json_response($success, $message, $statusCode = 200) {
    http_response_code($statusCode);
    echo json_encode(['success' => $success, 'message' => $message]);
    exit;
}

$data = json_decode(file_get_contents('php://input'), true);

if (empty($data['email']) || !filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
    send_json_response(false, 'Por favor, insira um endereço de e-mail válido.', 400);
}

$email = $data['email'];

try {
    // 1. Verificar se o usuário existe
    $stmt = $pdo->prepare("SELECT id FROM users WHERE email = :email");
    $stmt->bindParam(':email', $email, PDO::PARAM_STR);
    $stmt->execute();
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($user) {
        // 2. Gerar um token seguro
        $token = bin2hex(random_bytes(32));
        $expires_at = (new DateTime('+1 hour'))->format('Y-m-d H:i:s');

        // 3. Salvar o token e a data de expiração no banco de dados
        $update_stmt = $pdo->prepare(
            "UPDATE users SET password_reset_token = :token, password_reset_expires_at = :expires WHERE id = :id"
        );
        $update_stmt->bindParam(':token', $token, PDO::PARAM_STR);
        $update_stmt->bindParam(':expires', $expires_at, PDO::PARAM_STR);
        $update_stmt->bindParam(':id', $user['id'], PDO::PARAM_INT);
        $update_stmt->execute();

        // 4. ** SIMULAÇÃO DE ENVIO DE E-MAIL **
        // Em um ambiente de produção, você enviaria o link por e-mail.
        // Aqui, retornamos o link na resposta para facilitar o teste.
        $reset_link = "http://localhost/html/reset_password.html?token=" . $token;

        $message = "Um link de recuperação de senha foi enviado para seu e-mail (simulação). Link para teste: " . $reset_link;
        send_json_response(true, $message);

    } else {
        // Para segurança, não revelamos se o e-mail existe ou não.
        send_json_response(true, "Se um usuário com este e-mail existir, um link de recuperação foi enviado.");
    }

} catch (Exception $e) {
    // Para depuração: error_log($e->getMessage());
    send_json_response(false, 'Ocorreu um erro no servidor.', 500);
}
?>