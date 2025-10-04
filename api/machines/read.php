<?php
require_once '../middleware/auth_check.php';
require_once '../config/database.php';

header('Content-Type: application/json');

$user_id = $_SESSION['user_id'];

$stmt = $pdo->prepare("SELECT id, name, type, model, serial_number, created_at FROM machines WHERE user_id = ? ORDER BY created_at DESC");
$stmt->execute([$user_id]);
$machines = $stmt->fetchAll(PDO::FETCH_ASSOC);

echo json_encode(['success' => true, 'machines' => $machines]);
?>