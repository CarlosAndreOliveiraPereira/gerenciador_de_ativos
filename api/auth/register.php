<?php
require_once '../config/database.php';

header('Content-Type: application/json');

// Função para enviar resposta JSON e sair
function send_json_response($success, $message, $statusCode = 200) {
    http_response_code($statusCode);
    echo json_encode(['success' => $success, 'message' => $message]);
    exit;
}

$data = json_decode(file_get_contents('php://input'), true);

// 1. Validação de Entrada
if (!$data || empty($data['name']) || empty($data['email']) || empty($data['password'])) {
    send_json_response(false, 'Todos os campos são obrigatórios.', 400);
}

$name = trim($data['name']);
$email = $data['email'];
$password = $data['password'];

if (strlen($name) < 2) {
    send_json_response(false, 'O nome deve ter pelo menos 2 caracteres.', 400);
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    send_json_response(false, 'Formato de e-mail inválido.', 400);
}

// Validação de domínio de e-mail (removida)
// if (substr($email, -17) !== '@grupomysa.com.br') {
//     send_json_response(false, 'O e-mail deve pertencer ao domínio @grupomysa.com.br.', 400);
// }

if (strlen($password) < 8) {
    send_json_response(false, 'A senha deve ter pelo menos 8 caracteres.', 400);
}

// A validação de e-mail da Microsoft foi removida para permitir qualquer e-mail.

// 3. Lógica de Registro com Tratamento de Erros
try {
    $password_hash = password_hash($password, PASSWORD_DEFAULT);

    $stmt = $pdo->prepare("INSERT INTO users (name, email, password_hash) VALUES (:name, :email, :password_hash)");
    $stmt->bindParam(':name', $name, PDO::PARAM_STR);
    $stmt->bindParam(':email', $email, PDO::PARAM_STR);
    $stmt->bindParam(':password_hash', $password_hash, PDO::PARAM_STR);
    $stmt->execute();

    send_json_response(true, 'Usuário cadastrado com sucesso!', 201);

} catch (PDOException $e) {
    if ($e->errorInfo[1] == 1062) {
        send_json_response(false, 'Este e-mail já está em uso.', 409);
    } else {
        send_json_response(false, 'Ocorreu um erro no servidor ao tentar registrar.', 500);
    }
}
?>