document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('login-form');
    const feedback = document.getElementById('login-feedback');
    const emailInput = document.getElementById('login-email');
    const rememberBox = document.getElementById('remember-me');

    if (!form) return;

    const rememberedEmail = window.localStorage.getItem('assetmanager:remembered-email');
    if (rememberedEmail) {
        emailInput.value = rememberedEmail;
        rememberBox.checked = true;
    }

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const email = emailInput.value.trim();
        const password = document.getElementById('login-password').value;

        AssetManager.setFeedback(feedback, 'Autenticando...', 'info');

        try {
            const response = await AssetManager.request('auth/login.php', {
                method: 'POST',
                data: { email, password },
            });

            if (rememberBox.checked) {
                window.localStorage.setItem('assetmanager:remembered-email', email);
            } else {
                window.localStorage.removeItem('assetmanager:remembered-email');
            }

            AssetManager.setFeedback(feedback, 'Login realizado com sucesso!', 'success');
            AssetManager.showToast({ title: 'Bem-vindo!', description: response?.message || 'Sessão iniciada.' });

            window.setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 600);
        } catch (error) {
            AssetManager.setFeedback(feedback, error.message || 'Falha ao entrar.', 'error');
        }
    });
});
