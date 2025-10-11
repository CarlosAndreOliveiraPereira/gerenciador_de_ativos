<?php include 'templates/header.php'; ?>
<title>AssetManager - Confirmar Cadastro</title>
<link rel="stylesheet" href="../css/login.css">

<div class="container" id="confirmation-container">
    <h1>Confirme seus Dados</h1>
    <p>Por favor, verifique se os dados abaixo estão corretos antes de finalizar o cadastro.</p>

    <div class="confirmation-details">
        <p><strong>Nome:</strong> <span id="confirm-name"></span></p>
        <p><strong>E-mail:</strong> <span id="confirm-email"></span></p>
    </div>

    <div class="confirmation-buttons">
        <button id="edit-button" onclick="window.location.href='register.php'">Editar</button>
        <button id="confirm-button">Confirmar e Cadastrar</button>
    </div>
    <div id="message"></div>
</div>
<script src="../js/utils.js"></script>
<script src="../js/confirmation.js"></script>
</body>
</html>