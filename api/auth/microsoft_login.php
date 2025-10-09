<?php
session_start();
require_once '../config/database.php';

// Ponto de entrada para o login com Microsoft
$authorization_endpoint = 'https://login.microsoftonline.com/' . MICROSOFT_TENANT_ID . '/oauth2/v2.0/authorize';

// Parâmetros para a requisição de autorização
$params = [
    'client_id' => MICROSOFT_CLIENT_ID,
    'redirect_uri' => MICROSOFT_REDIRECT_URI,
    'response_type' => 'code',
    'scope' => 'openid profile email User.Read', // Escopos necessários para obter informações do usuário
    'response_mode' => 'query',
];

// Gera um 'state' aleatório para mitigar ataques CSRF
$_SESSION['oauth2state'] = bin2hex(random_bytes(16));
$params['state'] = $_SESSION['oauth2state'];

// Constrói a URL de autorização e redireciona o usuário
$auth_url = $authorization_endpoint . '?' . http_build_query($params);
header('Location: ' . $auth_url);
exit();
?>