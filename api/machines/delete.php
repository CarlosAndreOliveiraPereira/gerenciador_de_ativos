<?php
header('Content-Type: application/json');
require_once '../middleware/auth_check.php';
require_once '../config/database.php';

$data = json_decode(file_get_contents('php://input'));

if (empty($data->id)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'ID da máquina não fornecido.']);
    exit;
}

$user_id = $_SESSION['user_id'];
$machine_id = $data->id;

try {
    // Verifica se a máquina pertence ao usuário logado
    $check_query = "SELECT user_id FROM machines WHERE id = :id";
    $check_stmt = $pdo->prepare($check_query);
    $check_stmt->bindParam(':id', $machine_id, PDO::PARAM_INT);
    $check_stmt->execute();
    $machine = $check_stmt->fetch(PDO::FETCH_ASSOC);

    if (!$machine || $machine['user_id'] != $user_id) {
        http_response_code(403); // Forbidden
        echo json_encode(['success' => false, 'message' => 'Você não tem permissão para excluir esta máquina.']);
        exit;
    }

    // Se a verificação passar, exclui a máquina
    $delete_query = "DELETE FROM machines WHERE id = :id";
    $delete_stmt = $pdo->prepare($delete_query);
    $delete_stmt->bindParam(':id', $machine_id, PDO::PARAM_INT);

    if ($delete_stmt->execute()) {
        echo json_encode(['success' => true, 'message' => 'Máquina excluída com sucesso!']);
    } else {
        http_response_code(500);
        echo json_encode(['success' => false, 'message' => 'Não foi possível excluir a máquina.']);
    }

} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Erro no servidor: ' . $e->getMessage()]);
}
?>