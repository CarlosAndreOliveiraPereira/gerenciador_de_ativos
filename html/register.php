<?php include 'templates/header.php'; ?>
<title>AssetManager - Cadastro</title>
<link rel="stylesheet" href="../css/login.css">

<div class="container">
    <h1>Cadastro de Usuário</h1>
    <form id="register-form">
        <input type="text" id="register-name" placeholder="Nome Completo" required>
        <input type="email" id="register-email" placeholder="E-mail" required>
        <input type="password" id="register-password" placeholder="Senha (mínimo 8 caracteres)" required>
        <button type="submit">Avançar</button>
    </form>
    <p>Já tem uma conta? <a href="login.php">Faça login</a></p>
    <div id="message"></div>
</div>
<script src="../js/utils.js"></script>
<script src="../js/register.js"></script>
</body>
</html>