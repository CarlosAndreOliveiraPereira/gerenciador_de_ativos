<?php
header('Content-Type: application/json');
require_once '../middleware/auth_check.php';
require_once '../config/database.php';

$data = json_decode(file_get_contents('php://input'));

// Validação básica
if (empty($data->id) || empty($data->name) || empty($data->model) || empty($data->serial_number)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Dados incompletos para atualização.']);
    exit;
}

$user_id = $_SESSION['user_id'];
$machine_id = $data->id;
$name = $data->name;
$model = $data->model;
$serial_number = $data->serial_number;
$description = $data->description ?? '';

try {
    // Primeiro, verifica se a máquina pertence ao usuário logado
    $check_query = "SELECT user_id FROM machines WHERE id = :id";
    $check_stmt = $pdo->prepare($check_query);
    $check_stmt->bindParam(':id', $machine_id, PDO::PARAM_INT);
    $check_stmt->execute();
    $machine = $check_stmt->fetch(PDO::FETCH_ASSOC);

    if (!$machine || $machine['user_id'] != $user_id) {
        http_response_code(403); // Forbidden
        echo json_encode(['success' => false, 'message' => 'Você não tem permissão para editar esta máquina.']);
        exit;
    }

    // Se a verificação passar, atualiza a máquina
    $update_query = "UPDATE machines SET name = :name, model = :model, serial_number = :serial_number, description = :description WHERE id = :id";
    $update_stmt = $pdo->prepare($update_query);
    $update_stmt->bindParam(':name', $name, PDO::PARAM_STR);
    $update_stmt->bindParam(':model', $model, PDO::PARAM_STR);
    $update_stmt->bindParam(':serial_number', $serial_number, PDO::PARAM_STR);
    $update_stmt->bindParam(':description', $description, PDO::PARAM_STR);
    $update_stmt->bindParam(':id', $machine_id, PDO::PARAM_INT);

    if ($update_stmt->execute()) {
        echo json_encode(['success' => true, 'message' => 'Máquina atualizada com sucesso!']);
    } else {
        http_response_code(500);
        echo json_encode(['success' => false, 'message' => 'Não foi possível atualizar a máquina.']);
    }

} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Erro no servidor: ' . $e->getMessage()]);
}
?>