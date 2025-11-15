<?php

declare(strict_types=1);

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

header('Content-Type: application/json; charset=utf-8');

require_once __DIR__ . '/config/database.php';

function respond(array $payload, int $status = 200): never
{
    http_response_code($status);
    echo json_encode($payload, JSON_UNESCAPED_UNICODE);
    exit;
}

function respond_success(string $message = '', array $extra = []): never
{
    $payload = ['success' => true];
    if ($message !== '') {
        $payload['message'] = $message;
    }
    foreach ($extra as $key => $value) {
        $payload[$key] = $value;
    }
    respond($payload);
}

function respond_error(string $message, int $status = 400, array $extra = []): never
{
    $payload = array_merge(['success' => false, 'message' => $message], $extra);
    respond($payload, $status);
}

function request_body(): array
{
    $input = file_get_contents('php://input');
    if ($input === false || trim($input) === '') {
        return [];
    }

    try {
        $decoded = json_decode($input, true, 512, JSON_THROW_ON_ERROR);
    } catch (Throwable $exception) {
        respond_error('Formato de corpo inválido. Envie um JSON válido.', 400);
    }

    return is_array($decoded) ? $decoded : [];
}

function require_auth(): int
{
    if (!isset($_SESSION['user_id'])) {
        respond_error('Acesso não autorizado.', 401);
    }

    return (int) $_SESSION['user_id'];
}

function sanitize_like(string $term): string
{
    $term = str_replace(['%', '_'], ['\\%', '\\_'], $term);
    return "%$term%";
}

$pdo = create_pdo();
