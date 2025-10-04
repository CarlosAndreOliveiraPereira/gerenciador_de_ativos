document.addEventListener('DOMContentLoaded', () => {
    const messageDiv = document.getElementById('message');

    // --- Lógica de Registro (Etapa 1: Captura e Armazenamento) ---
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        // Preenche o formulário se o usuário voltou para editar
        const registrationData = JSON.parse(sessionStorage.getItem('registrationData'));
        if (registrationData) {
            document.getElementById('register-name').value = registrationData.name;
            document.getElementById('register-email').value = registrationData.email;
        }

        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('register-name').value;
            const email = document.getElementById('register-email').value;
            const password = document.getElementById('register-password').value;

            // Salva os dados na sessão e redireciona para confirmação
            const data = { name, email, password };
            sessionStorage.setItem('registrationData', JSON.stringify(data));
            window.location.href = 'confirm-registration.html';
        });
    }

    // --- Lógica de Confirmação de Cadastro (Etapa 2: Exibição e Envio) ---
    const confirmationContainer = document.getElementById('confirmation-container');
    if (confirmationContainer) {
        const registrationData = JSON.parse(sessionStorage.getItem('registrationData'));

        if (!registrationData) {
            // Se não houver dados, volta para a página de registro
            window.location.href = 'register.html';
            return;
        }

        // Exibe os dados para o usuário
        document.getElementById('confirm-name').textContent = registrationData.name;
        document.getElementById('confirm-email').textContent = registrationData.email;

        // Lógica do botão de confirmar
        document.getElementById('confirm-button').addEventListener('click', async () => {
            const response = await fetch('../api/auth/register.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(registrationData)
            });
            const result = await response.json();

            if (messageDiv) {
                messageDiv.textContent = result.message;
                messageDiv.className = result.success ? 'success' : 'error';
            }

            if (result.success) {
                sessionStorage.removeItem('registrationData'); // Limpa os dados da sessão
                setTimeout(() => {
                    window.location.href = 'login.html'; // Redireciona para login
                }, 1500);
            }
        });
    }

    // --- Lógica de Login ---
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;

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
                }
            }
        });
    }
});