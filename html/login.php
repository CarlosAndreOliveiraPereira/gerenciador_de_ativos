<?php include 'templates/header.php'; ?>
<title>AssetManager - Login</title>
<link rel="stylesheet" href="../css/login.css">

<div class="container">
    <div id="login-form-container">
        <h1>Login</h1>
        <form id="login-form">
            <input type="email" id="login-email" placeholder="E-mail" required>
            <input type="password" id="login-password" placeholder="Senha" required>
            <button type="submit">Entrar</button>
        </form>
        <p>Não tem uma conta? <a href="register.php">Cadastre-se</a></p>
        <p class="forgot-password"><a href="request_password_reset.html">Esqueci minha senha</a></p>
    </div>
    <div id="message"></div>
</div>
<script src="../js/utils.js"></script>
<script src="../js/login.js"></script>
</body>
</html>