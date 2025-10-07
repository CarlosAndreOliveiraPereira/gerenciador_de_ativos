<?php
require_once '../middleware/auth_check.php';
require_once '../config/database.php';

header('Content-Type: application/json');

// Função para enviar resposta JSON e sair
function send_json_response($success, $data, $statusCode = 200) {
    http_response_code($statusCode);
    $key = $success ? 'machines' : 'message';
    echo json_encode(['success' => $success, $key => $data]);
    exit;
}

$user_id = $_SESSION['user_id'];
$search_term = isset($_GET['search']) ? trim($_GET['search']) : '';

try {
    $base_query = "SELECT
                    id, localidade, nome_dispositivo, numero_serie, nota_fiscal,
                    responsavel, email_responsavel, setor, windows_update_ativo,
                    sistema_operacional, observacao
                   FROM machines
                   WHERE user_id = :user_id";

    $params = [':user_id' => $user_id];

    // Adiciona a lógica de busca se um termo for fornecido
    if (!empty($search_term)) {
        $base_query .= " AND (
            localidade LIKE :search OR
            nome_dispositivo LIKE :search OR
            numero_serie LIKE :search OR
            nota_fiscal LIKE :search OR
            responsavel LIKE :search OR
            email_responsavel LIKE :search OR
            setor LIKE :search OR
            sistema_operacional LIKE :search OR
            observacao LIKE :search
        )";
        // Adiciona wildcards para a busca LIKE
        $params[':search'] = '%' . $search_term . '%';
    }

    $base_query .= " ORDER BY nome_dispositivo ASC";

    $stmt = $pdo->prepare($base_query);

    // Vincula os parâmetros dinamicamente
    foreach ($params as $key => &$val) {
        $stmt->bindParam($key, $val);
    }

    $stmt->execute();
    $machines = $stmt->fetchAll(PDO::FETCH_ASSOC);

    send_json_response(true, $machines);

} catch (PDOException $e) {
    // Para depuração: error_log($e->getMessage());
    send_json_response(false, 'Ocorreu um erro no servidor ao buscar as máquinas.', 500);
}
?>