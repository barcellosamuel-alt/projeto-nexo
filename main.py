<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projeto Nexo — Sanctuary Dashboard (Medicina UEL)</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #060911;
            --bg-card: rgba(13, 19, 33, 0.85);
            --bg-glass: rgba(30, 41, 59, 0.45);
            --border-color: rgba(51, 65, 85, 0.5);
            --border-hover: rgba(245, 158, 11, 0.6);
            --accent-amber: #f59e0b;
            --accent-emerald: #10b981;
            --accent-cyan: #38bdf8;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --danger: #f43f5e;
        }

        body {
            font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-base);
            color: var(--text-main);
            margin: 0;
            padding: 30px 20px;
            line-height: 1.6;
            background-image: 
                radial-gradient(circle at 10% 10%, rgba(245, 158, 11, 0.07) 0%, transparent 40%),
                radial-gradient(circle at 90% 90%, rgba(16, 185, 129, 0.07) 0%, transparent 40%),
                radial-gradient(circle at 50% 50%, rgba(56, 189, 248, 0.04) 0%, transparent 50%);
            background-attachment: fixed;
        }

        .container {
            max-width: 1150px;
            margin: 0 auto;
        }

        .top-utility-bar {
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 20px;
            margin-bottom: 25px;
        }

        header.hero {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            border: 1px solid var(--border-color);
            padding: 28px 35px;
            border-radius: 20px;
            box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
            overflow: hidden;
        }

        header.hero::after {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 4px; height: 100%;
            background: linear-gradient(to bottom, var(--accent-amber), var(--accent-emerald));
        }

        header.hero h1 {
            font-size: 26px;
            font-weight: 800;
            margin: 0 0 4px 0;
            color: #ffffff;
            letter-spacing: -0.5px;
        }

        header.hero p {
            font-size: 14px;
            color: var(--text-muted);
            margin: 0;
        }

        .clock-widget {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            padding: 15px 25px;
            border-radius: 20px;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            justify-content: center;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);
            backdrop-filter: blur(12px);
        }

        .clock-time {
            font-family: 'JetBrains Mono', monospace;
            font-size: 26px;
            font-weight: 700;
            color: var(--accent-amber);
            letter-spacing: 1px;
        }

        .clock-date {
            font-size: 12px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 2px;
        }

        .tools-bar {
            display: flex;
            gap: 12px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }

        .tool-btn {
            background: var(--bg-glass);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 10px 18px;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 600;
            font-size: 13px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.25s ease;
            backdrop-filter: blur(10px);
        }

        .tool-btn:hover {
            background: rgba(245, 158, 11, 0.12);
            border-color: var(--accent-amber);
            color: var(--accent-amber);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(245, 158, 11, 0.15);
        }

        .aux-drawer {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            padding: 20px;
            border-radius: 16px;
            margin-bottom: 25px;
            display: none;
            animation: fadeIn 0.3s ease;
            backdrop-filter: blur(16px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* NexoCat — Pet Digital Inteligente, Animado e Brincalhão */
        .pet-companion {
            position: fixed;
            bottom: 25px;
            right: 25px;
            background: var(--bg-card);
            border: 2px solid var(--accent-amber);
            padding: 14px 20px;
            border-radius: 24px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.7), 0 0 20px rgba(245, 158, 11, 0.2);
            display: flex;
            align-items: center;
            gap: 14px;
            z-index: 1000;
            backdrop-filter: blur(16px);
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .pet-companion:hover { 
            transform: scale(1.06) translateY(-3px); 
            border-color: var(--accent-emerald);
            box-shadow: 0 20px 45px rgba(0,0,0,0.8), 0 0 25px rgba(16, 185, 129, 0.3);
        }
        .pet-avatar { 
            font-size: 32px; 
            animation: floatPet 3.5s ease-in-out infinite;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.5));
        }
        @keyframes floatPet { 
            0%, 100% { transform: translateY(0) rotate(0deg); } 
            50% { transform: translateY(-7px) rotate(3deg); } 
        }
        .pet-bubble { font-size: 12px; color: var(--text-main); max-width: 210px; }
        .pet-jump { animation: jumpPet 0.4s ease; }
        @keyframes jumpPet {
            0% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-20px) scale(1.2); }
            100% { transform: translateY(0) scale(1); }
        }

        .card {
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            padding: 30px;
            border-radius: 20px;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.4);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .card:hover {
            border-color: var(--border-hover);
            box-shadow: 0 20px 40px -10px rgba(245, 158, 11, 0.15);
        }

        .card-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }

        .card-header svg {
            width: 26px;
            height: 26px;
            fill: var(--accent-amber);
            margin-right: 14px;
            flex-shrink: 0;
        }

        .card h3 {
            margin: 0;
            color: #ffffff;
            font-size: 19px;
            font-weight: 700;
        }

        .card p {
            color: var(--text-muted);
            font-size: 14px;
            margin-bottom: 20px;
        }

        label {
            display: block;
            font-weight: 600;
            font-size: 13px;
            color: var(--accent-amber);
            margin-bottom: 6px;
            margin-top: 15px;
            letter-spacing: 0.3px;
        }

        input[type="text"], textarea {
            width: 100%;
            padding: 12px 16px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 14px;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            box-sizing: border-box;
            background: #03050a;
            color: var(--text-main);
            transition: all 0.2s ease;
        }

        input[type="text"]:focus, textarea:focus {
            outline: none;
            border-color: var(--accent-amber);
            background: #020409;
            box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.15);
        }

        button.action-btn {
            background-color: #1e293b;
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 12px 22px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 600;
            font-size: 13px;
            transition: all 0.25s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 12px;
        }

        button.action-btn:hover {
            background-color: var(--accent-amber);
            color: #060911;
            border-color: var(--accent-amber);
            box-shadow: 0 0 20px rgba(245, 158, 11, 0.4);
            transform: translateY(-1px);
        }

        .btn-success {
            background-color: rgba(16, 185, 129, 0.15) !important;
            border-color: var(--accent-emerald) !important;
            color: var(--accent-emerald) !important;
        }
        .btn-success:hover {
            background-color: var(--accent-emerald) !important;
            color: #030712 !important;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.5) !important;
        }

        .response-box {
            background: #03050a;
            border: 1px solid var(--border-color);
            color: var(--accent-cyan);
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
            white-space: pre-wrap;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            border-left: 3px solid var(--accent-amber);
        }

        .content-display {
            background: #03050a;
            border: 1px solid var(--border-color);
            border-left: 3px solid var(--accent-amber);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            font-size: 14px;
        }

        .timer-badge {
            background: rgba(244, 63, 94, 0.15);
            border: 1px solid rgba(244, 63, 94, 0.4);
            color: var(--danger);
            padding: 6px 14px;
            border-radius: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            font-size: 13px;
            margin-left: auto;
        }

        .analytics-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 15px;
        }

        .metric-card {
            background: #03050a;
            border: 1px solid var(--border-color);
            padding: 20px;
            border-radius: 14px;
            position: relative;
        }

        .metric-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 2px;
            background: linear-gradient(to right, var(--accent-amber), transparent);
        }

        .metric-card strong {
            color: #ffffff;
            font-size: 13px;
            display: block;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        @media(max-width: 850px) {
            .top-utility-bar { grid-template-columns: 1fr; }
            .clock-widget { align-items: flex-start; }
            .analytics-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>

<!-- Pet Digital Flutuante (NexoCat Animado & Interativo) -->
<div class="pet-companion" onclick="interagirPet()" title="Clique para interagir com o NexoCat!">
    <div class="pet-avatar" id="petEmoji">🐱</div>
    <div class="pet-bubble">
        <strong style="color:var(--accent-amber); font-size:11px; display:block;">NexoCat (Guia Medicina UEL)</strong>
        <span id="petSpeech">"Miau! Pronto para gabaritar hoje?"</span>
    </div>
</div>

<div class="container">
    <div class="top-utility-bar">
        <header class="hero" style="margin-bottom: 0;">
            <div>
                <h1>PROJETO NEXO // SANCTUARY</h1>
                <p>Plataforma Longitudinal de Alta Performance — Medicina UEL</p>
            </div>
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); color: var(--accent-emerald); padding: 8px 16px; border-radius: 10px; font-weight: 700; font-size: 13px;">
                ✨ Foco, Saúde & Alta Performance
            </div>
        </header>
        <div class="clock-widget">
            <div class="clock-time" id="liveClock">00:00:00</div>
            <div class="clock-date" id="liveDate">A carregar data...</div>
        </div>
    </div>

    <!-- Barra de Ferramentas e Mini-Jogos Anti-Estresse -->
    <div class="tools-bar">
        <button class="tool-btn" onclick="toggleTool('notesDrawer')">📝 Bloco de Notas</button>
        <button class="tool-btn" onclick="toggleTool('calcDrawer')">🧮 Calculadora</button>
        <button class="tool-btn" onclick="toggleTool('focusDrawer')">💡 Pílula de Motivação</button>
        <button class="tool-btn" onclick="toggleTool('gamesDrawer')" style="border-color: var(--accent-emerald); color: var(--accent-emerald);">🎮 Pausa Ativa & Anti-Estresse</button>
    </div>

    <!-- Gaveta de Bloco de Notas -->
    <div id="notesDrawer" class="aux-drawer">
        <strong style="color: var(--accent-amber); display:block; margin-bottom: 8px;">📝 Bloco de Notas Local (Scratchpad)</strong>
        <textarea id="quickNotes" rows="4" placeholder="Escreva aqui fórmulas rápidas ou insights..." oninput="salvarNotas()"></textarea>
    </div>

    <!-- Gaveta de Calculadora Rápida -->
    <div id="calcDrawer" class="aux-drawer">
        <strong style="color: var(--accent-amber); display:block; margin-bottom: 8px;">🧮 Calculadora de Apoio Rápido</strong>
        <div style="display: flex; gap: 10px; margin-bottom: 10px;">
            <input type="text" id="calcInput" placeholder="Ex: 340 / 680" style="margin-top:0;" onkeydown="if(event.key==='Enter') calcularResultado()">
            <button class="action-btn" onclick="calcularResultado()" style="margin-top:0;">Calcular</button>
        </div>
        <div id="calcResult" style="font-family: 'JetBrains Mono'; font-size: 14px; color: var(--accent-emerald);"></div>
    </div>

    <!-- Gaveta de Motivação -->
    <div id="focusDrawer" class="aux-drawer">
        <strong style="color: var(--accent-amber); display:block; margin-bottom: 8px;">💡 Cantinho da Clareza & Saúde Mental</strong>
        <p style="font-style: italic; color: var(--text-main); font-size: 14px; margin: 0;">"A aprovação em Medicina na UEL é construída na consistência diária, respirando fundo e corrigindo cada lacuna com paciência."</p>
    </div>

    <!-- Gaveta de Mini-Jogos Anti-Estresse -->
    <div id="gamesDrawer" class="aux-drawer" style="border-color: var(--accent-emerald);">
        <strong style="color: var(--accent-emerald); display:block; margin-bottom: 8px;">🎮 Zona de Alívio & Pausa Ativa</strong>
        <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 12px;">Faça uma pausa de 2 minutos para recarregar o cérebro:</p>
        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <button class="action-btn" onclick="iniciarRespiracao()" style="border-color: var(--accent-emerald); color: var(--accent-emerald);">🧘 Exercício Respiração 4-7-8</button>
            <button class="action-btn" onclick="gerarDesafioRelampago()">⚡ Desafio Relâmpago UEL</button>
        </div>
        <div id="gameOutput" style="margin-top: 15px; font-size: 14px; color: var(--text-main); background: #03050a; padding: 15px; border-radius: 8px; display:none;"></div>
    </div>

    <!-- 1º Módulo: Treino Diário — Bloco de 20 Questões -->
    <div class="card">
        <div class="card-header">
            <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
            <h3>01 // Bloco de Treino Diário (20 Questões UEL)</h3>
        </div>
        <p>Inicialize o ciclo tático diário de resolução ativa para ganho de ritmo e precisão analítica:</p>
        <button class="action-btn" onclick="carregarBlocoDiario()">Carregar Bloco Diário</button>
        <div id="blockResponse" class="response-box" style="display:none; max-height: 300px; overflow-y: auto;"></div>
    </div>

    <!-- 2º Módulo: Protocolo de Active Recall & Validação de Recomposição -->
    <div class="card">
        <div class="card-header">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>
            <h3>02 // Protocolo de Active Recall & Recomposição Pedagógica</h3>
        </div>
        <p>Insira o ID da tentativa para carregar o protocolo dinâmico de remediação e o exercício de validação:</p>
        
        <label for="attemptId">ID da Tentativa / Sessão:</label>
        <input type="text" id="attemptId" value="1">
        
        <button class="action-btn" onclick="carregarRecomposicao()">Carregar Recomposição</button>

        <div id="recompositionContentContainer" style="display:none; margin-top: 20px;">
            <div class="content-display">
                <span style="color: var(--accent-amber); font-weight: 700; font-size: 12px; text-transform: uppercase;">[Diagnóstico de Lacuna]</span>
                <div id="gapInfo" style="margin-top: 4px; color: var(--text-main);"></div>
                
                <span style="color: var(--accent-emerald); font-weight: 700; font-size: 12px; text-transform: uppercase; display:block; margin-top: 14px;">[Microrevisão Ativa]</span>
                <div id="microRevisaoInfo" style="margin-top: 4px; color: var(--text-muted);"></div>
                
                <span style="color: var(--accent-cyan); font-weight: 700; font-size: 12px; text-transform: uppercase; display:block; margin-top: 14px;">[Exercício de Validação]</span>
                <div id="exercicioInfo" style="margin-top: 4px; color: var(--text-muted);"></div>
            </div>
            
            <label for="commandInput">Comando de Confirmação e Compreensão:</label>
            <input type="text" id="commandInput" value="[NEXO_LIDO_E_COMPREENDIDO]">
            
            <button class="action-btn btn-success" onclick="enviarAcknowledge()">Validar e Consolidar Leitura</button>
        </div>

        <div id="ackResponse" class="response-box" style="display:none;"></div>
    </div>

    <!-- 3º Módulo: Simulado Mensal Oficial (Padrão COPS/UEL — 60 Questões) -->
    <div class="card">
        <div class="card-header" style="display: flex; align-items: center; width: 100%; flex-wrap: wrap; gap: 10px;">
            <div style="display: flex; align-items: center;">
                <svg viewBox="0 0 24 24"><path d="M19 3h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm2 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
                <h3>03 // Simulado Mensal Oficial (60 Questões)</h3>
            </div>
            <span id="timerBadge" class="timer-badge">05:00:00</span>
        </div>
        <p>Execução do simulado completo de alto rendimento com cronômetro regressivo ativo padrão COPS/UEL:</p>
        <button class="action-btn" onclick="carregarSimulado()">Iniciar / Carregar Simulado</button>
        
        <div id="simulatedContainer" style="display:none; margin-top: 20px;">
            <div id="questionBox" class="content-display"></div>
            <div style="display: flex; gap: 10px; margin-top: 15px; flex-wrap: wrap;">
                <button class="action-btn" onclick="questaoAnterior()">Anterior</button>
                <button class="action-btn" onclick="proximaQuestao()">Seguinte</button>
                <button class="action-btn btn-success" onclick="submeterSimulado()" style="margin-left: auto;">Submeter Simulado</button>
            </div>
        </div>
        <div id="simResponse" class="response-box" style="display:none;"></div>
    </div>

    <!-- 4º Módulo: Submissão de Prova Discursiva (Banca COPS/UEL) -->
    <div class="card">
        <div class="card-header">
            <svg viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
            <h3>04 // Módulo Discursivo (Banca COPS/UEL)</h3>
        </div>
        <p>Submissão de respostas dissertativas para auditoria rigorosa de argumentação e fundamentação científica:</p>
        
        <label for="examTitle">Título / Questão:</label>
        <input type="text" id="examTitle" value="Simulado Discursivo — Biologia Celular">
        
        <label for="proposalContent">Enunciado / Proposta:</label>
        <textarea id="proposalContent" rows="3">Explique o processo de fosforilação oxidativa e o papel da ATP sintase na mitocôndria.</textarea>
        
        <label for="studentAnswer">A sua resposta:</label>
        <textarea id="studentAnswer" rows="4">A fosforilação oxidativa ocorre nas cristas mitocondriais...</textarea>
        
        <button class="action-btn" onclick="enviarDiscursiva()">Submeter Discursiva</button>
        <div id="discResponse" class="response-box" style="display:none;"></div>
    </div>

    <!-- 5º Módulo: Painel Analítico Longitudinal & Perfil de Ingresso -->
    <div class="card" style="border-color: rgba(245, 158, 11, 0.3);">
        <div class="card-header">
            <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/></svg>
            <h3>05 // Telemetria Longitudinal & Projeção de Ingresso (Medicina UEL)</h3>
        </div>
        <p>Cruzamento estatístico automatizado de descritores cognitivos com o histórico de notas de corte:</p>
        
        <div class="analytics-grid">
            <div class="metric-card">
                <strong>Status de Descritores:</strong>
                <p style="font-size: 13px; margin: 5px 0; color: var(--text-muted);">
                    Biologia Celular: <span style="color: var(--accent-emerald);">78% [CONSOLIDADO]</span><br>
                    Física Ondulatória: <span style="color: var(--danger);">45% [REQUER GAP]</span><br>
                    Química Orgânica: <span style="color: var(--accent-amber);">62% [ESTÁVEL]</span>
                </p>
            </div>
            <div class="metric-card">
                <strong>Projeção de Corte (UEL):</strong>
                <p style="font-size: 13px; margin: 5px 0; color: var(--text-muted);">
                    Baseline S1: <span style="color: #ffffff;">65.0 pts</span><br>
                    Teto Estimado: <span style="color: var(--accent-cyan);">82.0 pts</span><br>
                    Tendência: <span style="color: var(--accent-emerald);">▲ ASCENDENTE</span>
                </p>
            </div>
        </div>
    </div>
</div>

<script>
    // --- Relógio Local Otimizado e Fluido ---
    function atualizarRelogio() {
        const agora = new Date();
        const clockEl = document.getElementById('liveClock');
        const dateEl = document.getElementById('liveDate');
        
        if (clockEl) {
            clockEl.innerText = agora.toLocaleTimeString('pt-BR');
        }
        if (dateEl) {
            const opcoes = { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' };
            dateEl.innerText = agora.toLocaleDateString('pt-BR', opcoes);
        }
    }
    atualizarRelogio();
    setInterval(atualizarRelogio, 1000);

    // --- Temporizador Regressivo do Simulado (5 Horas) ---
    let tempoSimuladoSegundos = 5 * 3600;
    let timerSimuladoInterval = null;

    function iniciarContadorSimulado() {
        if (timerSimuladoInterval) clearInterval(timerSimuladoInterval);
        timerSimuladoInterval = setInterval(() => {
            if (tempoSimuladoSegundos > 0) {
                tempoSimuladoSegundos--;
                const horas = Math.floor(tempoSimuladoSegundos / 3600).toString().padStart(2, '0');
                const minutos = Math.floor((tempoSimuladoSegundos % 3600) / 60).toString().padStart(2, '0');
                const segundos = (tempoSimuladoSegundos % 60).toString().padStart(2, '0');
                const badge = document.getElementById('timerBadge');
                if (badge) {
                    badge.innerText = `${horas}:${minutos}:${segundos}`;
                }
            }
        }, 1000);
    }

    // --- NexoCat — Interações Brincalhonas, Emojis Dinâmicos e Animação ---
    const avataresPet = ["🐱", "😸", "😻", "😽", "😺"];
    const falasPet = [
        "Miau! Lembre-se de beber água e esticar as costas!",
        "Excelente foco! A vaga de Medicina na UEL é tua!",
        "Purr... O método longitudinal é o segredo do sucesso!",
        "Respira fundo! Cada questão resolvida é um passo rumo ao jaleco.",
        "Miau! Quer resolver um simulado ou fazer uma pausa ativa?"
    ];

    function interagirPet() {
        const companion = document.querySelector('.pet-companion');
        const emojiEl = document.getElementById('petEmoji');
        const speech = document.getElementById('petSpeech');
        
        if (companion && emojiEl && speech) {
            companion.classList.add('pet-jump');
            setTimeout(() => companion.classList.remove('pet-jump'), 400);

            const randomAvatar = avataresPet[Math.floor(Math.random() * avataresPet.length)];
            const randomFala = falasPet[Math.floor(Math.random() * falasPet.length)];
            
            emojiEl.innerText = randomAvatar;
            speech.innerText = `"${randomFala}"`;
        }
    }

    // --- Mini-Jogos & Pausa Ativa ---
    function iniciarRespiracao() {
        const out = document.getElementById('gameOutput');
        if (out) {
            out.style.display = 'block';
            out.innerHTML = "🧘 <strong>Ciclo de Respiração 4-7-8:</strong><br>Inspira pelo nariz (4s)... Segura o ar (7s)... Expira devagar pela boca (8s).<br><em style='color:var(--accent-emerald);'>Repita 3 vezes para baixar o cortisol instantaneamente.</em>";
        }
    }

    function gerarDesafioRelampago() {
        const out = document.getElementById('gameOutput');
        if (out) {
            out.style.display = 'block';
            out.innerHTML = "⚡ <strong>Desafio Relâmpago COPS:</strong><br>Qual é o hormônio responsável pela regulação da osmolaridade e reabsorção de água nos túbulos renais?<br><strong style='color:var(--accent-amber);'>Resposta: ADH (Hormônio Antidiurético / Vasopressina).</strong>";
        }
    }

    // --- Ferramentas Auxiliares & LocalStorage ---
    function toggleTool(drawerId) {
        const drawer = document.getElementById(drawerId);
        if (drawer) {
            drawer.style.display = drawer.style.display === 'block' ? 'none' : 'block';
        }
    }

    document.addEventListener("DOMContentLoaded", () => {
        const savedNotes = localStorage.getItem('nexo_quick_notes');
        if (savedNotes) {
            const notesEl = document.getElementById('quickNotes');
            if (notesEl) notesEl.value = savedNotes;
        }
    });

    function salvarNotas() {
        const notesEl = document.getElementById('quickNotes');
        if (notesEl) {
            localStorage.setItem('nexo_quick_notes', notesEl.value);
        }
    }

    function calcularResultado() {
        const exprInput = document.getElementById('calcInput');
        const resultEl = document.getElementById('calcResult');
        if (!exprInput || !resultEl) return;
        const expr = exprInput.value;
        try {
            const res = Function('"use strict";return (' + expr + ')')();
            resultEl.innerText = "Resultado: " + res;
        } catch (e) {
            resultEl.innerText = "Expressão inválida.";
        }
    }

    // --- Integrações Seguras com o Backend Local ---
    let simuladoData = null;
    let currentQuestionIndex = 0;
    let respostasAluno = {};

    async function carregarBlocoDiario() {
        const box = document.getElementById('blockResponse');
        if (!box) return;
        box.style.display = 'block';
        box.innerText = "A carregar bloco diário de 20 questões...";
        try {
            const res = await fetch(`http://127.0.0.1:8000/api/v1/blocks/daily`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();
            box.innerText = JSON.stringify(data, null, 2);
        } catch (err) {
            box.innerText = "Erro ao carregar o bloco diário: " + err + "\n(Certifique-se de que o backend local está ativo em http://127.0.0.1:8000)";
        }
    }

    async function carregarRecomposicao() {
        const attemptIdEl = document.getElementById('attemptId');
        const container = document.getElementById('recompositionContentContainer');
        const box = document.getElementById('ackResponse');
        if (!attemptIdEl || !container || !box) return;

        const attemptId = attemptIdEl.value;
        box.style.display = 'none';
        container.style.display = 'block';
        document.getElementById('gapInfo').innerText = "A carregar...";
        document.getElementById('microRevisaoInfo').innerText = "A carregar...";
        document.getElementById('exercicioInfo').innerText = "A carregar...";
        try {
            const res = await fetch(`http://127.0.0.1:8000/api/v1/recompositions/${attemptId}`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();
            document.getElementById('gapInfo').innerText = (data.discipline || "Geral") + " — " + (data.learning_gap || "Lacuna identificada");
            document.getElementById('microRevisaoInfo').innerText = data.micro_revisao || "Sem microrevisão disponível.";
            document.getElementById('exercicioInfo').innerText = data.exercicio_validacao || "Sem exercício de validação.";
        } catch (err) {
            document.getElementById('gapInfo').innerText = "Erro ao ligar ao backend: " + err;
        }
    }

    async function enviarAcknowledge() {
        const attemptId = document.getElementById('attemptId').value;
        const command = document.getElementById('commandInput').value;
        const box = document.getElementById('ackResponse');
        if (!box) return;
        box.style.display = 'block';
        box.innerText = "A processar validação no backend...";
        try {
            const res = await fetch(`http://127.0.0.1:8000/api/v1/recompositions/${attemptId}/acknowledge`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: command })
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();
            box.innerText = JSON.stringify(data, null, 2);
        } catch (err) {
            box.innerText = "Erro de ligação: " + err;
        }
    }

    async function carregarSimulado() {
        const container = document.getElementById('simulatedContainer');
        const box = document.getElementById('simResponse');
        if (!container || !box) return;
        container.style.display = 'block';
        box.style.display = 'none';
        document.getElementById('questionBox').innerText = "A descarregar simulado oficial da UEL...";
        try {
            const res = await fetch(`http://127.0.0.1:8000/api/v1/simulated/full`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            simuladoData = await res.json();
            currentQuestionIndex = 0;
            respostasAluno = {};
            iniciarContadorSimulado();
            exibirQuestaoAtual();
        } catch (err) {
            document.getElementById('questionBox').innerText = "Erro ao carregar simulado: " + err + "\n(Certifique-se de que o backend está ativo).";
        }
    }

    function exibirQuestaoAtual() {
        if (!simuladoData || !simuladoData.questions) return;
        const q = simuladoData.questions[currentQuestionIndex];
        let html = `<strong style="color:var(--accent-amber);">Questão ${q.id || (currentQuestionIndex + 1)} de ${simuladoData.total_questions || simuladoData.questions.length} [${q.discipline || 'UEL'}]</strong><p style="margin-top:8px; color:var(--text-main);">${q.enunciado || q.text || ''}</p>`;
        
        const alternativas = q.alternatives || q.opcoes || [];
        alternativas.forEach((alt, idx) => {
            const letra = String.fromCharCode(65 + idx);
            const checked = respostasAluno[q.id || currentQuestionIndex] === letra ? 'checked' : '';
            html += `<label style="display:block; margin-top:8px; font-weight:normal; cursor:pointer; color:var(--text-muted);"><input type="radio" name="q_current" value="${letra}" onclick="registraResposta(${q.id || currentQuestionIndex}, '${letra}')" ${checked}> ${alt}</label>`;
        });
        document.getElementById('questionBox').innerHTML = html;
    }

    function registraResposta(qid, alt) { 
        respostasAluno[qid] = alt; 
    }

    function proximaQuestao() { 
        if (simuladoData && simuladoData.questions && currentQuestionIndex < simuladoData.questions.length - 1) { 
            currentQuestionIndex++; 
            exibirQuestaoAtual(); 
        } 
    }

    function questaoAnterior() { 
        if (simuladoData && simuladoData.questions && currentQuestionIndex > 0) { 
            currentQuestionIndex--; 
            exibirQuestaoAtual(); 
        } 
    }

    async function submeterSimulado() {
        const box = document.getElementById('simResponse');
        if (!box) return;
        box.style.display = 'block';
        box.innerText = "A submeter e avaliar simulado...";
        try {
            const res = await fetch(`http://127.0.0.1:8000/api/v1/simulated/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ answers: respostasAluno })
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();
            box.innerText = JSON.stringify(data, null, 2);
            if (timerSimuladoInterval) clearInterval(timerSimuladoInterval);
        } catch (err) { 
            box.innerText = "Erro ao submeter simulado: " + err; 
        }
    }

    async function enviarDiscursiva() {
        const title = document.getElementById('examTitle').value;
        const proposal_content = document.getElementById('proposalContent').value;
        const student_answer = document.getElementById('studentAnswer').value;
        const box = document.getElementById('discResponse');
        if (!box) return;
        box.style.display = 'block';
        box.innerText = "A submeter prova discursiva...";
        try {
            const res = await fetch(`http://127.0.0.1:8000/api/v1/discursive/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, proposal_content, student_answer })
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();
            box.innerText = JSON.stringify(data, null, 2);
        } catch (err) { 
            box.innerText = "Erro de ligação: " + err; 
        }
    }
</script>

</body>
</html>
