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
if (!$data || empty($data->id)) {
    send_json_response(false, 'O ID da máquina é obrigatório.', 400);
}

// 2. Sanitização do ID
$id = filter_var($data->id, FILTER_VALIDATE_INT);
if ($id === false) {
    send_json_response(false, 'Formato de ID inválido.', 400);
}

$user_id = $_SESSION['user_id'];

// 3. Lógica de Exclusão com Tratamento de Erros e Verificação de Propriedade
try {
    $query = "DELETE FROM machines WHERE id = :id AND user_id = :user_id";

    $stmt = $pdo->prepare($query);
    $stmt->bindParam(':id', $id, PDO::PARAM_INT);
    $stmt->bindParam(':user_id', $user_id, PDO::PARAM_INT);

    $stmt->execute();

    // Verifica se alguma linha foi realmente excluída
    if ($stmt->rowCount() > 0) {
        send_json_response(true, 'Máquina excluída com sucesso!');
    } else {
        // Nenhuma linha afetada, significa que a máquina não foi encontrada ou não pertence ao usuário
        send_json_response(false, 'Máquina não encontrada ou você não tem permissão para excluí-la.', 404);
    }

} catch (PDOException $e) {
    // Erro interno do servidor
    send_json_response(false, 'Ocorreu um erro no servidor ao excluir a máquina.', 500);
}
?>