<?php
session_start();
header('Content-Type: application/json');

if (isset($_SESSION['user_id']) && isset($_SESSION['user_name'])) {
    echo json_encode([
        'success' => true,
        'data' => [
            'user_id' => $_SESSION['user_id'],
            'user_name' => $_SESSION['user_name']
        ]
    ]);
} else {
    http_response_code(401); // Não autorizado
    echo json_encode(['success' => false, 'message' => 'Nenhuma sessão ativa.']);
}
?>