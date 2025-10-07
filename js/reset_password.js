document.addEventListener('DOMContentLoaded', () => {
    const resetPasswordForm = document.getElementById('reset-password-form');
    const tokenInput = document.getElementById('reset-token');

    // 1. Capturar o token da URL e colocá-lo no formulário
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');

    if (token) {
        tokenInput.value = token;
    } else {
        // Se não houver token, exibe um erro e desabilita o formulário
        showMessage('Token de recuperação não encontrado. Por favor, solicite um novo link.', false);
        resetPasswordForm.querySelector('button').disabled = true;
    }

    if (resetPasswordForm) {
        resetPasswordForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const newPassword = document.getElementById('new-password').value;
            const confirmPassword = document.getElementById('confirm-password').value;
            const currentToken = tokenInput.value;

            if (newPassword !== confirmPassword) {
                showMessage('As senhas não coincidem.', false);
                return;
            }

            if (newPassword.length < 8) {
                showMessage('A nova senha deve ter pelo menos 8 caracteres.', false);
                return;
            }

            try {
                const response = await fetch('../api/auth/do_password_reset.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        token: currentToken,
                        password: newPassword,
                        confirm_password: confirmPassword
                    })
                });

                const result = await response.json();
                showMessage(result.message, result.success);

                if (result.success) {
                    // Desabilita o formulário e redireciona para o login após um tempo
                    resetPasswordForm.querySelector('button').disabled = true;
                    setTimeout(() => {
                        window.location.href = 'login.html';
                    }, 3000);
                }

            } catch (error) {
                showMessage('Ocorreu um erro de conexão. Tente novamente.', false);
            }
        });
    }
});