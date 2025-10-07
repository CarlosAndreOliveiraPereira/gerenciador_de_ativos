<?php
require_once '../middleware/auth_check.php';
require_once '../config/database.php';

header('Content-Type: application/json');

// Função para enviar resposta JSON e sair
function send_json_response($success, $data, $statusCode = 200) {
    http_response_code($statusCode);
    // Para este endpoint, a chave principal é 'machines' ou 'message'
    $key = $success ? 'machines' : 'message';
    echo json_encode(['success' => $success, $key => $data]);
    exit;
}

$user_id = $_SESSION['user_id'];

try {
    $query = "SELECT id, name, model, serial_number, description FROM machines WHERE user_id = :user_id ORDER BY name ASC";

    $stmt = $pdo->prepare($query);
    $stmt->bindParam(':user_id', $user_id, PDO::PARAM_INT);
    $stmt->execute();

    $machines = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Envia os dados com sucesso, mesmo que a lista esteja vazia
    send_json_response(true, $machines);

} catch (PDOException $e) {
    // Erro interno do servidor
    send_json_response(false, 'Ocorreu um erro no servidor ao buscar as máquinas.', 500);
}
?>