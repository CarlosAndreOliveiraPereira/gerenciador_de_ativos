<?php

declare(strict_types=1);

require_once __DIR__ . '/../bootstrap.php';

$userId = require_auth();
$data = request_body();
$id = isset($data['id']) ? (int) $data['id'] : 0;

if ($id <= 0) {
    respond_error('O identificador do ativo é obrigatório.', 400);
}

try {
    $stmt = $pdo->prepare('DELETE FROM machines WHERE id = :id AND user_id = :user_id');
    $stmt->bindValue(':id', $id, PDO::PARAM_INT);
    $stmt->bindValue(':user_id', $userId, PDO::PARAM_INT);
    $stmt->execute();

    if ($stmt->rowCount() === 0) {
        respond_error('Máquina não encontrada ou sem permissão para excluir.', 404);
    }

    respond_success('Máquina excluída com sucesso.');
} catch (PDOException $exception) {
    respond_error('Não foi possível remover a máquina agora.', 500);
}
