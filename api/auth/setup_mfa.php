<?php
session_start();
require_once '../config/database.php';
require_once __DIR__ . '/../../vendor/autoload.php'; // Carrega o autoload do Composer

use GAuth\GAuth;

header('Content-Type: application/json');

// Função para enviar resposta JSON e sair
function send_json_response($success, $data, $statusCode = 200) {
    http_response_code($statusCode);
    echo json_encode(['success' => $success] + $data);
    exit;
}

// 1. Verifica se o usuário está logado e em processo de setup de MFA
if (!isset($_SESSION['user_id']) || !isset($_SESSION['mfa_pending'])) {
    send_json_response(false, ['message' => 'Acesso não autorizado.'], 401);
}

$user_id = $_SESSION['user_id'];

// 2. Lida com a requisição com base no método HTTP
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    // ---- GERAÇÃO DO QR CODE (GET) ----
    try {
        $stmt = $pdo->prepare("SELECT email FROM users WHERE id = :id");
        $stmt->bindParam(':id', $user_id, PDO::PARAM_INT);
        $stmt->execute();
        $user = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$user) {
            send_json_response(false, ['message' => 'Usuário não encontrado.'], 404);
        }

        // Gera um novo segredo MFA
        $gauth = new GAuth();
        $secret = $gauth->generateSecret();

        // Armazena o segredo temporariamente na sessão para verificação posterior
        $_SESSION['mfa_temp_secret'] = $secret;

        $issuer = 'AssetManager';
        $otpauth_url = $gauth->getURL($user['email'], $issuer, $secret);

        send_json_response(true, ['otpauth_url' => $otpauth_url]);

    } catch (Exception $e) {
        send_json_response(false, ['message' => 'Erro ao gerar o código QR.'], 500);
    }

} elseif ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // ---- VERIFICAÇÃO DO CÓDIGO (POST) ----
    $data = json_decode(file_get_contents('php://input'), true);
    $mfa_code = $data['mfa_code'] ?? '';
    $temp_secret = $_SESSION['mfa_temp_secret'] ?? null;

    if (empty($mfa_code) || !$temp_secret || !preg_match('/^[0-9]{6}$/', $mfa_code)) {
        send_json_response(false, ['message' => 'Código MFA inválido ou sessão expirada.'], 400);
    }

    try {
        // Verifica o código fornecido com o segredo temporário
        $gauth = new GAuth();
        if ($gauth->verifyCode($temp_secret, $mfa_code)) {
            // Sucesso! Salva o segredo permanente no banco de dados
            $stmt = $pdo->prepare("UPDATE users SET mfa_secret = :secret WHERE id = :id");
            $stmt->bindParam(':secret', $temp_secret, PDO::PARAM_STR);
            $stmt->bindParam(':id', $user_id, PDO::PARAM_INT);
            $stmt->execute();

            // Limpa as variáveis de sessão do processo de MFA
            unset($_SESSION['mfa_pending']);
            unset($_SESSION['mfa_temp_secret']);

            send_json_response(true, ['message' => 'MFA ativado com sucesso!']);
        } else {
            send_json_response(false, ['message' => 'Código de verificação incorreto.'], 401);
        }
    } catch (Exception $e) {
        send_json_response(false, ['message' => 'Erro no servidor ao verificar o código.'], 500);
    }
} else {
    send_json_response(false, ['message' => 'Método não permitido.'], 405);
}
?>