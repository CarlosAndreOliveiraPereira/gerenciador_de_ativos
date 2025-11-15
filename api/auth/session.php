<?php

declare(strict_types=1);

require_once __DIR__ . '/../bootstrap.php';

if (!isset($_SESSION['user_id'], $_SESSION['user_name'])) {
    respond_error('Nenhuma sessão ativa.', 401);
}

respond([
    'success' => true,
    'data' => [
        'user_id' => (int) $_SESSION['user_id'],
        'user_name' => $_SESSION['user_name'],
    ],
]);
