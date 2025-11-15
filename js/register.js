document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('register-form');
    const feedback = document.getElementById('register-feedback');

    if (!form) return;

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const name = document.getElementById('register-name').value.trim();
        const email = document.getElementById('register-email').value.trim();
        const password = document.getElementById('register-password').value;

        AssetManager.setFeedback(feedback, 'Criando sua conta...', 'info');

        try {
            const response = await AssetManager.request('auth/register.php', {
                method: 'POST',
                data: { name, email, password },
            });

            AssetManager.setFeedback(feedback, response?.message || 'Conta criada com sucesso!', 'success');
            AssetManager.showToast({
                title: 'Cadastro concluído!',
                description: 'Agora é só acessar com seu e-mail e senha.',
            });

            window.setTimeout(() => {
                window.location.href = 'login.html';
            }, 900);
        } catch (error) {
            AssetManager.setFeedback(feedback, error.message || 'Não foi possível concluir o cadastro.', 'error');
        }
    });
});
