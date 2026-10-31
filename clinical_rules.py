<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Radar Beers - Triagem Farmacêutica</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f1f5f9; }
        .topbar { background: linear-gradient(90deg, #07192f 0%, #0d2747 100%); border-bottom: 2px solid #0284c7; }
    </style>
</head>
<body class="text-slate-800">

    <!-- MODAL DE LOGIN -->
    <div id="login-modal" class="fixed inset-0 bg-slate-900/80 z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-xl shadow-2xl max-w-sm w-full p-6 border border-slate-200">
            <div class="flex items-center gap-3 mb-4">
                <div class="w-11 h-11 rounded-lg bg-[#0d2747] border border-sky-400 flex items-center justify-center">
                    <svg class="w-7 h-7 text-sky-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/><path d="M12 12L18.5 5.5"/>
                    </svg>
                </div>
                <div>
                    <h2 class="text-lg font-extrabold text-slate-900">Radar<span class="text-sky-500">Beers</span></h2>
                    <p class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Acesso Farmacêutico</p>
                </div>
            </div>
            <div class="space-y-3">
                <div>
                    <label class="text-xs font-bold text-slate-600 uppercase">Usuário</label>
                    <input id="login-user" type="text" class="w-full mt-1 p-2.5 border border-slate-300 rounded-lg text-sm" placeholder="admin">
                </div>
                <div>
                    <label class="text-xs font-bold text-slate-600 uppercase">Senha</label>
                    <input id="login-pass" type="password" class="w-full mt-1 p-2.5 border border-slate-300 rounded-lg text-sm" placeholder="••••••••">
                </div>
                <p id="login-err" class="text-xs text-red-600 font-semibold hidden"></p>
                <button onclick="doLogin()" class="w-full bg-[#0d2747] hover:bg-slate-800 text-white font-bold py-2.5 rounded-lg text-sm">Entrar no Sistema</button>
            </div>
        </div>
    </div>

    <!-- BARRA SUPERIOR ORIGINAL RESTAURADA -->
    <header class="topbar text-white px-5 py-2.5 flex flex-wrap justify-between items-center gap-4 shadow-md">
        <div class="flex items-center gap-5">
            <!-- LOGO RADAR BEERS (Aceita logo.png se existir no GitHub ou exibe o Radar SVG embutido sem quebrar) -->
            <div class="flex items-center gap-3">
                <img src="/logo.png" alt="Radar Beers" class="h-10 w-10 rounded-lg object-contain border border-sky-400/40"
                     onerror="this.style.display='none'; document.getElementById('svg-radar-logo').style.display='flex';">
                <div id="svg-radar-logo" style="display:none;" class="w-10 h-10 rounded-lg bg-[#0b223e] border border-sky-400/70 items-center justify-center shadow-inner">
                    <svg class="w-6 h-6 text-sky-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="9" stroke-opacity="0.9"/>
                        <circle cx="12" cy="12" r="5" stroke-opacity="0.6"/>
                        <circle cx="12" cy="12" r="1.5" fill="#38bdf8"/>
                        <path d="M12 12L18.3 5.7" stroke="#38bdf8" stroke-width="2.2" stroke-linecap="round"/>
                    </svg>
                </div>
                <div>
                    <div class="text-lg font-extrabold tracking-tight leading-none">Radar<span class="text-sky-400">Beers</span></div>
                    <div class="text-[10px] font-bold text-sky-400 tracking-widest uppercase mt-0.5">TRIAGEM FARMACÊUTICA</div>
                </div>
            </div>

            <!-- BOTÕES DE AÇÃO DA ESQUERDA -->
            <div class="flex items-center gap-2.5 ml-4">
                <button onclick="resetScreening()" class="bg-[#0d9488] hover:bg-[#0f766e] text-white font-semibold text-xs px-3.5 py-2 rounded-md flex items-center gap-1.5 shadow-sm transition">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
                    Nova Triagem
                </button>
                <a href="/manual.html" target="_blank" class="bg-[#0284c7] hover:bg-[#0369a1] text-white font-semibold text-xs px-3.5 py-2 rounded-md flex items-center gap-1.5 shadow-sm transition">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
                    Manual Operacional
                </a>
            </div>
        </div>

        <!-- INDICADORES E CONTROLES DA DIREITA -->
        <div class="flex items-center gap-4">
            <div class="text-right">
                <div class="text-[10px] font-bold text-slate-400 uppercase">CLCR CALCULADO</div>
                <div id="header-crcl" class="text-xs font-extrabold text-sky-400">-- mL/min</div>
            </div>
            <div class="text-right">
                <div class="text-[10px] font-bold text-slate-400 uppercase">CRITÉRIOS DE BEERS</div>
                <div id="header-alerts" class="text-xs font-extrabold text-amber-400">0</div>
            </div>

            <div class="h-6 w-px bg-slate-700"></div>

            <span id="current-user-label" class="text-xs font-bold text-white">admin (ADMIN)</span>

            <button onclick="openMetricsModal()" class="bg-[#16355d] hover:bg-[#1e4475] border border-sky-500/30 text-sky-300 font-semibold text-xs px-3 py-1.5 rounded-md flex items-center gap-1.5 transition">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
                Indicadores
            </button>
            <button onclick="openUsersModal()" class="bg-[#16355d] hover:bg-[#1e4475] border border-sky-500/30 text-sky-300 font-semibold text-xs px-3 py-1.5 rounded-md flex items-center gap-1.5 transition">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                Usuários
            </button>
            <button onclick="doLogout()" class="bg-slate-800 hover:bg-red-900/60 border border-slate-600 text-slate-200 font-semibold text-xs px-3 py-1.5 rounded-md flex items-center gap-1 transition">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
                Sair
            </button>
        </div>
    </header>

    <!-- CONTEÚDO PRINCIPAL -->
    <main class="max-w-7xl mx-auto p-4 space-y-4">

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <!-- 1. PACIENTE & DIAGNÓSTICOS -->
            <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200/80">
                <h2 class="text-xs font-extrabold uppercase tracking-wider text-slate-800 mb-3">1. PACIENTE & DIAGNÓSTICOS</h2>
                <div class="grid grid-cols-2 gap-3 mb-3">
                    <div>
                        <label class="block text-[10px] font-bold text-slate-500 uppercase mb-1">IDADE (ANOS)</label>
                        <input type="number" id="age" value="71" class="w-full bg-slate-50 border border-slate-300 text-slate-800 text-sm rounded-lg p-2">
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold text-slate-500 uppercase mb-1">SETOR</label>
                        <select id="sector" class="w-full bg-slate-100 border border-slate-300 text-slate-800 text-sm font-semibold rounded-lg p-2" disabled>
                            <option value="Enfermaria" selected>Enfermaria</option>
                        </select>
                    </div>
                </div>

                <label class="flex items-center gap-2 mb-3 cursor-pointer">
                    <input id="fall_risk" type="checkbox" class="w-4 h-4 text-sky-600 rounded border-slate-300">
                    <span class="text-xs font-semibold text-blue-900">Risco Alto de Queda (Idoso / Acamado)</span>
                </label>

                <div>
                    <label class="block text-[10px] font-bold text-slate-500 uppercase mb-1">COMORBIDADES / CONDIÇÕES CLÍNICAS</label>
                    <input type="text" id="conditions-input" placeholder="Selecione ou adicione via atalhos..." class="w-full bg-slate-50 border border-slate-300 text-xs rounded-lg p-2 mb-2">
                    <div class="flex flex-wrap gap-1.5">
                        <button type="button" onclick="addCondition('HAS')" class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold px-2 py-0.5 rounded border border-slate-300">+ HAS</button>
                        <button type="button" onclick="addCondition('DM')" class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold px-2 py-0.5 rounded border border-slate-300">+ DM</button>
                        <button type="button" onclick="addCondition('DRC')" class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold px-2 py-0.5 rounded border border-slate-300">+ DRC</button>
                        <button type="button" onclick="addCondition('IC')" class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold px-2 py-0.5 rounded border border-slate-300">+ IC</button>
                        <button type="button" onclick="addCondition('Demência')" class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold px-2 py-0.5 rounded border border-slate-300">+ Demência</button>
                        <button type="button" onclick="addCondition('Parkinson')" class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold px-2 py-0.5 rounded border border-slate-300">+ Parkinson</button>
                        <button type="button" onclick="addCondition('DPOC')" class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold px-2 py-0.5 rounded border border-slate-300">+ DPOC</button>
                        <button type="button" onclick="addCondition('IAM')" class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold px-2 py-0.5 rounded border border-slate-300">+ IAM</button>
                    </div>
                </div>
            </div>

            <!-- 2. FUNÇÃO RENAL & ANTROPOMETRIA -->
            <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200/80">
                <h2 class="text-xs font-extrabold uppercase tracking-wider text-slate-800 mb-3">2. FUNÇÃO RENAL & ANTROPOMETRIA</h2>
                <div class="grid grid-cols-3 gap-2 mb-3">
                    <div>
                        <label class="block text-[10px] font-bold text-slate-500 uppercase mb-1">CREATININA (MG/DL)</label>
                        <input type="text" id="creatinina" placeholder="Ex: 1.2" class="w-full bg-slate-50 border border-slate-300 text-sm rounded-lg p-2">
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold text-slate-500 uppercase mb-1">PESO (KG)</label>
                        <input type="text" id="peso" placeholder="Ex: 70" class="w-full bg-slate-50 border border-slate-300 text-sm rounded-lg p-2">
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold text-slate-500 uppercase mb-1">ALTURA (CM)</label>
                        <input type="text" id="altura" placeholder="Ex: 165" class="w-full bg-slate-50 border border-slate-300 text-sm rounded-lg p-2">
                    </div>
                </div>
                <div class="mb-3">
                    <label class="block text-[10px] font-bold text-slate-500 uppercase mb-1">SEXO BIOLÓGICO</label>
                    <select id="sexo" class="w-full bg-slate-50 border border-slate-300 text-sm rounded-lg p-2">
                        <option value="M">Masculino</option>
                        <option value="F">Feminino</option>
                    </select>
                </div>
                <div class="bg-slate-50 border border-slate-200 rounded-lg p-3 text-center">
                    <div class="text-[10px] font-bold text-slate-400 uppercase">DEPURAÇÃO ESTIMADA</div>
                    <div id="calc-crcl" class="text-lg font-extrabold text-slate-800 mt-0.5">-- mL/min</div>
                    <div id="sarcopenia-note" class="text-[10px] text-amber-700 font-semibold hidden mt-0.5">Piso de sarcopenia (0,6 mg/dL) aplicado</div>
                </div>
            </div>

            <!-- 3. ENTRADA DA PRESCRIÇÃO -->
            <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200/80 flex flex-col justify-between">
                <div>
                    <h2 class="text-xs font-extrabold uppercase tracking-wider text-slate-800 mb-3">3. ENTRADA DA PRESCRIÇÃO</h2>
                    <label class="block text-[10px] font-bold text-slate-500 uppercase mb-1">PRESCRIÇÃO HOSPITALAR (PDF)</label>
                    <input type="file" id="pdf-upload" accept="application/pdf" class="block w-full text-xs text-slate-500 mb-3 file:mr-3 file:py-1.5 file:px-3 file:rounded-md file:border file:border-sky-200 file:text-xs file:font-semibold file:bg-sky-50 file:text-sky-700 hover:file:bg-sky-100">

                    <label class="block text-[10px] font-bold text-slate-500 uppercase mb-1">OU COLE A PRESCRIÇÃO</label>
                    <textarea id="text-upload" rows="3" placeholder="Cole o texto da prescrição..." class="w-full bg-slate-50 border border-slate-300 text-xs rounded-lg p-2 mb-3"></textarea>
                </div>
                <button id="btn-extract" class="w-full bg-[#0b223e] hover:bg-[#13325b] text-white font-bold py-2.5 px-4 rounded-lg text-xs transition">
                    Extrair Prescrição Completa
                </button>
            </div>
        </div>

        <!-- 4. MEDICAMENTOS EM USO -->
        <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200/80">
            <div class="flex justify-between items-center mb-3">
                <h2 class="text-xs font-extrabold uppercase tracking-wider text-slate-800">4. MEDICAMENTOS EM USO</h2>
                <span id="med-count-badge" class="bg-slate-100 text-slate-700 text-xs font-bold px-2.5 py-0.5 rounded border border-slate-300">0 Medicamentos</span>
            </div>

            <div class="bg-slate-50/70 border border-slate-200 rounded-lg p-3 mb-4">
                <div class="text-[10px] font-bold text-slate-500 uppercase mb-2">+ ADIÇÃO RÁPIDA MANUAL</div>
                <div class="flex flex-wrap gap-2">
                    <input type="text" id="manual-med-name" placeholder="Princípio Ativo ou Medicamento..." class="flex-grow min-w-[200px] bg-white border border-slate-300 text-xs rounded-lg p-2">
                    <input type="text" id="manual-med-dose" placeholder="Dose (Ex: 25mg)" class="w-32 bg-white border border-slate-300 text-xs rounded-lg p-2">
                    <select id="manual-med-route" class="w-36 bg-white border border-slate-300 text-xs rounded-lg p-2">
                        <option>VO (Oral)</option>
                        <option>IV (Endovenoso)</option>
                        <option>IM (Intramuscular)</option>
                        <option>SC (Subcutâneo)</option>
                        <option>Inalatório</option>
                        <option>Tópico</option>
                    </select>
                    <input type="text" id="manual-med-freq" placeholder="Posologia (Ex: 12/12h)" class="w-40 bg-white border border-slate-300 text-xs rounded-lg p-2">
                    <label class="flex items-center gap-1.5 text-xs font-semibold bg-white border border-slate-300 px-3 rounded-lg cursor-pointer">
                        <input type="checkbox" id="manual-med-sos" class="rounded text-sky-600"> SN/QN
                    </label>
                    <button id="btn-add-manual" class="bg-[#0b223e] hover:bg-[#13325b] text-white font-bold py-2 px-4 rounded-lg text-xs">
                        + Inserir
                    </button>
                </div>
            </div>

            <div class="overflow-x-auto border border-slate-200 rounded-lg">
                <table class="w-full text-xs text-left">
                    <thead class="text-[11px] text-slate-600 uppercase bg-slate-100 border-b border-slate-200">
                        <tr>
                            <th class="px-4 py-2.5">MEDICAMENTO / PRINCÍPIO ATIVO</th>
                            <th class="px-4 py-2.5">DOSE / VIA / FREQUÊNCIA</th>
                            <th class="px-4 py-2.5">AVALIAÇÃO AGS BEERS</th>
                            <th class="px-4 py-2.5 text-right">AÇÕES</th>
                        </tr>
                    </thead>
                    <tbody id="med-table-body">
                        <tr>
                            <td colspan="4" class="px-4 py-8 text-center text-slate-400">Nenhum medicamento na lista de triagem.</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="mt-4 flex justify-end gap-2.5">
                <button id="btn-clear" class="text-slate-600 bg-white border border-slate-300 hover:bg-slate-100 font-semibold rounded-lg text-xs px-4 py-2">Limpar Lista</button>
                <button id="btn-process" class="text-white bg-[#0284c7] hover:bg-[#0369a1] font-bold rounded-lg text-xs px-5 py-2.5 shadow-sm">
                    Processar Triagem Farmacêutica
                </button>
            </div>
        </div>

        <!-- ÁREA DE RESULTADOS E INTERVENÇÕES -->
        <div id="results-area" class="hidden bg-white p-5 rounded-xl shadow-sm border border-sky-200 space-y-4">
            <h2 class="text-sm font-extrabold uppercase tracking-wider text-slate-900 border-b pb-2">PARECER FARMACÊUTICO — RADAR BEERS (ENFERMARIA)</h2>
            <div id="results-content" class="space-y-3"></div>
        </div>

    </main>

    <!-- MODAL DE INDICADORES (EXCLUSIVO ENFERMARIA) -->
    <div id="metrics-modal" class="fixed inset-0 bg-slate-900/75 z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-xl shadow-xl max-w-2xl w-full p-6">
            <div class="flex justify-between items-center border-b pb-3 mb-4">
                <h3 class="text-base font-extrabold text-slate-800">Indicadores Clínicos — Enfermaria (Radar Beers)</h3>
                <button onclick="closeMetricsModal()" class="text-slate-400 hover:text-slate-700 font-bold text-lg">&times;</button>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
                <div class="bg-slate-50 p-3 rounded-lg border text-center">
                    <div class="text-[10px] font-bold text-slate-500 uppercase">Pacientes (Enfermaria)</div>
                    <div id="m-total-patients" class="text-2xl font-black text-slate-800">0</div>
                </div>
                <div class="bg-amber-50 p-3 rounded-lg border border-amber-200 text-center">
                    <div class="text-[10px] font-bold text-amber-700 uppercase">Alertas Beers</div>
                    <div id="m-total-alerts" class="text-2xl font-black text-amber-700">0</div>
                </div>
                <div class="bg-emerald-50 p-3 rounded-lg border border-emerald-200 text-center">
                    <div class="text-[10px] font-bold text-emerald-700 uppercase">Intervenções Aceitas</div>
                    <div id="m-accepted" class="text-2xl font-black text-emerald-700">0</div>
                </div>
                <div class="bg-sky-50 p-3 rounded-lg border border-sky-200 text-center">
                    <div class="text-[10px] font-bold text-sky-700 uppercase">Taxa de Aceitação</div>
                    <div id="m-rate" class="text-2xl font-black text-sky-700">0%</div>
                </div>
            </div>
            <div>
                <h4 class="text-xs font-bold uppercase text-slate-500 mb-2">Top 5 Medicamentos Potencialmente Inapropriados</h4>
                <div id="m-top5" class="space-y-1.5 text-xs"></div>
            </div>
        </div>
    </div>

    <!-- MODAL DE USUÁRIOS -->
    <div id="users-modal" class="fixed inset-0 bg-slate-900/75 z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-xl shadow-xl max-w-xl w-full p-6">
            <div class="flex justify-between items-center border-b pb-3 mb-4">
                <h3 class="text-base font-extrabold text-slate-800">Gestão de Usuários</h3>
                <button onclick="closeUsersModal()" class="text-slate-400 hover:text-slate-700 font-bold text-lg">&times;</button>
            </div>
            <div class="flex gap-2 mb-4">
                <input id="new-u-name" type="text" placeholder="Novo usuário" class="flex-1 border rounded-lg p-2 text-xs">
                <input id="new-u-pass" type="password" placeholder="Senha" class="w-32 border rounded-lg p-2 text-xs">
                <select id="new-u-role" class="border rounded-lg p-2 text-xs">
                    <option value="pharmacist">Farmacêutico</option>
                    <option value="admin">Admin</option>
                </select>
                <button onclick="createUser()" class="bg-[#0b223e] text-white text-xs font-bold px-3 py-2 rounded-lg">Criar</button>
            </div>
            <div id="users-list" class="space-y-2 max-h-60 overflow-y-auto text-xs"></div>
        </div>
    </div>

    <script>
        let medicationsList = [];
        let currentUser = { username: "admin", role: "ADMIN" };
        const API_BASE_URL = '/api/v1';

        function addCondition(cond) {
            const inp = document.getElementById('conditions-input');
            const current = inp.value.split(',').map(s => s.trim()).filter(Boolean);
            if (!current.includes(cond)) {
                current.push(cond);
                inp.value = current.join(', ');
            }
        }

        function calculateCrCl() {
            const scr = parseFloat(document.getElementById('creatinina').value.replace(',', '.'));
            const weight = parseFloat(document.getElementById('peso').value.replace(',', '.'));
            const age = parseInt(document.getElementById('age').value, 10);
            const sex = document.getElementById('sexo').value;
            const note = document.getElementById('sarcopenia-note');

            if (isNaN(scr) || isNaN(weight) || isNaN(age) || scr <= 0 || weight <= 0 || age <= 0) {
                document.getElementById('calc-crcl').textContent = "-- mL/min";
                document.getElementById('header-crcl').textContent = "-- mL/min";
                note.classList.add('hidden');
                return null;
            }

            let adjustedScr = scr;
            if (scr < 0.6) {
                adjustedScr = 0.6;
                note.classList.remove('hidden');
            } else {
                note.classList.add('hidden');
            }

            let crcl = ((140 - age) * weight) / (72 * adjustedScr);
            if (sex === 'F') crcl *= 0.85;

            const formatted = crcl.toFixed(1) + " mL/min";
            document.getElementById('calc-crcl').textContent = formatted;
            document.getElementById('header-crcl').textContent = formatted;
            return parseFloat(crcl.toFixed(1));
        }

        ['creatinina', 'peso', 'age', 'sexo'].forEach(id => {
            document.getElementById(id).addEventListener('input', calculateCrCl);
            document.getElementById(id).addEventListener('change', calculateCrCl);
        });

        function renderTable(rowsFromServer = null) {
            const tbody = document.getElementById('med-table-body');
            document.getElementById('med-count-badge').textContent = `${medicationsList.length} Medicamentos`;

            if (medicationsList.length === 0) {
                tbody.innerHTML = `<tr><td colspan="4" class="px-4 py-8 text-center text-slate-400">Nenhum medicamento na lista de triagem.</td></tr>`;
                return;
            }

            tbody.innerHTML = '';
            const displayRows = rowsFromServer || medicationsList.map(m => ({
                name: m.name,
                dose_route: [m.dose, m.route, m.frequency].filter(Boolean).join(' '),
                is_sos: m.is_sos,
                is_beers: null,
                alert_tag: ''
            }));

            displayRows.forEach((row, index) => {
                const sosBadge = row.is_sos ? `<span class="bg-amber-100 text-amber-800 text-[10px] font-bold px-2 py-0.5 rounded ml-1.5 border border-amber-300">SN/QN (Se Necessário)</span>` : '';
                let statusHtml = `<span class="text-slate-400 italic">Aguardando processamento...</span>`;
                if (row.is_beers === true) {
                    statusHtml = `<span class="bg-red-100 text-red-700 font-bold px-2 py-1 rounded border border-red-200 uppercase text-[10px]">${row.alert_tag}</span>`;
                } else if (row.is_beers === false) {
                    statusHtml = `<span class="bg-emerald-50 text-emerald-700 font-semibold px-2 py-1 rounded border border-emerald-200 text-[10px]">Sem Alerta Beers</span>`;
                }

                const tr = document.createElement('tr');
                tr.className = row.is_beers ? "bg-red-50/60 border-b" : "bg-white border-b";
                tr.innerHTML = `
                    <td class="px-4 py-2.5 font-bold text-slate-900">${row.name} ${sosBadge}</td>
                    <td class="px-4 py-2.5 text-slate-600">${row.dose_route || 'VO (Oral)'}</td>
                    <td class="px-4 py-2.5">${statusHtml}</td>
                    <td class="px-4 py-2.5 text-right">
                        <button onclick="removeMedication(${index})" class="text-red-600 hover:underline font-semibold">Remover</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        function removeMedication(idx) {
            medicationsList.splice(idx, 1);
            renderTable();
        }

        function resetScreening() {
            medicationsList = [];
            document.getElementById('pdf-upload').value = '';
            document.getElementById('text-upload').value = '';
            document.getElementById('conditions-input').value = '';
            document.getElementById('header-alerts').textContent = '0';
            document.getElementById('results-area').classList.add('hidden');
            renderTable();
        }

        document.getElementById('btn-clear').addEventListener('click', resetScreening);

        document.getElementById('btn-add-manual').addEventListener('click', () => {
            const name = document.getElementById('manual-med-name').value.trim();
            const dose = document.getElementById('manual-med-dose').value.trim();
            const route = document.getElementById('manual-med-route').value;
            const freq = document.getElementById('manual-med-freq').value.trim();
            const isSos = document.getElementById('manual-med-sos').checked || /\b(sn|qn|sos)\b/i.test(freq);

            if (!name) return alert("Informe o nome do medicamento.");
            medicationsList.push({ name, dose, route, frequency: freq, is_sos: isSos });

            document.getElementById('manual-med-name').value = '';
            document.getElementById('manual-med-dose').value = '';
            document.getElementById('manual-med-freq').value = '';
            document.getElementById('manual-med-sos').checked = false;
            renderTable();
        });

        document.getElementById('btn-extract').addEventListener('click', async () => {
            const file = document.getElementById('pdf-upload').files[0];
            const text = document.getElementById('text-upload').value.trim();
            if (!file && !text) return alert("Selecione um PDF ou cole o texto da prescrição.");

            try {
                let data;
                if (file) {
                    const formData = new FormData();
                    formData.append("file", file);
                    const res = await fetch(`${API_BASE_URL}/prescription/extract-pdf`, { method: 'POST', body: formData });
                    data = await res.json();
                } else {
                    const res = await fetch(`${API_BASE_URL}/prescription/extract-text`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ text })
                    });
                    data = await res.json();
                }

                if (data.items && data.items.length > 0) {
                    medicationsList = [...medicationsList, ...data.items];
                    renderTable();
                } else {
                    alert("Nenhum medicamento da lista de Beers foi detectado.");
                }
            } catch (e) {
                alert("Erro ao extrair prescrição: " + e.message);
            }
        });

        document.getElementById('btn-process').addEventListener('click', async () => {
            if (medicationsList.length === 0) return alert("Adicione medicamentos antes de processar.");

            const payload = {
                age: parseInt(document.getElementById('age').value, 10) || 70,
                sector: "Enfermaria",
                fall_risk: document.getElementById('fall_risk').checked,
                conditions: document.getElementById('conditions-input').value.split(',').map(s => s.trim()).filter(Boolean),
                crcl_ml_min: calculateCrCl(),
                medications: medicationsList,
                persist: true
            };

            const res = await fetch(`${API_BASE_URL}/screen`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            document.getElementById('header-alerts').textContent = data.total_beers_alerts || 0;
            renderTable(data.medication_rows);

            const resultsArea = document.getElementById('results-area');
            const resultsContent = document.getElementById('results-content');
            resultsArea.classList.remove('hidden');
            resultsContent.innerHTML = '';

            // Card ACB
            const acbDiv = document.createElement('div');
            acbDiv.className = `p-4 rounded-lg border ${data.acb_score >= 3 ? 'bg-red-50 border-red-300 text-red-900' : 'bg-sky-50 border-sky-200 text-sky-900'} flex justify-between items-center`;
            acbDiv.innerHTML = `
                <div>
                    <div class="font-extrabold text-sm uppercase">Carga Anticolinérgica Basal (ACB Score Contínuo)</div>
                    <div class="text-xs mt-1">${data.acb_interpretation}</div>
                </div>
                <div class="text-3xl font-black">${data.acb_score}</div>
            `;
            resultsContent.appendChild(acbDiv);

            (data.alerts || []).forEach(alert => {
                const card = document.createElement('div');
                card.className = "p-4 rounded-lg border border-slate-200 bg-slate-50/60 space-y-2";
                const sosBanner = alert.is_sos
                    ? `<span class="inline-block bg-amber-100 text-amber-900 border border-amber-300 text-[10px] font-extrabold px-2.5 py-0.5 rounded uppercase">Prescrito SN/QN — Paciente sem uso contínuo</span>`
                    : `<span class="inline-block bg-red-100 text-red-800 border border-red-200 text-[10px] font-extrabold px-2.5 py-0.5 rounded uppercase">Uso Regular / Contínuo</span>`;

                card.innerHTML = `
                    <div class="flex flex-wrap justify-between items-center gap-2">
                        <div>
                            ${sosBanner}
                            <h3 class="text-base font-extrabold text-slate-900 mt-1">${alert.drug} <span class="text-xs font-semibold text-slate-500">(${alert.axis})</span></h3>
                        </div>
                        ${alert.id ? `
                        <div class="flex gap-1.5">
                            <button onclick="setOutcome(${alert.id}, 'accepted', this)" class="px-2.5 py-1 text-[11px] font-bold rounded border bg-white hover:bg-emerald-50 text-emerald-700 border-emerald-300">Aceita</button>
                            <button onclick="setOutcome(${alert.id}, 'rejected', this)" class="px-2.5 py-1 text-[11px] font-bold rounded border bg-white hover:bg-red-50 text-red-700 border-red-300">Não Aceita</button>
                        </div>` : ''}
                    </div>
                    <p class="text-xs"><strong class="text-slate-800">Conduta:</strong> ${alert.recommendation}</p>
                    <p class="text-xs text-slate-600"><strong class="text-slate-800">Racional Clínico:</strong> ${alert.rationale}</p>
                    <div class="bg-white p-2.5 rounded border border-sky-200 text-xs text-sky-950">
                        <strong>Manejo Prático / Desprescrição:</strong> ${alert.tapering}
                    </div>
                `;
                resultsContent.appendChild(card);
            });
        });

        async function setOutcome(alertId, outcome, btn) {
            await fetch(`${API_BASE_URL}/alerts/${alertId}/outcome`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ outcome })
            });
            btn.parentElement.innerHTML = `<span class="text-xs font-bold ${outcome === 'accepted' ? 'text-emerald-700' : 'text-red-700'}">${outcome === 'accepted' ? '✓ Intervenção Aceita' : '✗ Não Aceita'}</span>`;
        }

        async function openMetricsModal() {
            document.getElementById('metrics-modal').classList.remove('hidden');
            const res = await fetch(`${API_BASE_URL}/admin/metrics`);
            const d = await res.json();
            document.getElementById('m-total-patients').textContent = d.total_patients || 0;
            document.getElementById('m-total-alerts').textContent = d.total_beers_alerts || 0;
            document.getElementById('m-accepted').textContent = d.accepted_interventions || 0;
            document.getElementById('m-rate').textContent = (d.acceptance_rate || 0) + '%';
            const top5 = document.getElementById('m-top5');
            top5.innerHTML = (d.top_5_beers || []).map(x => `<div class="flex justify-between bg-slate-50 p-2 rounded border"><span>${x.drug}</span><strong>${x.count} alerta(s)</strong></div>`).join('') || '<p class="text-slate-400">Sem registros.</p>';
        }
        function closeMetricsModal() { document.getElementById('metrics-modal').classList.add('hidden'); }

        async function openUsersModal() {
            document.getElementById('users-modal').classList.remove('hidden');
            const res = await fetch(`${API_BASE_URL}/admin/users`);
            const users = await res.json();
            document.getElementById('users-list').innerHTML = users.map(u => `
                <div class="flex justify-between items-center p-2 border rounded-lg">
                    <div><strong>${u.username}</strong> (${u.role}) ${u.is_online ? '<span class="text-emerald-600 font-bold">● online</span>' : ''}</div>
                </div>
            `).join('');
        }
        function closeUsersModal() { document.getElementById('users-modal').classList.add('hidden'); }

        async function createUser() {
            const username = document.getElementById('new-u-name').value.trim();
            const password = document.getElementById('new-u-pass').value.trim();
            const role = document.getElementById('new-u-role').value;
            if (!username || !password) return;
            await fetch(`${API_BASE_URL}/admin/users`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password, role })
            });
            openUsersModal();
        }

        function doLogout() {
            document.getElementById('login-modal').classList.remove('hidden');
        }

        async function doLogin() {
            const username = document.getElementById('login-user').value.trim();
            const password = document.getElementById('login-pass').value.trim();
            const res = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            if (res.ok) {
                const data = await res.json();
                document.getElementById('current-user-label').textContent = `${data.user.username} (${data.user.role.toUpperCase()})`;
                document.getElementById('login-modal').classList.add('hidden');
            } else {
                const err = document.getElementById('login-err');
                err.textContent = "Usuário ou senha inválidos.";
                err.classList.remove('hidden');
            }
        }
    </script>
</body>
</html>
