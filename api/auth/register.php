<?php
require_once '../config/database.php';

header('Content-Type: application/json');

$data = json_decode(file_get_contents('php://input'), true);

if (empty($data['name']) || empty($data['email']) || empty($data['password'])) {
    echo json_encode(['success' => false, 'message' => 'Todos os campos são obrigatórios.']);
    exit;
}

$name = $data['name'];
$email = $data['email'];
$password = $data['password'];
$password_hash = password_hash($password, PASSWORD_DEFAULT);

try {
    $stmt = $pdo->prepare("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)");
    $stmt->execute([$name, $email, $password_hash]);
    echo json_encode(['success' => true, 'message' => 'Usuário cadastrado com sucesso!']);
} catch (PDOException $e) {
    if ($e->errorInfo[1] == 1062) { // Código de erro para entrada duplicada
        echo json_encode(['success' => false, 'message' => 'Este e-mail já está em uso.']);
    } else {
        echo json_encode(['success' => false, 'message' => 'Erro ao cadastrar usuário.']);
    }
}
?>