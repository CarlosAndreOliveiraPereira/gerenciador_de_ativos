<?php
session_start();
require_once '../config/database.php';

header('Content-Type: application/json');

function send_json_response($success, $message, $data = null) {
    $response = ['success' => $success, 'message' => $message];
    if ($data) {
        $response['data'] = $data;
    }
    echo json_encode($response);
    exit;
}

$data = json_decode(file_get_contents('php://input'), true);

if (!$data || empty($data['email']) || empty($data['password'])) {
    http_response_code(400);
    send_json_response(false, 'E-mail e senha são obrigatórios.');
}

$email = $data['email'];
$password = $data['password'];

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    send_json_response(false, 'Formato de e-mail inválido.');
}

try {
    $stmt = $pdo->prepare("SELECT id, name, password_hash FROM users WHERE email = :email");
    $stmt->bindParam(':email', $email);
    $stmt->execute();

    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($user && password_verify($password, $user['password_hash'])) {
        // Regenera o ID da sessão para evitar fixação de sessão
        session_regenerate_id(true);

        $_SESSION['user_id'] = $user['id'];
        $_SESSION['user_name'] = $user['name'];

        send_json_response(true, 'Login bem-sucedido!');
    } else {
        http_response_code(401);
        send_json_response(false, 'E-mail ou senha inválidos.');
    }

} catch (PDOException $e) {
    http_response_code(500);
    send_json_response(false, 'Erro no servidor. Tente novamente mais tarde.');
}
?>