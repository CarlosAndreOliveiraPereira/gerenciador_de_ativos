function showMessage(message, isSuccess) {
    const messageElement = document.getElementById('message');
    if (messageElement) {
        messageElement.textContent = message;
        messageElement.className = isSuccess ? 'message success' : 'message error';

        // Limpa a mensagem após alguns segundos
        setTimeout(() => {
            messageElement.textContent = '';
            messageElement.className = 'message';
        }, 3000);
    }
}
