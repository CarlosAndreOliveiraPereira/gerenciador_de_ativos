<?php

declare(strict_types=1);

require_once __DIR__ . '/../bootstrap.php';

$data = request_body();
$name = trim($data['name'] ?? '');
$email = trim($data['email'] ?? '');
$password = $data['password'] ?? '';

if ($name === '' || $email === '' || $password === '') {
    respond_error('Todos os campos são obrigatórios.', 400);
}

if (mb_strlen($name) < 2) {
    respond_error('O nome deve ter pelo menos 2 caracteres.', 400);
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond_error('Informe um e-mail válido.', 400);
}

if (mb_strlen($password) < 8) {
    respond_error('A senha deve ter pelo menos 8 caracteres.', 400);
}

try {
    $stmt = $pdo->prepare('INSERT INTO users (name, email, password_hash) VALUES (:name, :email, :password)');
    $stmt->bindValue(':name', $name, PDO::PARAM_STR);
    $stmt->bindValue(':email', $email, PDO::PARAM_STR);
    $stmt->bindValue(':password', password_hash($password, PASSWORD_DEFAULT), PDO::PARAM_STR);
    $stmt->execute();

    respond_success('Usuário cadastrado com sucesso.', ['id' => (int) $pdo->lastInsertId()]);
} catch (PDOException $exception) {
    if ($exception->errorInfo[1] === 1062) {
        respond_error('Este e-mail já está em uso.', 409);
    }

    respond_error('Não foi possível concluir o cadastro no momento.', 500);
}
