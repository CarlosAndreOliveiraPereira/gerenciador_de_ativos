<?php include 'templates/header.php'; ?>
<title>AssetManager - Redefinir Senha</title>
<link rel="stylesheet" href="../css/login.css">

<div class="container">
    <h1>Redefinir Senha</h1>
    <form id="reset-password-form">
        <input type="password" id="new-password" placeholder="Nova Senha" required>
        <input type="password" id="confirm-password" placeholder="Confirmar Nova Senha" required>
        <button type="submit">Redefinir Senha</button>
    </form>
    <div id="message"></div>
</div>
<script src="../js/utils.js"></script>
<script src="../js/reset_password.js"></script>
</body>
</html>