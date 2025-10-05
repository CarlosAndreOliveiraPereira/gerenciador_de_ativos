document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const messageDiv = document.getElementById('message');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;

            try {
                const response = await fetch('../api/auth/login.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                const result = await response.json();

                if (result.success) {
                    window.location.href = 'dashboard.html'; // Redireciona para o dashboard
                } else {
                    if (messageDiv) {
                        messageDiv.textContent = result.message;
                        messageDiv.className = 'error';
                        messageDiv.style.display = 'block';
                    }
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