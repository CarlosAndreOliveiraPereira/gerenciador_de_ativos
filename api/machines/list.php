<?php

declare(strict_types=1);

require_once __DIR__ . '/../bootstrap.php';

$userId = require_auth();
$search = trim($_GET['search'] ?? '');

try {
    if ($search !== '') {
        $stmt = $pdo->prepare(
            'SELECT id, nome_dispositivo, setor, responsavel
             FROM machines
             WHERE user_id = :user_id
               AND (
                    nome_dispositivo LIKE :term OR
                    setor LIKE :term OR
                    responsavel LIKE :term
               )
             ORDER BY nome_dispositivo ASC'
        );
        $stmt->bindValue(':term', sanitize_like($search), PDO::PARAM_STR);
    } else {
        $stmt = $pdo->prepare(
            'SELECT id, nome_dispositivo, setor, responsavel
             FROM machines
             WHERE user_id = :user_id
             ORDER BY id DESC
             LIMIT 100'
        );
    }

    $stmt->bindValue(':user_id', $userId, PDO::PARAM_INT);
    $stmt->execute();
    $machines = $stmt->fetchAll();

    echo json_encode($machines, JSON_UNESCAPED_UNICODE);
} catch (PDOException $exception) {
    respond_error('Não foi possível carregar a lista de ativos.', 500);
}
