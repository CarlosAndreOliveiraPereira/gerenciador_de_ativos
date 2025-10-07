document.addEventListener('DOMContentLoaded', () => {
    const mfaForm = document.getElementById('mfa-form');

    if (mfaForm) {
        mfaForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const mfaCode = document.getElementById('mfa-code').value;

            if (!mfaCode || !/^[0-9]{6}$/.test(mfaCode)) {
                showMessage('Por favor, insira um código de 6 dígitos.', false);
                return;
            }

            try {
                const response = await fetch('../api/auth/verify_mfa.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ mfa_code: mfaCode })
                });

                const result = await response.json();

                if (result.success) {
                    showMessage('Login verificado com sucesso! Redirecionando...', true);
                    setTimeout(() => {
                        window.location.href = 'dashboard.html';
                    }, 1500);
                } else {
                    showMessage(result.message || 'Ocorreu um erro.', false);
                }
            } catch (error) {
                showMessage('Ocorreu um erro de conexão. Tente novamente.', false);
            }
        });
    }
});