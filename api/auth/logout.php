<?php
session_start();
session_destroy(); // Destrói todos os dados da sessão
header('Content-Type: application/json');
echo json_encode(['success' => true, 'message' => 'Logout realizado com sucesso.']);
?>