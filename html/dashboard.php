<?php
session_start();
// Se o usuário não estiver logado, redireciona para a página de login
if (!isset($_SESSION['user_id'])) {
    header('Location: login.php');
    exit;
}
include 'templates/app_header.php';
?>
<title>AssetManager - Dashboard</title>
<link rel="stylesheet" href="../css/dashboard.css">

<div class="container">
    <div class="dashboard-header">
        <h1>Dashboard de Máquinas</h1>
        <div class="toolbar">
            <input type="search" id="search-bar" placeholder="Buscar por nome, localidade...">
            <a href="add-machine.html" class="btn-add-machine">Adicionar Máquina</a>
            <a href="../api/auth/logout.php" class="btn-logout">Sair</a>
        </div>
    </div>
    <div id="machines-container">
        <!-- As máquinas serão carregadas aqui -->
    </div>
    <div id="message"></div>
</div>
<script src="../js/utils.js"></script>
<script src="../js/dashboard.js"></script>
</body>
</html>