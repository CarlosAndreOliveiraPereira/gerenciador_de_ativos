document.addEventListener('DOMContentLoaded', () => {
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

    const urlParams = new URLSearchParams(window.location.search);
    const machineId = urlParams.get('id');

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

        try {
            const response = await fetch(`../api/machines/get.php?id=${machineId}`);
            const result = await response.json();

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

    async function fetchSession() {
        try {
            const response = await fetch('../api/auth/session.php');
            const result = await response.json();
            if (result.success && result.data.user_name) {
                if (userNameElement) {
                    userNameElement.textContent = `Olá, ${result.data.user_name}`;
                }
            } else {
                window.location.href = 'login.html';
            }
        } catch (error) {
            window.location.href = 'login.html';
        }
    }

    async function handleLogout() {
        try {
            await fetch('../api/auth/logout.php', { method: 'POST' });
        } finally {
            window.location.href = 'login.html';
        }
    }

    if (logoutButton) {
        logoutButton.addEventListener('click', handleLogout);
    }

    fetchSession();
    fetchMachineDetails();
});
