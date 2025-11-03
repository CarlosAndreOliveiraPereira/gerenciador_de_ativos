<?php
// Configurações de conexão com o banco de dados
$host = '127.0.0.1'; // Use 127.0.0.1 em vez de localhost
$dbname = 'asset_manager';
$user = 'root';
$pass = '';
$charset = 'utf8mb4';

// Opções do PDO para otimização e segurança
$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION, // Lança exceções em caso de erro
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,       // Retorna arrays associativos
    PDO::ATTR_EMULATE_PREPARES   => false,                  // Desabilita a emulação de prepared statements
];

// DSN (Data Source Name)
$dsn = "mysql:host=$host;dbname=$dbname;charset=$charset";

try {
    // Cria a instância do PDO
    $pdo = new PDO($dsn, $user, $pass, $options);
} catch (PDOException $e) {
    // Em caso de falha na conexão, exibe uma mensagem de erro genérica
    // Em um ambiente de produção, seria ideal logar o erro em vez de exibi-lo
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Falha na conexão com o banco de dados.']);
    // Log do erro (exemplo): error_log($e->getMessage());
    exit; // Interrompe a execução do script
}
?>