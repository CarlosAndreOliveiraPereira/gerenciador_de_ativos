<?php

declare(strict_types=1);

require_once __DIR__ . '/../bootstrap.php';

$data = request_body();
$email = trim($data['email'] ?? '');

if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond_error('Informe um endereço de e-mail válido.', 400);
}

try {
    $stmt = $pdo->prepare('SELECT id FROM users WHERE email = :email LIMIT 1');
    $stmt->bindValue(':email', $email, PDO::PARAM_STR);
    $stmt->execute();
    $user = $stmt->fetch();

    if ($user) {
        $token = bin2hex(random_bytes(32));
        $expiresAt = (new DateTime('+1 hour'))->format('Y-m-d H:i:s');

        $update = $pdo->prepare('UPDATE users SET password_reset_token = :token, password_reset_expires_at = :expires WHERE id = :id');
        $update->bindValue(':token', $token, PDO::PARAM_STR);
        $update->bindValue(':expires', $expiresAt, PDO::PARAM_STR);
        $update->bindValue(':id', $user['id'], PDO::PARAM_INT);
        $update->execute();

        $resetLink = sprintf('http://localhost/html/reset_password.html?token=%s', $token);
        respond_success('Enviamos o link de redefinição (simulação).', ['reset_link' => $resetLink]);
    }

    respond_success('Se o e-mail estiver cadastrado, enviaremos as instruções.');
} catch (Throwable $exception) {
    respond_error('Não foi possível enviar o link de redefinição agora.', 500);
}
