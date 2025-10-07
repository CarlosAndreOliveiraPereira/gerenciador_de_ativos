document.addEventListener('DOMContentLoaded', () => {
    const confirmationContainer = document.getElementById('confirmation-container');

    if (confirmationContainer) {
        const registrationData = JSON.parse(sessionStorage.getItem('registrationData'));

        if (!registrationData) {
            window.location.href = 'register.html';
            return;
        }

        document.getElementById('confirm-name').textContent = registrationData.name;
        document.getElementById('confirm-email').textContent = registrationData.email;

        document.getElementById('confirm-button').addEventListener('click', async () => {
            try {
                const response = await fetch('../api/auth/register.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(registrationData)
                });
                const result = await response.json();

                showMessage(result.message, result.success);

                if (result.success) {
                    sessionStorage.removeItem('registrationData');
                    setTimeout(() => {
                        window.location.href = 'login.html';
                    }, 2000);
                }
            } catch (error) {
                showMessage('Ocorreu um erro de conexão. Tente novamente.', false);
            }
        });
    }
});