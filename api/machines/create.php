<?php
header('Content-Type: application/json');
require_once '../middleware/auth_check.php';
require_once '../config/database.php';

$data = json_decode(file_get_contents('php://input'));

// Validação básica dos dados recebidos
if (empty($data->name) || empty($data->model) || empty($data->serial_number)) {
    http_response_code(400); // Bad Request
    echo json_encode(['success' => false, 'message' => 'Todos os campos obrigatórios devem ser preenchidos.']);
    exit;
}

$user_id = $_SESSION['user_id'];
$name = $data->name;
$model = $data->model;
$serial_number = $data->serial_number;
$description = $data->description ?? ''; // Opcional

try {
    $query = "INSERT INTO machines (user_id, name, model, serial_number, description) VALUES (:user_id, :name, :model, :serial_number, :description)";
    $stmt = $pdo->prepare($query);

    $stmt->bindParam(':user_id', $user_id, PDO::PARAM_INT);
    $stmt->bindParam(':name', $name, PDO::PARAM_STR);
    $stmt->bindParam(':model', $model, PDO::PARAM_STR);
    $stmt->bindParam(':serial_number', $serial_number, PDO::PARAM_STR);
    $stmt->bindParam(':description', $description, PDO::PARAM_STR);

    if ($stmt->execute()) {
        echo json_encode(['success' => true, 'message' => 'Máquina adicionada com sucesso!']);
    } else {
        http_response_code(500); // Internal Server Error
        echo json_encode(['success' => false, 'message' => 'Não foi possível adicionar a máquina.']);
    }
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Erro no servidor: ' . $e->getMessage()]);
}
?>