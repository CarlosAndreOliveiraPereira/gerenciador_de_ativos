<?php

declare(strict_types=1);

require_once __DIR__ . '/../bootstrap.php';

$userId = require_auth();
$id = isset($_GET['id']) ? (int) $_GET['id'] : 0;

if ($id <= 0) {
    respond_error('ID do ativo inválido.', 400);
}

try {
    $stmt = $pdo->prepare('SELECT * FROM machines WHERE id = :id AND user_id = :user_id LIMIT 1');
    $stmt->bindValue(':id', $id, PDO::PARAM_INT);
    $stmt->bindValue(':user_id', $userId, PDO::PARAM_INT);
    $stmt->execute();
    $machine = $stmt->fetch();

    if (!$machine) {
        respond_error('Ativo não encontrado.', 404);
    }

    respond([
        'success' => true,
        'data' => $machine,
    ]);
} catch (PDOException $exception) {
    respond_error('Não foi possível carregar os dados do ativo.', 500);
}
