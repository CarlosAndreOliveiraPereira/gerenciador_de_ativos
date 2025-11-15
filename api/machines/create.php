<?php

declare(strict_types=1);

require_once __DIR__ . '/../bootstrap.php';

$userId = require_auth();
$data = request_body();

$fields = [
    'localidade' => trim($data['localidade'] ?? ''),
    'nome_dispositivo' => trim($data['nome_dispositivo'] ?? ''),
    'numero_serie' => trim($data['numero_serie'] ?? ''),
    'nota_fiscal' => trim($data['nota_fiscal'] ?? ''),
    'responsavel' => trim($data['responsavel'] ?? ''),
    'email_responsavel' => trim($data['email_responsavel'] ?? ''),
    'setor' => trim($data['setor'] ?? ''),
    'windows_update_ativo' => trim($data['windows_update_ativo'] ?? ''),
    'sistema_operacional' => trim($data['sistema_operacional'] ?? ''),
    'observacao' => trim($data['observacao'] ?? ''),
];

try {
    $stmt = $pdo->prepare(
        'INSERT INTO machines (
            user_id, localidade, nome_dispositivo, numero_serie, nota_fiscal,
            responsavel, email_responsavel, setor, windows_update_ativo,
            sistema_operacional, observacao
        ) VALUES (
            :user_id, :localidade, :nome_dispositivo, :numero_serie, :nota_fiscal,
            :responsavel, :email_responsavel, :setor, :windows_update_ativo,
            :sistema_operacional, :observacao
        )'
    );

    $stmt->execute([
        ':user_id' => $userId,
        ':localidade' => $fields['localidade'] ?: null,
        ':nome_dispositivo' => $fields['nome_dispositivo'] ?: null,
        ':numero_serie' => $fields['numero_serie'] ?: null,
        ':nota_fiscal' => $fields['nota_fiscal'] ?: null,
        ':responsavel' => $fields['responsavel'] ?: null,
        ':email_responsavel' => $fields['email_responsavel'] ?: null,
        ':setor' => $fields['setor'] ?: null,
        ':windows_update_ativo' => $fields['windows_update_ativo'] ?: null,
        ':sistema_operacional' => $fields['sistema_operacional'] ?: null,
        ':observacao' => $fields['observacao'] ?: null,
    ]);

    respond_success('Máquina cadastrada com sucesso.', ['id' => (int) $pdo->lastInsertId()]);
} catch (PDOException $exception) {
    respond_error('Não foi possível cadastrar a máquina agora.', 500);
}
