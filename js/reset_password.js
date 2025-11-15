document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('password-reset-form');
    const feedback = document.getElementById('password-update-feedback');
    const tokenField = document.getElementById('reset-token');

    if (!form) return;

    const token = AssetManager.getQueryParam('token');
    if (!token) {
        AssetManager.setFeedback(feedback, 'Token de redefinição ausente. Use o link enviado por e-mail.', 'error');
        form.querySelectorAll('input, button').forEach((el) => (el.disabled = true));
        return;
    }

    tokenField.value = token;

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const password = document.getElementById('new-password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        AssetManager.setFeedback(feedback, 'Atualizando senha...', 'info');

        try {
            const response = await AssetManager.request('auth/do_password_reset.php', {
                method: 'POST',
                data: {
                    token,
                    password,
                    confirm_password: confirmPassword,
                },
            });

            AssetManager.setFeedback(feedback, response?.message || 'Senha atualizada com sucesso!', 'success');
            AssetManager.showToast({ title: 'Senha redefinida', description: 'Você já pode fazer login novamente.' });

            window.setTimeout(() => {
                window.location.href = 'login.html';
            }, 1200);
        } catch (error) {
            AssetManager.setFeedback(feedback, error.message || 'Não foi possível redefinir a senha.', 'error');
        }
    });
});
