const loginFormContainer = document.getElementById('login-form-container');
const registerFormContainer = document.getElementById('register-form-container');
const messageDiv = document.getElementById('message');

function toggleForms() {
    loginFormContainer.style.display = loginFormContainer.style.display === 'none' ? 'block' : 'none';
    registerFormContainer.style.display = registerFormContainer.style.display === 'none' ? 'block' : 'none';
    messageDiv.textContent = '';
}

// Lógica de Registro
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('register-name').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;

    const response = await fetch('api/auth/register.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password })
    });
    const result = await response.json();

    messageDiv.textContent = result.message;
    messageDiv.className = result.success ? 'success' : 'error';
    if (result.success) {
        setTimeout(toggleForms, 1500); // Volta para tela de login após sucesso
    }
});

// Lógica de Login
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    const response = await fetch('api/auth/login.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    const result = await response.json();

    if (result.success) {
        window.location.href = 'dashboard.html'; // Redireciona para o dashboard
    } else {
        messageDiv.textContent = result.message;
        messageDiv.className = 'error';
    }
});