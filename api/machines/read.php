<?php

declare(strict_types=1);

require_once __DIR__ . '/../bootstrap.php';

$userId = require_auth();
$search = trim($_GET['search'] ?? '');

try {
    $query = 'SELECT id, localidade, nome_dispositivo, numero_serie, nota_fiscal,
                     responsavel, email_responsavel, setor, windows_update_ativo,
                     sistema_operacional, observacao
              FROM machines
              WHERE user_id = :user_id';

    $params = [':user_id' => $userId];

    if ($search !== '') {
        $query .= ' AND (
            localidade LIKE :term OR
            nome_dispositivo LIKE :term OR
            numero_serie LIKE :term OR
            nota_fiscal LIKE :term OR
            responsavel LIKE :term OR
            email_responsavel LIKE :term OR
            setor LIKE :term OR
            sistema_operacional LIKE :term OR
            observacao LIKE :term
        )';
        $params[':term'] = sanitize_like($search);
    }

    $query .= ' ORDER BY nome_dispositivo ASC';

    $stmt = $pdo->prepare($query);
    $stmt->execute($params);

    respond([
        'success' => true,
        'machines' => $stmt->fetchAll(),
    ]);
} catch (PDOException $exception) {
    respond_error('Não foi possível recuperar os ativos.', 500);
}
