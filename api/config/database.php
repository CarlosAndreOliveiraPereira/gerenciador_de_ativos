<?php

declare(strict_types=1);

function assetmanager_connection_settings(): array
{
    return [
        'host' => '127.0.0.1',
        'dbname' => 'asset_manager',
        'user' => 'root',
        'pass' => '',
        'charset' => 'utf8mb4',
    ];
}

function create_pdo(): PDO
{
    static $pdo = null;

    if ($pdo instanceof PDO) {
        return $pdo;
    }

    $settings = assetmanager_connection_settings();
    $dsn = sprintf('mysql:host=%s;dbname=%s;charset=%s', $settings['host'], $settings['dbname'], $settings['charset']);

    $options = [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
    ];

    try {
        $pdo = new PDO($dsn, $settings['user'], $settings['pass'], $options);
    } catch (PDOException $exception) {
        http_response_code(500);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode([
            'success' => false,
            'message' => 'Falha ao conectar ao banco de dados.',
        ], JSON_UNESCAPED_UNICODE);
        exit;
    }

    return $pdo;
}
