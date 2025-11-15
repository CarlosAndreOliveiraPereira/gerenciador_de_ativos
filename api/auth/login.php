<?php

declare(strict_types=1);

require_once __DIR__ . '/../bootstrap.php';

$data = request_body();
$email = trim($data['email'] ?? '');
$password = $data['password'] ?? '';

if ($email === '' || $password === '') {
    respond_error('E-mail e senha são obrigatórios.', 400);
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond_error('Formato de e-mail inválido.', 400);
}

try {
    $stmt = $pdo->prepare('SELECT id, name, password_hash FROM users WHERE email = :email LIMIT 1');
    $stmt->bindValue(':email', $email, PDO::PARAM_STR);
    $stmt->execute();
    $user = $stmt->fetch();

    if (!$user || !password_verify($password, $user['password_hash'])) {
        respond_error('E-mail ou senha inválidos.', 401);
    }

    session_regenerate_id(true);
    $_SESSION['user_id'] = (int) $user['id'];
    $_SESSION['user_name'] = $user['name'];

    respond_success('Login realizado com sucesso.');
} catch (PDOException $exception) {
    respond_error('Erro no servidor. Tente novamente em instantes.', 500);
}
