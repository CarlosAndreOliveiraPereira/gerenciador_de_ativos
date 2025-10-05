document.addEventListener('DOMContentLoaded', () => {
    const confirmationContainer = document.getElementById('confirmation-container');
    const messageDiv = document.getElementById('message');

    if (confirmationContainer) {
        const registrationData = JSON.parse(sessionStorage.getItem('registrationData'));

        // Se não houver dados na sessão, redireciona de volta para o registro
        if (!registrationData) {
            window.location.href = 'register.html';
            return;
        }

        // Exibe os dados para o usuário confirmar
        document.getElementById('confirm-name').textContent = registrationData.name;
        document.getElementById('confirm-email').textContent = registrationData.email;

        // Adiciona o listener para o botão de confirmar
        document.getElementById('confirm-button').addEventListener('click', async () => {
            try {
                const response = await fetch('../api/auth/register.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(registrationData)
                });
                const result = await response.json();

                if (messageDiv) {
                    messageDiv.textContent = result.message;
                    messageDiv.className = result.success ? 'success' : 'error';
                    messageDiv.style.display = 'block';
                }

                if (result.success) {
                    sessionStorage.removeItem('registrationData'); // Limpa os dados da sessão
                    setTimeout(() => {
                        window.location.href = 'login.html'; // Redireciona para login após sucesso
                    }, 2000);
                }
            } catch (error) {
                if (messageDiv) {
                    messageDiv.textContent = 'Ocorreu um erro de conexão. Tente novamente.';
                    messageDiv.className = 'error';
                    messageDiv.style.display = 'block';
                }
            }
        });
    }
});