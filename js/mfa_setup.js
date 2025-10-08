document.addEventListener('DOMContentLoaded', () => {
    const qrCodeContainer = document.getElementById('qrcode');
    const verifyForm = document.getElementById('mfa-verify-form');
    const messageContainer = document.getElementById('message');

    // Função para exibir mensagens (pode ser movida para um utils.js)
    const showMessage = (message, isSuccess) => {
        messageContainer.textContent = message;
        messageContainer.className = isSuccess ? 'message success' : 'message error';
    };

    // 1. Buscar o QR Code do backend ao carregar a página
    const fetchQrCode = async () => {
        try {
            const response = await fetch('../api/auth/setup_mfa.php', { method: 'GET' });
            const result = await response.json();

            if (result.success && result.otpauth_url) {
                qrCodeContainer.innerHTML = ''; // Limpa qualquer conteúdo anterior
                new QRCode(qrCodeContainer, {
                    text: result.otpauth_url,
                    width: 200,
                    height: 200,
                    colorDark: "#000000",
                    colorLight: "#ffffff",
                    correctLevel: QRCode.CorrectLevel.H
                });
            } else {
                showMessage(result.message || 'Não foi possível carregar o QR Code.', false);
            }
        } catch (error) {
            showMessage('Erro de conexão ao buscar o QR Code.', false);
        }
    };

    // 2. Lidar com a submissão do formulário de verificação
    if (verifyForm) {
        verifyForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const mfaCode = document.getElementById('mfa-code').value;

            if (!mfaCode || !/^[0-9]{6}$/.test(mfaCode)) {
                showMessage('Por favor, insira um código de 6 dígitos válido.', false);
                return;
            }

            try {
                const response = await fetch('../api/auth/setup_mfa.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ mfa_code: mfaCode })
                });

                const result = await response.json();

                if (result.success) {
                    showMessage('MFA ativado com sucesso! Redirecionando para o dashboard...', true);
                    setTimeout(() => {
                        window.location.href = 'dashboard.html';
                    }, 2000);
                } else {
                    showMessage(result.message || 'Ocorreu um erro ao verificar o código.', false);
                }
            } catch (error) {
                showMessage('Erro de conexão ao verificar o código.', false);
            }
        });
    }

    // Inicia o processo
    fetchQrCode();
});