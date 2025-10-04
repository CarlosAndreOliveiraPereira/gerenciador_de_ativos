<?php
require_once '../middleware/auth_check.php';
require_once '../config/database.php';

header('Content-Type: application/json');

$data = json_decode(file_get_contents('php://input'), true);
$user_id = $_SESSION['user_id'];
$machine_id = $data['id'] ?? 0;

// A verificação 'user_id' garante que um usuário não apague a máquina de outro
$stmt = $pdo->prepare("DELETE FROM machines WHERE id = ? AND user_id = ?");
$stmt->execute([$machine_id, $user_id]);

if ($stmt->rowCount() > 0) {
    echo json_encode(['success' => true, 'message' => 'Máquina excluída com sucesso!']);
} else {
    echo json_encode(['success' => false, 'message' => 'Máquina não encontrada ou você não tem permissão.']);
}
?>