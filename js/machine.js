document.addEventListener('DOMContentLoaded', () => {
codex/improve-code-for-professional-and-interactive-design-9coivc
    const machineId = AssetManager.getQueryParam('id');
    const nameElement = document.getElementById('machine-name');
    const sectorElement = document.getElementById('machine-sector');
    const locationElement = document.getElementById('machine-location');
    const ownerElement = document.getElementById('machine-owner');
    const ownerEmailElement = document.getElementById('machine-owner-email');
    const serialElement = document.getElementById('machine-serial');
    const invoiceElement = document.getElementById('machine-invoice');
    const windowsUpdateElement = document.getElementById('machine-windows-update');
    const osElement = document.getElementById('machine-os');
    const notesElement = document.getElementById('machine-notes');
    const updatedElement = document.getElementById('machine-updated');
    const editButton = document.getElementById('edit-machine-button');
    const copyButton = document.getElementById('copy-summary');
=======
    const machineDetails = document.getElementById('machine-details');
    const userNameElement = document.getElementById('user-name');
    const logoutButton = document.getElementById('logout-button');
    const machineNameElement = document.getElementById('machine-name');
    const machineSectorElement = document.getElementById('machine-sector');
    const machineLocationElement = document.getElementById('machine-location');
    const machineResponsibleElement = document.getElementById('machine-responsible');
    const machineEmailButton = document.getElementById('machine-email');
    const overviewGrid = document.getElementById('overview-grid');
    const technicalGrid = document.getElementById('technical-grid');
    const machineNotesElement = document.getElementById('machine-notes');
    const toastElement = document.getElementById('toast');
    const machineAvatarElement = document.getElementById('machine-avatar');
    const refreshNotesButton = document.getElementById('refresh-notes');
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    if (!machineId) {
        nameElement.textContent = 'Ativo não encontrado';
        notesElement.textContent = 'O identificador do ativo não foi informado.';
        editButton?.setAttribute('disabled', 'true');
        copyButton?.setAttribute('disabled', 'true');
        return;
    }

 codex/improve-code-for-professional-and-interactive-design-9coivc
    editButton?.addEventListener('click', () => {
        window.location.href = `edit-machine.html?id=${encodeURIComponent(machineId)}`;
    });

    const visualThemes = [
        {
            gradient: 'linear-gradient(135deg, rgba(255, 193, 7, 0.35), rgba(255, 152, 0, 0.1))',
            cardBg: 'rgba(255, 255, 255, 0.04)',
            border: 'rgba(255, 193, 7, 0.18)'
        },
        {
            gradient: 'linear-gradient(135deg, rgba(3, 218, 198, 0.35), rgba(0, 150, 136, 0.12))',
            cardBg: 'rgba(0, 0, 0, 0.32)',
            border: 'rgba(3, 218, 198, 0.18)'
        },
        {
            gradient: 'linear-gradient(135deg, rgba(103, 58, 183, 0.35), rgba(63, 81, 181, 0.12))',
            cardBg: 'rgba(15, 15, 30, 0.42)',
            border: 'rgba(126, 87, 194, 0.22)'
        }
    ];
    let themeIndex = 0;
    applyVisualTheme(themeIndex);

    if (machineAvatarElement && !machineAvatarElement.dataset.initial) {
        machineAvatarElement.setAttribute('data-initial', 'A');
    }

    function applyVisualTheme(index) {
        const theme = visualThemes[index % visualThemes.length];
        document.documentElement.style.setProperty('--machine-hero-gradient', theme.gradient);
        document.documentElement.style.setProperty('--machine-card-bg', theme.cardBg);
        document.documentElement.style.setProperty('--machine-card-border', theme.border);
    }

    function getInitials(value) {
        if (!value) {
            return 'A';
        }
        const cleanValue = value.toString().trim();
        if (!cleanValue) {
            return 'A';
        }
        const [firstWord = ''] = cleanValue.split(/\s+/);
        return firstWord.charAt(0).toUpperCase();
    }

    function showToast(message) {
        if (!toastElement) {
            return;
        }
        toastElement.textContent = message;
        toastElement.classList.add('visible');
        setTimeout(() => {
            toastElement.classList.remove('visible');
        }, 2200);
    }

    function copyToClipboard(value, label) {
        if (!value) {
            showToast('Nada para copiar.');
            return;
        }

        const text = value.toString().trim();
        if (!text) {
            showToast('Nada para copiar.');
            return;
        }

        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard
                .writeText(text)
                .then(() => showToast(`${label} copiado`))
                .catch(() => fallbackCopy(text, label));
        } else {
            fallbackCopy(text, label);
        }
    }

    function fallbackCopy(text, label) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.setAttribute('readonly', '');
        textarea.style.position = 'absolute';
        textarea.style.left = '-9999px';
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            showToast(`${label} copiado`);
        } catch (error) {
            showToast('Não foi possível copiar.');
        } finally {
            document.body.removeChild(textarea);
        }
    }

    function clearGrid(grid) {
        if (grid) {
            grid.innerHTML = '';
        }
    }

    function createInfoCard({ label, value, hint = 'Clique para copiar' }) {
        const hasValue = Boolean(value && value.toString().trim());
        const card = document.createElement('button');
        card.type = 'button';
        card.className = 'info-card';
        card.innerHTML = `
            <span class="info-label">${label}</span>
            <span class="info-value">${hasValue ? value : 'Não informado'}</span>
            <span class="info-hint">${hint}</span>
        `;

        if (!hasValue) {
            card.classList.add('disabled');
            card.setAttribute('aria-disabled', 'true');
            card.disabled = true;
            const hintElement = card.querySelector('.info-hint');
            if (hintElement) {
                hintElement.textContent = 'Não disponível';
            }
        } else {
            card.addEventListener('click', () => copyToClipboard(value, label));
        }

        return card;
    }

    function populateGrid(grid, items) {
        if (!grid) {
            return;
        }
        clearGrid(grid);
        items.forEach((item) => {
            grid.appendChild(createInfoCard(item));
        });
    }

    function updateHero(machine) {
        const deviceName = machine.nome_dispositivo || 'Ativo sem nome';
        if (machineNameElement) {
            machineNameElement.textContent = deviceName;
        }
        if (machineSectorElement) {
            machineSectorElement.textContent = machine.setor || 'Setor não informado';
        }
        if (machineLocationElement) {
            machineLocationElement.textContent = machine.localidade
                ? `Localizado em ${machine.localidade}`
                : 'Localidade não informada';
        }
        if (machineResponsibleElement) {
            machineResponsibleElement.textContent = machine.responsavel || 'Não informado';
        }

        const email = machine.email_responsavel || '';
        if (machineEmailButton) {
            if (email) {
                machineEmailButton.disabled = false;
                machineEmailButton.querySelector('.meta-value').textContent = email;
                machineEmailButton.onclick = () => copyToClipboard(email, 'E-mail');
            } else {
                machineEmailButton.disabled = true;
                machineEmailButton.querySelector('.meta-value').textContent = 'Não informado';
                machineEmailButton.onclick = null;
            }
        }

        machineAvatarElement?.setAttribute('data-initial', getInitials(deviceName));
    }

    function updateInfoSections(machine) {
        const overviewItems = [
            { label: 'ID do Ativo', value: machine.id },
            { label: 'Setor', value: machine.setor },
            { label: 'Responsável', value: machine.responsavel },
            { label: 'Localidade', value: machine.localidade }
        ];

        const technicalItems = [
            { label: 'Número de Série', value: machine.numero_serie },
            { label: 'Sistema Operacional', value: machine.sistema_operacional },
            { label: 'E-mail do Responsável', value: machine.email_responsavel }
        ];

        populateGrid(overviewGrid, overviewItems);
        populateGrid(technicalGrid, technicalItems);

        const notes = machine.observacao && machine.observacao.trim();
        if (machineNotesElement) {
            machineNotesElement.textContent = notes || 'Nenhuma observação registrada.';
        }
    }

    function activateTab(targetTab) {
        tabButtons.forEach((button) => {
            const isActive = button.dataset.tab === targetTab;
            button.classList.toggle('active', isActive);
            button.setAttribute('aria-selected', String(isActive));
        });

        tabContents.forEach((content) => {
            const isActive = content.id === `tab-${targetTab}`;
            content.classList.toggle('active', isActive);
            if (isActive) {
                content.removeAttribute('aria-hidden');
            } else {
                content.setAttribute('aria-hidden', 'true');
            }
        });
    }

    tabButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const { tab } = button.dataset;
            if (tab) {
                activateTab(tab);
            }
        });
    });

    if (refreshNotesButton) {
        refreshNotesButton.addEventListener('click', () => {
            themeIndex = (themeIndex + 1) % visualThemes.length;
            applyVisualTheme(themeIndex);
            showToast('Visual atualizado');
        });
    }

    async function fetchMachineDetails() {
        if (!machineId) {
            if (machineDetails) {
                machineDetails.innerHTML = '<p>ID do ativo não fornecido.</p>';
            }
            return;
        }


    function present(value) {
        return value && value.trim() ? value : '—';
    }

 codex/improve-code-for-professional-and-interactive-design-9coivc
    function formatSummary(machine) {
        return [
            `Ativo: ${machine.nome_dispositivo || 'N/D'}`,
            `Setor: ${machine.setor || 'N/D'}`,
            `Responsável: ${machine.responsavel || 'N/D'} (${machine.email_responsavel || 'sem e-mail'})`,
            `Localidade: ${machine.localidade || 'Não informada'}`,
            `Série: ${machine.numero_serie || 'N/D'}`,
            `Sistema operacional: ${machine.sistema_operacional || 'Não informado'}`,
            `Windows Update: ${machine.windows_update_ativo || 'Não informado'}`,
            `Observações: ${machine.observacao || 'Sem observações registradas.'}`,
        ].join('\n');

            if (result.success) {
                const machine = result.data;
                updateHero(machine);
                updateInfoSections(machine);

                const seed = parseInt(machine.id, 10) || machine.nome_dispositivo?.length || 0;
                themeIndex = seed % visualThemes.length;
                applyVisualTheme(themeIndex);
            } else {
                if (machineDetails) {
                    machineDetails.innerHTML = `<p>${result.message}</p>`;
                }
            }
        } catch (error) {
            if (machineDetails) {
                machineDetails.innerHTML = '<p>Erro ao carregar os detalhes do ativo.</p>';
            }
        }

    }

    async function loadMachine() {
        try {
 codex/improve-code-for-professional-and-interactive-design-9coivc
            const response = await AssetManager.request(`machines/get.php?id=${encodeURIComponent(machineId)}`);
            if (!response?.data) {
                throw new Error('Ativo não encontrado.');

            const response = await fetch('../api/auth/session.php');
            const result = await response.json();
            if (result.success && result.data.user_name) {
                if (userNameElement) {
                    userNameElement.textContent = `Olá, ${result.data.user_name}`;
                }
            } else {
                window.location.href = 'login.html';
            }

            const machine = response.data;
            nameElement.textContent = machine.nome_dispositivo || 'Ativo sem nome';
            sectorElement.textContent = machine.setor ? `Setor: ${machine.setor}` : 'Setor não informado';
            locationElement.textContent = machine.localidade ? `Local: ${machine.localidade}` : 'Localidade não informada';
            ownerElement.textContent = present(machine.responsavel);
            ownerEmailElement.textContent = present(machine.email_responsavel);
            serialElement.textContent = present(machine.numero_serie);
            invoiceElement.textContent = present(machine.nota_fiscal);
            windowsUpdateElement.textContent = present(machine.windows_update_ativo);
            osElement.textContent = present(machine.sistema_operacional);
            notesElement.textContent = machine.observacao?.trim() || 'Sem observações registradas.';

            const now = new Intl.DateTimeFormat('pt-BR', {
                dateStyle: 'long',
                timeStyle: 'short',
            }).format(new Date());
            updatedElement.textContent = `Visualizado em ${now}`;

            copyButton?.addEventListener('click', async () => {
                try {
                    await navigator.clipboard.writeText(formatSummary(machine));
                    AssetManager.showToast({ title: 'Resumo copiado', description: 'As informações foram copiadas para a área de transferência.' });
                } catch (error) {
                    AssetManager.showToast({ title: 'Não foi possível copiar', variant: 'error' });
                }
            });
        } catch (error) {
            nameElement.textContent = 'Erro ao carregar';
            notesElement.textContent = error.message || 'Não foi possível recuperar os dados deste ativo.';
            if (error.status === 401) {
                window.location.href = 'login.html';
            }
        }
    }

    loadMachine();
});
