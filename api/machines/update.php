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
if (!$data || empty($data->id) || empty($data->name) || empty($data->model) || empty($data->serial_number)) {
    send_json_response(false, 'ID, nome, modelo e número de série são obrigatórios.', 400);
}

// 2. Sanitização dos Dados
$id = $data->id;
$name = trim($data->name);
$model = trim($data->model);
$serial_number = trim($data->serial_number);
$description = isset($data->description) ? trim($data->description) : '';
$user_id = $_SESSION['user_id'];

if (empty($name) || empty($model) || empty($serial_number)) {
    send_json_response(false, 'Os campos obrigatórios não podem estar vazios.', 400);
}

// 3. Lógica de Atualização com Tratamento de Erros e Verificação de Propriedade
try {
    $query = "UPDATE machines SET name = :name, model = :model, serial_number = :serial_number, description = :description WHERE id = :id AND user_id = :user_id";

    $stmt = $pdo->prepare($query);
    $stmt->bindParam(':name', $name, PDO::PARAM_STR);
    $stmt->bindParam(':model', $model, PDO::PARAM_STR);
    $stmt->bindParam(':serial_number', $serial_number, PDO::PARAM_STR);
    $stmt->bindParam(':description', $description, PDO::PARAM_STR);
    $stmt->bindParam(':id', $id, PDO::PARAM_INT);
    $stmt->bindParam(':user_id', $user_id, PDO::PARAM_INT);

    $stmt->execute();

    // Verifica se alguma linha foi realmente atualizada
    if ($stmt->rowCount() > 0) {
        send_json_response(true, 'Máquina atualizada com sucesso!');
    } else {
        // Nenhuma linha afetada, significa que a máquina não foi encontrada ou não pertence ao usuário
        send_json_response(false, 'Máquina não encontrada ou você não tem permissão para editá-la.', 404);
    }

} catch (PDOException $e) {
    // Erro interno do servidor
    send_json_response(false, 'Ocorreu um erro no servidor ao atualizar a máquina.', 500);
}
?>