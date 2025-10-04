<?php
header('Content-Type: application/json');
require_once '../middleware/auth_check.php';
require_once '../config/database.php';

$user_id = $_SESSION['user_id'];

try {
    $query = "SELECT id, name, model, serial_number, description FROM machines WHERE user_id = :user_id ORDER BY name ASC";
    $stmt = $pdo->prepare($query);
    $stmt->bindParam(':user_id', $user_id, PDO::PARAM_INT);
    $stmt->execute();

    $machines = $stmt->fetchAll(PDO::FETCH_ASSOC);

    echo json_encode(['success' => true, 'machines' => $machines]);

} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Erro ao buscar as máquinas: ' . $e->getMessage()]);
}
?>