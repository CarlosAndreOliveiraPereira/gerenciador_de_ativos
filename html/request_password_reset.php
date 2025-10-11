<?php include 'templates/header.php'; ?>
<title>AssetManager - Recuperar Senha</title>
<link rel="stylesheet" href="../css/login.css">

<div class="container">
    <h1>Recuperar Senha</h1>
    <p>Insira seu e-mail para receber as instruções de recuperação de senha.</p>
    <form id="request-reset-form">
        <input type="email" id="reset-email" placeholder="Seu e-mail de cadastro" required>
        <button type="submit">Enviar</button>
    </form>
    <p>Lembrou a senha? <a href="login.php">Faça login</a></p>
    <div id="message"></div>
</div>
<script src="../js/utils.js"></script>
<script src="../js/request_password_reset.js"></script>
</body>
</html>