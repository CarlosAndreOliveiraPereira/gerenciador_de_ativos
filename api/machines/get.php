<?php
session_start();
require_once '../config/database.php';

header('Content-Type: application/json');

if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['success' => false, 'message' => 'Acesso não autorizado.']);
    exit;
}

$machineId = isset($_GET['id']) ? (int)$_GET['id'] : 0;

if ($machineId <= 0) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'ID do ativo inválido.']);
    exit;
}

try {
    $stmt = $pdo->prepare("SELECT * FROM machines WHERE id = :id");
    $stmt->bindParam(':id', $machineId, PDO::PARAM_INT);
    $stmt->execute();

    $machine = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($machine) {
        echo json_encode(['success' => true, 'data' => $machine]);
    } else {
        http_response_code(404);
        echo json_encode(['success' => false, 'message' => 'Ativo não encontrado.']);
    }
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Erro no servidor ao buscar o ativo.']);
}
?>