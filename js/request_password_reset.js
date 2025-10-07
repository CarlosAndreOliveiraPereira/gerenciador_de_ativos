document.addEventListener('DOMContentLoaded', () => {
    const requestResetForm = document.getElementById('request-reset-form');

    if (requestResetForm) {
        requestResetForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const submitButton = requestResetForm.querySelector('button[type="submit"]');

            if (!email) {
                showMessage('Por favor, insira um endereço de e-mail.', false);
                return;
            }

            // Desabilitar o botão para evitar múltiplos envios
            submitButton.disabled = true;
            submitButton.textContent = 'Enviando...';

            try {
                const response = await fetch('../api/auth/request_password_reset.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: email })
                });

                const result = await response.json();

                // Exibe a mensagem da API, seja de sucesso ou erro.
                // A mensagem de sucesso incluirá o link de teste.
                showMessage(result.message, result.success);

            } catch (error) {
                showMessage('Ocorreu um erro de conexão. Tente novamente.', false);
            } finally {
                // Reabilita o botão após a conclusão
                submitButton.disabled = false;
                submitButton.textContent = 'Enviar Link de Recuperação';
            }
        });
    }
});