document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('add-machine-form');
    const feedback = document.getElementById('machine-feedback');

    if (!form) return;

    AssetManager.request('auth/session.php').catch(() => {
        window.location.href = 'login.html';
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const data = {
            localidade: document.getElementById('localidade').value.trim(),
            nome_dispositivo: document.getElementById('nome_dispositivo').value.trim(),
            numero_serie: document.getElementById('numero_serie').value.trim(),
            nota_fiscal: document.getElementById('nota_fiscal').value.trim(),
            responsavel: document.getElementById('responsavel').value.trim(),
            email_responsavel: document.getElementById('email_responsavel').value.trim(),
            setor: document.getElementById('setor').value.trim(),
            windows_update_ativo: document.getElementById('windows_update_ativo').value,
            sistema_operacional: document.getElementById('sistema_operacional').value.trim(),
            observacao: document.getElementById('observacao').value.trim(),
        };

        AssetManager.setFeedback(feedback, 'Salvando ativo...', 'info');

        try {
            const response = await AssetManager.request('machines/create.php', {
                method: 'POST',
                data,
            });

            AssetManager.setFeedback(feedback, response?.message || 'Ativo cadastrado!', 'success');
            AssetManager.showToast({
                title: 'Cadastro realizado',
                description: 'O ativo foi adicionado ao inventário.',
            });

            form.reset();
            document.getElementById('windows_update_ativo').selectedIndex = 0;
        } catch (error) {
            if (error.status === 401) {
                window.location.href = 'login.html';
                return;
            }
            AssetManager.setFeedback(feedback, error.message || 'Erro ao salvar ativo.', 'error');
        }
    });
});
