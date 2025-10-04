<?php
require_once '../middleware/auth_check.php';
require_once '../config/database.php';

header('Content-Type: application/json');

$data = json_decode(file_get_contents('php://input'), true);
$user_id = $_SESSION['user_id'];

$name = $data['name'] ?? '';
$type = $data['type'] ?? '';
$model = $data['model'] ?? '';
$serial = $data['serial_number'] ?? '';

$stmt = $pdo->prepare("INSERT INTO machines (user_id, name, type, model, serial_number) VALUES (?, ?, ?, ?, ?)");
$stmt->execute([$user_id, $name, $type, $model, $serial]);

echo json_encode(['success' => true, 'message' => 'Máquina adicionada com sucesso!']);
?>