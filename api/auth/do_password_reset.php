<?php

declare(strict_types=1);

require_once __DIR__ . '/../bootstrap.php';

$data = request_body();
$token = trim($data['token'] ?? '');
$password = $data['password'] ?? '';
$confirm = $data['confirm_password'] ?? '';

if ($token === '' || $password === '' || $confirm === '') {
    respond_error('Todos os campos são obrigatórios.', 400);
}

if ($password !== $confirm) {
    respond_error('As senhas não coincidem.', 400);
}

if (mb_strlen($password) < 8) {
    respond_error('A nova senha deve ter pelo menos 8 caracteres.', 400);
}

try {
    $stmt = $pdo->prepare('SELECT id, password_reset_expires_at FROM users WHERE password_reset_token = :token LIMIT 1');
    $stmt->bindValue(':token', $token, PDO::PARAM_STR);
    $stmt->execute();
    $user = $stmt->fetch();

    if (!$user) {
        respond_error('Token de recuperação inválido ou expirado.', 404);
    }

    $expires = isset($user['password_reset_expires_at']) ? new DateTime($user['password_reset_expires_at']) : null;
    if ($expires && new DateTime() > $expires) {
        respond_error('O token de recuperação expirou. Solicite um novo link.', 401);
    }

    $update = $pdo->prepare(
        'UPDATE users SET password_hash = :password, password_reset_token = NULL, password_reset_expires_at = NULL WHERE id = :id'
    );
    $update->bindValue(':password', password_hash($password, PASSWORD_DEFAULT), PDO::PARAM_STR);
    $update->bindValue(':id', $user['id'], PDO::PARAM_INT);
    $update->execute();

    respond_success('Sua senha foi atualizada com sucesso.');
} catch (Throwable $exception) {
    respond_error('Não foi possível redefinir a senha agora.', 500);
}
