document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

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

                // A chave para o novo fluxo de MFA
                if (result.success && result.mfa_required) {
                    // Exibe a mensagem (que contém o código para teste)
                    showMessage(result.message, true);
                    // Redireciona para a página de verificação de MFA
                    setTimeout(() => {
                        window.location.href = 'mfa.html';
                    }, 2000);
                } else if (result.success) {
                    // Fallback para o caso de o MFA não ser acionado (não deve acontecer)
                    window.location.href = 'dashboard.html';
                }
                else {
                    showMessage(result.message, false);
                }
            } catch (error) {
                showMessage('Ocorreu um erro de conexão. Tente novamente.', false);
            }
        });
    }
});