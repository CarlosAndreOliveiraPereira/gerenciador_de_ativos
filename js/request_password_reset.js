document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('password-reset-request-form');
    const feedback = document.getElementById('password-reset-feedback');

    if (!form) return;

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const email = document.getElementById('password-reset-email').value.trim();

        AssetManager.setFeedback(feedback, 'Enviando instruções...', 'info');

        try {
            const response = await AssetManager.request('auth/request_password_reset.php', {
                method: 'POST',
                data: { email },
            });
            AssetManager.setFeedback(feedback, response?.message || 'Se existir, enviaremos o link por e-mail.', 'success');
            AssetManager.showToast({ title: 'Verifique seu e-mail', description: 'Uma mensagem foi enviada com as instruções.' });
        } catch (error) {
            AssetManager.setFeedback(feedback, error.message || 'Não foi possível enviar o e-mail.', 'error');
        }
    });
});
