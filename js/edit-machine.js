document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('edit-machine-form');
    const feedback = document.getElementById('edit-feedback');
    const deleteButton = document.getElementById('delete-button');
    const backLink = document.getElementById('back-to-detail');

    if (!form) return;

    const machineId = AssetManager.getQueryParam('id');
    if (!machineId) {
        AssetManager.setFeedback(feedback, 'ID do ativo não informado.', 'error');
        form.querySelectorAll('input, textarea, select, button').forEach((el) => {
            el.disabled = true;
        });
        return;
    }

    backLink?.setAttribute('href', `machine.html?id=${encodeURIComponent(machineId)}`);
    document.getElementById('machine-id').value = machineId;

    async function loadMachine() {
        try {
            const response = await AssetManager.request(`machines/get.php?id=${encodeURIComponent(machineId)}`);
            if (!response?.data) {
                throw new Error('Ativo não encontrado.');
            }
            const machine = response.data;
            form.localidade.value = machine.localidade ?? '';
            form.nome_dispositivo.value = machine.nome_dispositivo ?? '';
            form.numero_serie.value = machine.numero_serie ?? '';
            form.nota_fiscal.value = machine.nota_fiscal ?? '';
            form.responsavel.value = machine.responsavel ?? '';
            form.email_responsavel.value = machine.email_responsavel ?? '';
            form.setor.value = machine.setor ?? '';
            form.windows_update_ativo.value = machine.windows_update_ativo ?? 'Sim';
            form.sistema_operacional.value = machine.sistema_operacional ?? '';
            form.observacao.value = machine.observacao ?? '';
        } catch (error) {
            AssetManager.setFeedback(feedback, error.message || 'Não foi possível carregar o ativo.', 'error');
            if (error.status === 401) {
                window.location.href = 'login.html';
            }
        }
    }

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const data = {
            id: machineId,
            localidade: form.localidade.value.trim(),
            nome_dispositivo: form.nome_dispositivo.value.trim(),
            numero_serie: form.numero_serie.value.trim(),
            nota_fiscal: form.nota_fiscal.value.trim(),
            responsavel: form.responsavel.value.trim(),
            email_responsavel: form.email_responsavel.value.trim(),
            setor: form.setor.value.trim(),
            windows_update_ativo: form.windows_update_ativo.value,
            sistema_operacional: form.sistema_operacional.value.trim(),
            observacao: form.observacao.value.trim(),
        };

        AssetManager.setFeedback(feedback, 'Salvando alterações...', 'info');

        try {
            const response = await AssetManager.request('machines/update.php', {
                method: 'POST',
                data,
            });
            AssetManager.setFeedback(feedback, response?.message || 'Dados atualizados!', 'success');
            AssetManager.showToast({ title: 'Ativo atualizado' });
        } catch (error) {
            if (error.status === 401) {
                window.location.href = 'login.html';
                return;
            }
            AssetManager.setFeedback(feedback, error.message || 'Não foi possível atualizar o ativo.', 'error');
        }
    });

    deleteButton?.addEventListener('click', async () => {
        if (!window.confirm('Tem certeza que deseja excluir este ativo? Essa ação não pode ser desfeita.')) {
            return;
        }

        AssetManager.setFeedback(feedback, 'Excluindo ativo...', 'info');

        try {
            const response = await AssetManager.request('machines/delete.php', {
                method: 'POST',
                data: { id: machineId },
            });
            AssetManager.showToast({ title: 'Ativo removido', description: response?.message });
            window.location.href = 'dashboard.html';
        } catch (error) {
            if (error.status === 401) {
                window.location.href = 'login.html';
                return;
            }
            AssetManager.setFeedback(feedback, error.message || 'Erro ao remover o ativo.', 'error');
        }
    });

    loadMachine();
});
