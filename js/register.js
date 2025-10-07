document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');

    if (registerForm) {
        // Preenche o formulário se o usuário voltou para editar os dados
        const registrationData = JSON.parse(sessionStorage.getItem('registrationData'));
        if (registrationData) {
            document.getElementById('register-name').value = registrationData.name;
            document.getElementById('register-email').value = registrationData.email;
        }

        registerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('register-name').value;
            const email = document.getElementById('register-email').value;
            const password = document.getElementById('register-password').value;

            // Salva os dados na sessão e redireciona para a página de confirmação
            const data = { name, email, password };
            sessionStorage.setItem('registrationData', JSON.stringify(data));
            window.location.href = 'confirm-registration.html';
        });
    }
});