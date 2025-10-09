<?php
// Mude estas credenciais para as do seu ambiente
define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', ''); // No XAMPP, a senha padrão é vazia
define('DB_NAME', 'asset_manager');

try {
    $pdo = new PDO("mysql:host=" . DB_HOST . ";dbname=" . DB_NAME, DB_USER, DB_PASS);
    // Configura o PDO para lançar exceções em caso de erro
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    // Em caso de falha na conexão, encerra o script e exibe o erro
    die("ERRO: Não foi possível conectar. " . $e->getMessage());
}
?>