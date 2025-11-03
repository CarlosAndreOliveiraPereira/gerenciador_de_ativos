document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const name = document.getElementById('register-name').value;
            const email = document.getElementById('register-email').value;
            const password = document.getElementById('register-password').value;

            // Validação básica no lado do cliente
            if (name.length < 2 || !email || password.length < 8) {
                showMessage('Por favor, preencha todos os campos corretamente.', false);
                return;
            }

            const data = { name, email, password };

            try {
                const response = await fetch('../api/auth/register.php', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (result.success) {
                    showMessage(result.message, true);
                    // Limpa o formulário e redireciona após um curto período
                    registerForm.reset();
                    setTimeout(() => {
                        window.location.href = 'login.html';
                    }, 2000);
                } else {
                    showMessage(result.message, false);
                }

            } catch (error) {
                showMessage('Ocorreu um erro de conexão. Tente novamente mais tarde.', false);
            }
        });
    }
});