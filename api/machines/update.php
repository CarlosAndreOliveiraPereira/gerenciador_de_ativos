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

// Validação de Entrada
if (!$data || empty($data->id)) {
    send_json_response(false, 'O ID da máquina é obrigatório.', 400);
}

// Sanitização dos Dados
$id = $data->id;
$localidade = isset($data->localidade) ? trim($data->localidade) : null;
$nome_dispositivo = isset($data->nome_dispositivo) ? trim($data->nome_dispositivo) : null;
$numero_serie = isset($data->numero_serie) ? trim($data->numero_serie) : null;
$nota_fiscal = isset($data->nota_fiscal) ? trim($data->nota_fiscal) : null;
$responsavel = isset($data->responsavel) ? trim($data->responsavel) : null;
$email_responsavel = isset($data->email_responsavel) ? filter_var(trim($data->email_responsavel), FILTER_SANITIZE_EMAIL) : null;
$setor = isset($data->setor) ? trim($data->setor) : null;
$windows_update_ativo = isset($data->windows_update_ativo) ? trim($data->windows_update_ativo) : null;
$sistema_operacional = isset($data->sistema_operacional) ? trim($data->sistema_operacional) : null;
$observacao = isset($data->observacao) ? trim($data->observacao) : null;
$user_id = $_SESSION['user_id'];

// Lógica de Atualização com Tratamento de Erros
try {
    $query = "UPDATE machines SET
                localidade = :localidade,
                nome_dispositivo = :nome_dispositivo,
                numero_serie = :numero_serie,
                nota_fiscal = :nota_fiscal,
                responsavel = :responsavel,
                email_responsavel = :email_responsavel,
                setor = :setor,
                windows_update_ativo = :windows_update_ativo,
                sistema_operacional = :sistema_operacional,
                observacao = :observacao
              WHERE id = :id AND user_id = :user_id";

    $stmt = $pdo->prepare($query);

    $stmt->bindParam(':localidade', $localidade, PDO::PARAM_STR);
    $stmt->bindParam(':nome_dispositivo', $nome_dispositivo, PDO::PARAM_STR);
    $stmt->bindParam(':numero_serie', $numero_serie, PDO::PARAM_STR);
    $stmt->bindParam(':nota_fiscal', $nota_fiscal, PDO::PARAM_STR);
    $stmt->bindParam(':responsavel', $responsavel, PDO::PARAM_STR);
    $stmt->bindParam(':email_responsavel', $email_responsavel, PDO::PARAM_STR);
    $stmt->bindParam(':setor', $setor, PDO::PARAM_STR);
    $stmt->bindParam(':windows_update_ativo', $windows_update_ativo, PDO::PARAM_STR);
    $stmt->bindParam(':sistema_operacional', $sistema_operacional, PDO::PARAM_STR);
    $stmt->bindParam(':observacao', $observacao, PDO::PARAM_STR);
    $stmt->bindParam(':id', $id, PDO::PARAM_INT);
    $stmt->bindParam(':user_id', $user_id, PDO::PARAM_INT);

    $stmt->execute();

    if ($stmt->rowCount() > 0) {
        send_json_response(true, 'Máquina atualizada com sucesso!');
    } else {
        send_json_response(false, 'Máquina não encontrada, ou você não tem permissão, ou nenhum dado foi alterado.', 404);
    }

} catch (PDOException $e) {
    // Para depuração: error_log($e->getMessage());
    send_json_response(false, 'Ocorreu um erro no servidor ao atualizar a máquina.', 500);
}
?>