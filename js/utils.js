/**
 * Exibe uma mensagem para o usuário.
 * @param {string} msg - A mensagem a ser exibida.
 * @param {boolean} isSuccess - Define se a mensagem é de sucesso (true) ou erro (false).
 * @param {string} elementId - O ID do elemento onde a mensagem será exibida (padrão: 'message').
 */
function showMessage(msg, isSuccess, elementId = 'message') {
    const messageDiv = document.getElementById(elementId);
    if (messageDiv) {
        messageDiv.textContent = msg;
        messageDiv.className = isSuccess ? 'success' : 'error';
        messageDiv.style.display = 'block';
    }
}