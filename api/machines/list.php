<?php
session_start();
require_once '../config/database.php';

header('Content-Type: application/json');

// Protege o endpoint, garantindo que apenas usuários autenticados possam acessá-lo
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Acesso não autorizado.']);
    exit;
}

// Obtém o termo de busca (se houver)
$searchTerm = isset($_GET['search']) ? $_GET['search'] : '';

try {
    if (!empty($searchTerm)) {
        $stmt = $pdo->prepare(
            "SELECT id, nome_dispositivo, setor, responsavel FROM machines
             WHERE nome_dispositivo LIKE :term
             OR setor LIKE :term
             OR responsavel LIKE :term"
        );
        $stmt->bindValue(':term', '%' . $searchTerm . '%', PDO::PARAM_STR);
    } else {
        $stmt = $pdo->prepare("SELECT id, nome_dispositivo, setor, responsavel FROM machines LIMIT 100"); // Limita a 100 registros por padrão
    }

    $stmt->execute();
    $machines = $stmt->fetchAll(PDO::FETCH_ASSOC);

    echo json_encode($machines);

} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Erro ao buscar os ativos no banco de dados.']);
}
?>