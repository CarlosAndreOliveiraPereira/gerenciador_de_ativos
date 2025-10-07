<?php
require_once '../middleware/auth_check.php';
require_once '../config/database.php';

header('Content-Type: application/json');

// Função para enviar resposta JSON e sair
function send_json_response($success, $message, $statusCode = 200) {
    http_response_code($statusCode);
    echo json_encode(['success' => $success, 'message' => $message]);
    exit;
}

$data = json_decode(file_get_contents('php://input'));

// 1. Validação de Entrada
if (!$data || empty($data->name) || empty($data->model) || empty($data->serial_number)) {
    send_json_response(false, 'Nome, modelo e número de série são obrigatórios.', 400);
}

// 2. Sanitização dos Dados
$name = trim($data->name);
$model = trim($data->model);
$serial_number = trim($data->serial_number);
$description = isset($data->description) ? trim($data->description) : '';
$user_id = $_SESSION['user_id'];

if (empty($name) || empty($model) || empty($serial_number)) {
    send_json_response(false, 'Os campos obrigatórios não podem estar vazios.', 400);
}

// 3. Lógica de Criação com Tratamento de Erros
try {
    $query = "INSERT INTO machines (user_id, name, model, serial_number, description) VALUES (:user_id, :name, :model, :serial_number, :description)";
    $stmt = $pdo->prepare($query);

    $stmt->bindParam(':user_id', $user_id, PDO::PARAM_INT);
    $stmt->bindParam(':name', $name, PDO::PARAM_STR);
    $stmt->bindParam(':model', $model, PDO::PARAM_STR);
    $stmt->bindParam(':serial_number', $serial_number, PDO::PARAM_STR);
    $stmt->bindParam(':description', $description, PDO::PARAM_STR);

    $stmt->execute();

    send_json_response(true, 'Máquina adicionada com sucesso!', 201); // 201 Created

} catch (PDOException $e) {
    // Erro interno do servidor
    send_json_response(false, 'Ocorreu um erro no servidor ao adicionar a máquina.', 500);
}
?>