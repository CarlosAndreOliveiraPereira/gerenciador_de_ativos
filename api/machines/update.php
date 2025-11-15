<?php

declare(strict_types=1);

require_once __DIR__ . '/../bootstrap.php';

$userId = require_auth();
$data = request_body();
$id = isset($data['id']) ? (int) $data['id'] : 0;

if ($id <= 0) {
    respond_error('O identificador do ativo é obrigatório.', 400);
}

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
        'UPDATE machines SET
            localidade = :localidade,
            nome_dispositivo = :nome_dispositivo,
            numero_serie = :numero_serie,
            nota_fiscal = :nota_fiscal,
            responsavel = :responsavel,
            email_responsavel = :email_responsavel,
            setor = :setor,
            windows_update_ativo = :windows_update_ativo,
            sistema_operacional = :sistema_operacional,
            observacao = :observacao
         WHERE id = :id AND user_id = :user_id'
    );

    $stmt->execute([
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
        ':id' => $id,
        ':user_id' => $userId,
    ]);

    if ($stmt->rowCount() === 0) {
        respond_error('Máquina não encontrada ou sem alterações.', 404);
    }

    respond_success('Máquina atualizada com sucesso.');
} catch (PDOException $exception) {
    respond_error('Não foi possível atualizar a máquina agora.', 500);
}
