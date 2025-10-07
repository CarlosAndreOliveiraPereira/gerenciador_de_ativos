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

// Não há campos estritamente obrigatórios além da associação do usuário,
// então a validação de entrada pode ser mínima.
if (!$data) {
    send_json_response(false, 'Nenhum dado recebido.', 400);
}

// Sanitização dos Dados (usando o operador de coalescência nula para segurança)
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

// Lógica de Criação com Tratamento de Erros
try {
    $query = "INSERT INTO machines (
                user_id, localidade, nome_dispositivo, numero_serie, nota_fiscal,
                responsavel, email_responsavel, setor, windows_update_ativo,
                sistema_operacional, observacao
              ) VALUES (
                :user_id, :localidade, :nome_dispositivo, :numero_serie, :nota_fiscal,
                :responsavel, :email_responsavel, :setor, :windows_update_ativo,
                :sistema_operacional, :observacao
              )";

    $stmt = $pdo->prepare($query);

    $stmt->bindParam(':user_id', $user_id, PDO::PARAM_INT);
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

    $stmt->execute();

    send_json_response(true, 'Máquina adicionada com sucesso!', 201);

} catch (PDOException $e) {
    // Para depuração: error_log($e->getMessage());
    send_json_response(false, 'Ocorreu um erro no servidor ao adicionar a máquina.', 500);
}
?>