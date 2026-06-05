# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página - Deve ser a primeira linha do Streamlit
st.set_page_config(page_title="ClimaEng", page_icon="🏗️", layout="wide")

# --- ESTADO DA SESSÃO ---
# Usado para guardar os resultados do questionário e mostrar no dashboard
if 'respostas' not in st.session_state:
    st.session_state['respostas'] = None

# --- ESTILO CSS INJETADO (ESTÉTICA PREMIUM) ---
st.markdown("""
<style>
    /* Importando a fonte Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Configurações globais de fonte */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Títulos e Subtítulos principais */
    h1 {
        font-weight: 700 !important;
        color: #0f172a !important;
        letter-spacing: -0.025em;
    }
    
    h2, h3 {
        font-weight: 600 !important;
        color: #1e293b !important;
        letter-spacing: -0.02em;
    }
    
    /* Estilizando a barra lateral */
    section[data-testid="stSidebar"] {
        background-image: linear-gradient(180deg, #0f172a, #1e293b) !important;
        color: #f8fafc !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Configuração de títulos e textos gerais na barra lateral */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] caption {
        color: #ffffff !important;
    }
    
    /* Rótulos e textos descritivos gerais */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] {
        color: #cbd5e1 !important; /* Slate 300 para melhor contraste secundário */
    }
    
    /* Estilização específica do menu de Rádio transformado em Menu de Navegação */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-testid="stWidgetLabel"]) {
        padding: 8px 14px !important;
        margin-bottom: 6px !important;
        border-radius: 10px !important;
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        transition: all 0.2s ease-in-out !important;
        cursor: pointer !important;
    }
    
    /* Efeito de hover nas opções do menu */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-testid="stWidgetLabel"]):hover {
        background-color: rgba(14, 165, 233, 0.08) !important;
        border-color: rgba(14, 165, 233, 0.2) !important;
        transform: translateX(4px);
    }
    
    /* Item selecionado ganha destaque premium (fundo azul semi-transparente) */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-testid="stWidgetLabel"]):has(input:checked) {
        background-image: linear-gradient(90deg, rgba(14, 165, 233, 0.2), rgba(2, 132, 199, 0.15)) !important;
        border-color: rgba(14, 165, 233, 0.4) !important;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.1) !important;
    }
    
    /* Cor do texto para todas as opções de rádio (tornar legível) */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-testid="stWidgetLabel"]) div div {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: color 0.2s ease;
    }
    
    /* Texto da opção selecionada fica branco brilhante e bold */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-testid="stWidgetLabel"]):has(input:checked) div div {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Estilizando caixas de informação e alertas */
    .stAlert {
        border-radius: 12px !important;
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        background-color: #f8fafc !important;
    }
    
    /* Estilizando formulário e sliders */
    .stForm {
        border-radius: 16px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 2.5rem !important;
        background-color: #ffffff;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Estilizando os botões */
    .stButton>button {
        background-image: linear-gradient(90deg, #0284c7, #0369a1) !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 6px -1px rgba(2, 132, 199, 0.2) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(2, 132, 199, 0.3) !important;
        border: none !important;
    }
    
    /* Estilizando abas (tabs) */
    button[data-baseweb="tab"] {
        font-weight: 500 !important;
        color: #64748b !important;
        transition: all 0.2s;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #0284c7 !important;
        font-weight: 600 !important;
        border-bottom-color: #0284c7 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- MENU LATERAL ---
st.sidebar.title("🏗️ ClimaEng")
st.sidebar.markdown("Ferramenta de Diagnóstico de Clima Ético e Comunicação")
pagina = st.sidebar.radio(
    "Navegue pelas etapas:",
    ["1. Início e Contexto", "2. Ferramenta de Diagnóstico", "3. Dashboard de Gestão", "4. Playbook Educativo"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Projeto Final - TEP 2 - 2026.1")

# --- PÁGINA 1: INÍCIO E CONTEXTO ---
if pagina == "1. Início e Contexto":
    st.title("Bem-vindo ao ClimaEng 🛠️")
    st.subheader("Transformando ambientes técnicos através da segurança psicológica")
    
    st.markdown("""
    ### A Interseção entre Engenharia, Ética e Sistemas Sociotécnicos
    
    Projetos de engenharia de alta complexidade frequentemente não falham por inaptidão técnica, mas por colapsos na comunicação interna, hierarquias excessivamente rígidas e uma cultura organizacional punitiva.
    
    Sistemas de engenharia são, fundamentalmente, **sistemas sociotécnicos** — onde a infraestrutura técnica e os fatores humanos estão profundamente entrelaçados. Quando os profissionais sentem medo de reportar falhas ou expressar divergências, riscos conhecidos pela base operacional são omitidos, criando o cenário ideal para falhas catastróficas.
    
    O **ClimaEng** é uma ferramenta de diagnóstico e educação desenvolvida para avaliar a percepção ética, segurança psicológica e barreiras de comunicação em equipes técnicas. O objetivo é substituir a cultura de culpabilização por um ambiente de aprendizado contínuo, mitigando o risco de silêncio institucional.
    """)
    
    st.markdown("---")
    st.markdown("### Por que focar na Segurança Psicológica?")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            """
            <div style="background-color: #f0f9ff; border-left: 5px solid #0284c7; padding: 1.5rem; border-radius: 8px; height: 160px;">
                <h4 style="margin: 0 0 0.5rem 0; color: #0369a1;">📉 Redução de Riscos</h4>
                <p style="margin: 0; color: #334155; font-size: 0.9rem;">
                    Equipes com alta segurança psicológica detectam e corrigem falhas técnicas até <b>40% mais rápido</b> antes que se tornem incidentes de segurança reais.
                </p>
            </div>
            """, unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            """
            <div style="background-color: #f0fdf4; border-left: 5px solid #22c55e; padding: 1.5rem; border-radius: 8px; height: 160px;">
                <h4 style="margin: 0 0 0.5rem 0; color: #166534;">💡 Inovação e Qualidade</h4>
                <p style="margin: 0; color: #334155; font-size: 0.9rem;">
                    A liberdade para dissentir tecnicamente e propoe soluções alternativas aumenta a qualidade das revisões de design de engenharia em <b>30%</b>.
                </p>
            </div>
            """, unsafe_allow_html=True
        )
    with m3:
        st.markdown(
            """
            <div style="background-color: #fffbeb; border-left: 5px solid #f59e0b; padding: 1.5rem; border-radius: 8px; height: 160px;">
                <h4 style="margin: 0 0 0.5rem 0; color: #92400e;">🤝 Retenção de Talentos</h4>
                <p style="margin: 0; color: #334155; font-size: 0.9rem;">
                    A segurança psicológica é o indicador número um de retenção e bem-estar de engenheiros em ambientes técnicos de alta pressão.
                </p>
            </div>
            """, unsafe_allow_html=True
        )
        
    st.markdown("---")
    st.markdown("### Como utilizar o ClimaEng?")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🔍 **1. Faça o Diagnóstico**\n\nAcesse a aba lateral e responda com sinceridade às 9 perguntas da ferramenta. Suas respostas são totalmente anônimas e servem para mapear a saúde do clima organizacional.")
    with col2:
        st.warning("📊 **2. Analise os Gráficos**\n\nNo Dashboard de Gestão, veja a distribuição das notas da sua equipe, os pilares em estado crítico e as projeções de riscos baseadas nas respostas.")
    with col3:
        st.success("📘 **3. Aplique Intervenções**\n\nConsulte o Playbook Educativo para acessar ferramentas como o roteiro de Post-Mortem Sem Culpa, guias de liderança inclusiva e estudos de caso históricos.")

# --- PÁGINA 2: DIAGNÓSTICO ---
elif pagina == "2. Ferramenta de Diagnóstico":
    st.title("📋 Diagnóstico de Clima Organizacional")
    st.markdown("Avalie a percepção do seu ambiente de trabalho de engenharia. As respostas a este formulário geram dados agregados que servem para identificar gargalos e riscos psicossociais. **Suas respostas são estritamente confidenciais.**")
    
    with st.form("form_diagnostico"):
        st.markdown("""
        <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem;">
            <h4 style="margin:0; color:#334155;">Escala de Avaliação</h4>
            <p style="margin: 0.5rem 0 0 0; color: #64748b; font-size: 0.9rem;">
                <b>1:</b> Discordo Totalmente | <b>2:</b> Discordo Parcialmente | <b>3:</b> Neutro | <b>4:</b> Concordo Parcialmente | <b>5:</b> Concordo Totalmente
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("🛡️ Pilar 1: Segurança Psicológica")
        st.markdown("*Mede a segurança compartilhada pela equipe de que o ambiente é seguro para assumir riscos interpessoais sem medo de constrangimento ou punição.*")
        q1 = st.slider("1. Sinto-me seguro para reportar falhas técnicas ou apontar riscos no projeto sem medo de sofrer retaliações ou punições da liderança.", 1, 5, 3)
        q2 = st.slider("2. Minhas ideias, preocupações e opiniões são valorizadas e ouvidas com respeito pela equipe, independentemente do meu cargo ou senioridade.", 1, 5, 3)
        q3 = st.slider("3. Nesta equipe, é fácil e seguro admitir erros, pedir ajuda ou sinalizar que não sei algo quando enfrento dificuldades técnicas.", 1, 5, 3)
        
        st.markdown("---")
        st.subheader("🗣️ Pilar 2: Comunicação e Hierarquia")
        st.markdown("*Mede a transparência no fluxo de informações de engenharia e se as posições de poder dificultam ou facilitam o reporte de inconformidades.*")
        q4 = st.slider("4. A liderança comunica decisões críticas de forma clara e transparente, oferecendo espaço real para questionamentos técnicos.", 1, 5, 3)
        q5 = st.slider("5. Sinto que a hierarquia organizacional não é um obstáculo para que informações técnicas críticas cheguem à diretoria ou à alta gestão.", 1, 5, 3)
        q6 = st.slider("6. Existe espaço e incentivo explícito para expressar divergências e opiniões contrárias (dissenso técnico) durante revisões de projeto.", 1, 5, 3)
        
        st.markdown("---")
        st.subheader("⚖️ Pilar 3: Resolução de Conflitos e Ética")
        st.markdown("*Avalia como a equipe trata discordâncias técnicas e se a liderança apoia o comportamento ético frente à pressão comercial de prazos.*")
        q7 = st.slider("7. Conflitos técnicos e discussões de projeto são mediados com foco na análise de fatos e resolução do problema, e não em ataques pessoais.", 1, 5, 3)
        q8 = st.slider("8. Há diretrizes claras e canais seguros/confidenciais para reportar desvios éticos, assédio moral ou violações de normas técnicas.", 1, 5, 3)
        q9 = st.slider("9. A liderança e a empresa priorizam a integridade ética, a segurança e a qualidade do produto acima do cumprimento cego de prazos e metas.", 1, 5, 3)
        
        submit = st.form_submit_button("Gerar Diagnóstico")
        
        if submit:
            # Calculando médias por pilar (3 perguntas por pilar)
            media_psi = (q1 + q2 + q3) / 3
            media_com = (q4 + q5 + q6) / 3
            media_con = (q7 + q8 + q9) / 3
            media_geral = (media_psi + media_com + media_con) / 3
            
            # Salvando na sessão
            st.session_state['respostas'] = {
                'Segurança Psicológica': media_psi,
                'Comunicação e Hierarquia': media_com,
                'Gestão de Conflitos': media_con,
                'Média Geral': media_geral
            }
            st.success("Diagnóstico concluído com sucesso! Vá para a aba '3. Dashboard de Gestão' para visualizar os resultados detalhados e as recomendações.")

# --- PÁGINA 3: DASHBOARD ---
elif pagina == "3. Dashboard de Gestão":
    st.title("📈 Dashboard de Análise Organizacional")
    
    if st.session_state['respostas'] is None:
        st.warning("Nenhum dado real foi inserido. Abaixo estão exibidos dados simulados para demonstração do dashboard. Preencha a 'Ferramenta de Diagnóstico' para gerar a análise do seu caso.")
        
        # Dados simulados
        dados = {
            'Segurança Psicológica': 2.33,
            'Comunicação e Hierarquia': 1.67,
            'Gestão de Conflitos': 3.33,
            'Média Geral': 2.44
        }
    else:
        dados = st.session_state['respostas']

    # Métricas Iniciais em Cards Premium
    st.markdown("### Painel Geral de Clima")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Função para definir cor baseada na nota
    def obter_status_texto(nota):
        if nota >= 4.0:
            return "Excelente", "#16a34a"
        elif 2.5 <= nota < 4.0:
            return "Alerta", "#d97706"
        else:
            return "Crítico", "#dc2626"
            
    status_geral, cor_geral = obter_status_texto(dados['Média Geral'])
    status_psi, cor_psi = obter_status_texto(dados['Segurança Psicológica'])
    status_com, cor_com = obter_status_texto(dados['Comunicação e Hierarquia'])
    status_con, cor_con = obter_status_texto(dados['Gestão de Conflitos'])
    
    with col1:
        st.markdown(
            f"""
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 1.25rem; border-radius: 12px; text-align: center;">
                <p style="margin: 0; color: #64748b; font-size: 0.85rem; font-weight: 500; text-transform: uppercase;">Média Geral</p>
                <h2 style="margin: 0.5rem 0 0.25rem 0; color: {cor_geral}; font-size: 2rem; font-weight: 700;">{dados['Média Geral']:.2f} <span style="font-size: 1rem; color: #94a3b8;">/ 5.0</span></h2>
                <span style="background-color: {cor_geral}15; color: {cor_geral}; padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">{status_geral}</span>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 1.25rem; border-radius: 12px; text-align: center;">
                <p style="margin: 0; color: #64748b; font-size: 0.85rem; font-weight: 500; text-transform: uppercase;">Segurança Psicológica</p>
                <h2 style="margin: 0.5rem 0 0.25rem 0; color: {cor_psi}; font-size: 2rem; font-weight: 700;">{dados['Segurança Psicológica']:.2f} <span style="font-size: 1rem; color: #94a3b8;">/ 5.0</span></h2>
                <span style="background-color: {cor_psi}15; color: {cor_psi}; padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">{status_psi}</span>
            </div>
            """, unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 1.25rem; border-radius: 12px; text-align: center;">
                <p style="margin: 0; color: #64748b; font-size: 0.85rem; font-weight: 500; text-transform: uppercase;">Comunicação e Hierarquia</p>
                <h2 style="margin: 0.5rem 0 0.25rem 0; color: {cor_com}; font-size: 2rem; font-weight: 700;">{dados['Comunicação e Hierarquia']:.2f} <span style="font-size: 1rem; color: #94a3b8;">/ 5.0</span></h2>
                <span style="background-color: {cor_com}15; color: {cor_com}; padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">{status_com}</span>
            </div>
            """, unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            f"""
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 1.25rem; border-radius: 12px; text-align: center;">
                <p style="margin: 0; color: #64748b; font-size: 0.85rem; font-weight: 500; text-transform: uppercase;">Gestão de Conflitos e Ética</p>
                <h2 style="margin: 0.5rem 0 0.25rem 0; color: {cor_con}; font-size: 2rem; font-weight: 700;">{dados['Gestão de Conflitos']:.2f} <span style="font-size: 1rem; color: #94a3b8;">/ 5.0</span></h2>
                <span style="background-color: {cor_con}15; color: {cor_con}; padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">{status_con}</span>
            </div>
            """, unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # Layout em duas colunas: Gráfico Radar à esquerda, diagnóstico de maturidade à direita
    col_chart, col_diagnostico = st.columns([1.2, 1])
    
    with col_chart:
        st.markdown("### Mapeamento de Riscos (Perfil de Radar)")
        categorias = ['Segurança Psicológica', 'Comunicação e Hierarquia', 'Gestão de Conflitos']
        valores = [dados['Segurança Psicológica'], dados['Comunicação e Hierarquia'], dados['Gestão de Conflitos']]
        
        fig_radar = go.Figure(data=go.Scatterpolar(
          r=valores + [valores[0]], # Fecha o polígono
          theta=categorias + [categorias[0]],
          fill='toself',
          fillcolor='rgba(14, 165, 233, 0.2)', # Teal / Light blue
          line=dict(color='#0ea5e9', width=3),
          marker=dict(color='#0284c7', size=8)
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5],
                    tickfont=dict(size=10, color="#64748b"),
                    gridcolor="#e2e8f0"
                ),
                angularaxis=dict(
                    tickfont=dict(size=12, family="Inter", color="#334155"),
                    gridcolor="#e2e8f0"
                ),
                bgcolor="rgba(255, 255, 255, 0)"
            ),
            showlegend=False,
            margin=dict(l=40, r=40, t=20, b=20),
            height=320
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
    with col_diagnostico:
        st.markdown("### Avaliação de Maturidade Sociotécnica")
        if dados['Média Geral'] >= 4.0:
            st.success("""
            **Nível de Maturidade: ALTO (Cultura Segura e Aprendente)**
            
            A equipe apresenta um ambiente propício à inovação e confiabilidade técnica. O silêncio institucional é mínimo.
            
            * **Ponto Forte:** Há transparência e segurança para reportar falhas.
            * **Recomendação:** Continue incentivando o dissenso técnico e documentando as lições aprendidas nos rituais atuais.
            """)
        elif 2.5 <= dados['Média Geral'] < 4.0:
            st.warning("""
            **Nível de Maturidade: MÉDIO (Ambiente em Estado de Alerta)**
            
            Existem atritos de comunicação ou canais que geram receio moderado na equipe. Riscos técnicos ou pequenos desvios de processo podem estar sendo acobertados ou ignorados temporariamente para evitar conflitos.
            
            * **Ponto Crítico:** Alguns membros hesitam em discordar publicamente da gestão.
            * **Recomendação:** A liderança deve formalizar dinâmicas de feedback anônimo e reforçar a segurança nas reuniões.
            """)
        else:
            st.error("""
            **Nível de Maturidade: BAIXO (Cultura Punitiva ou Silenciada)**
            
            Alto risco sociotécnico e psicológico. Há indícios severos de silêncio institucional, onde problemas de qualidade ou segurança são retidos devido ao medo de punição, ridicularização ou demissão.
            
            * **Risco Imediato:** Perigo de falha operacional grave por falta de fluxo de informação crítica.
            * **Recomendação:** Intervenção urgente. Necessário desatar nós de poder de lideranças imediatas e instituir canais de ouvidoria externos e independentes.
            """)
            
    st.markdown("---")
    st.markdown("### Análise Dinâmica e Recomendações por Pilar")
    
    # Seção detalhada para cada pilar dependendo do seu valor
    p1_col, p2_col, p3_col = st.columns(3)
    
    with p1_col:
        st.markdown("#### 🛡️ Segurança Psicológica")
        nota_p1 = dados['Segurança Psicológica']
        if nota_p1 >= 4.0:
            st.markdown("""
            **Avaliação:** Saudável e Receptiva.
            
            **Ação sugerida:** A equipe admite falhas sem medo de punições. Para manter este patamar, implemente a prática sistemática de *Post-Mortem Sem Culpa* nas revisões de entregas críticas.
            """)
        elif 2.5 <= nota_p1 < 4.0:
            st.markdown("""
            **Avaliação:** Vulnerável / Sob Pressão.
            
            **Ação sugerida:** O medo do erro está presente em alguns momentos. Os gestores devem liderar com vulnerabilidade, admitindo seus próprios erros em reuniões de alinhamento para diminuir a barreira do medo do fracasso.
            """)
        else:
            st.markdown("""
            **Avaliação:** Crítica / Cultura de Culpa.
            
            **Ação sugerida:** O erro é tratado como falha individual. É crucial realizar um reset de governança na equipe, proibindo explicitamente a atribuição de culpa individual em relatórios técnicos de falhas de software ou projeto.
            """)
            
    with p2_col:
        st.markdown("#### 🗣️ Comunicação e Hierarquia")
        nota_p2 = dados['Comunicação e Hierarquia']
        if nota_p2 >= 4.0:
            st.markdown("""
            **Avaliação:** Fluxo Aberto de Dissenso.
            
            **Ação sugerida:** A liderança incentiva opiniões divergentes e a tomada de decisão técnica é descentralizada. Foque em manter reuniões com tempos de fala equilibrados (*conversational turn-taking*).
            """)
        elif 2.5 <= nota_p2 < 4.0:
            st.markdown("""
            **Avaliação:** Comunicação Unilateral.
            
            **Ação sugerida:** Decisões descem sem contextualização e questionar as lideranças é desconfortável. Recomenda-se realizar retrospectivas de clima periódicas usando painéis virtuais anônimos (ex: Miro/Mural).
            """)
        else:
            st.markdown("""
            **Avaliação:** Hierarquia Punitiva / Silenciamento.
            
            **Ação sugerida:** Engenheiros de base evitam fazer perguntas ou apontar riscos devido a uma barreira hierárquica intransponível. Implemente canais diretos de comunicação executiva \"pule uma linha\" (skip-level).
            """)
            
    with p3_col:
        st.markdown("#### ⚖️ Resolução de Conflitos e Ética")
        nota_p3 = dados['Gestão de Conflitos']
        if nota_p3 >= 4.0:
            st.markdown("""
            **Avaliação:** Ética e Foco no Processo.
            
            **Ação sugerida:** As divergências são profissionais e a ética prevalece. Recomenda-se apenas realizar feedbacks cruzados para verificar a manutenção destas dinâmicas.
            """)
        elif 2.5 <= nota_p3 < 4.0:
            st.markdown("""
            **Avaliação:** Atrito e Foco nas Pessoas.
            
            **Ação sugerida:** Conflitos às vezes descambam para o pessoal ou há desvios de processo para atingir metas comerciais de prazos. Recomenda-se alinhar acordos de convivência e definir limites claros para a pressa de entrega.
            """)
        else:
            st.markdown("""
            **Avaliação:** Risco Ético Grave.
            
            **Ação sugerida:** Elevada pressão gerencial atropela a ética, o cumprimento das normas e o respeito básico. É recomendada a suspensão ou revisão imediata dos indicadores de metas punitivas do projeto.
            """)

# --- PÁGINA 4: PLAYBOOK EDUCATIVO ---
elif pagina == "4. Playbook Educativo":
    st.title("📘 Playbook de Cultura Segura e Ética")
    st.markdown("Guia conceitual, ferramentas práticas e estudos de caso focados no desenvolvimento sociotécnico de equipes de engenharia.")
    
    tab1, tab2, tab3 = st.tabs(["📚 Fundamentos", "🎓 Estudos de Caso Históricos", "⚙️ Protocolos de Ação"])
    
    with tab1:
        st.subheader("Bases Teóricas da Segurança Psicológica")
        
        st.markdown("""
        #### 1. Segurança Psicológica vs. Confiança
        Muitas vezes esses conceitos são confundidos, mas eles operam em níveis diferentes:
        * **Confiança:** Foca no nível individual. É a crença de que *uma pessoa específica* agirá de forma correta e previsível. (ex: *\"Eu confio que o engenheiro João fará uma boa revisão deste cálculo\"*).
        * **Segurança Psicológica:** Foca no nível do grupo/equipe. É a percepção coletiva de que a equipe não vai punir, humilhar ou retaliar quem expuser uma fraqueza ou cometer um erro. (ex: *\"Nesta equipe, qualquer um de nós se sente seguro para admitir no Slack que deletou acidentalmente a base de dados de testes\"*).
        
        #### 2. Os 4 Estágios da Segurança Psicológica (Timothy Clark)
        A segurança psicológica não é binária. Ela se desenvolve em fases progressivas:
        1. **Segurança de Inclusão:** Sentir-se aceito como membro da equipe, valorizado pela sua identidade e não apenas pela sua utilidade.
        2. **Segurança de Aprendizagem:** Sentir-se seguro para fazer perguntas, dar e receber feedbacks, experimentar e cometer erros durante o aprendizado.
        3. **Segurança de Contribuição:** Sentir-se seguro para usar suas habilidades para fazer uma diferença real, participando de discussões ativamente.
        4. **Segurança de Desafio:** O nível mais alto. Sentir-se seguro para desafiar o *status quo*, decisões de superiores ou práticas vigentes quando achar que há um risco técnico ou ético.
        
        #### 3. Os 3 Tipos de Silêncio Organizacional
        Por que as pessoas se calam? O silêncio não é apenas a falta de fala:
        * **Silêncio Aquiescente:** Postura resignada baseada na crença de que *\"falar não fará diferença\"* ou *\"nada vai mudar mesmo\"*.
        * **Silêncio Defensivo:** Postura de autoproteção baseada no medo. *\"Se eu falar, serei punido, visto como criador de problemas ou demitido\"*.
        * **Silêncio Prosocial:** Postura de reter informações com a intenção benevolente de proteger os colegas ou a organização de constrangimentos.
        """)
        
    with tab2:
        st.subheader("Estudos de Caso: Quando o Silêncio Custa Vidas")
        
        st.markdown("""
        O silêncio institucional e a ausência de segurança psicológica são os fatores causais ocultos por trás de grandes tragédias da engenharia moderna.
        """)
        
        with st.expander("🚀 1. O Desastre do Ônibus Espacial Challenger (1986)"):
            st.markdown("""
            **O Contexto:**
            Na noite anterior ao lançamento do ônibus espacial Challenger em 28 de janeiro de 1986, engenheiros da empresa contratada Morton Thiokol alertaram os gestores da NASA de que as temperaturas congelantes previstas para a Flórida comprometeriam a elasticidade dos anéis de vedação de borracha (O-rings) dos foguetes propulsores.
            
            **O Ponto de Ruptura Ético e Hierárquico:**
            Durante uma teleconferência crucial, gerentes da NASA reagiram de forma agressiva aos dados apresentados pelos engenheiros, exigindo que eles \"provassem que o lançamento seria inseguro\", invertendo o ônus da prova padrão de engenharia espacial (onde se deve provar que o voo é *seguro*). 
            Sob forte pressão, um gerente sênior da Morton Thiokol disse ao diretor de engenharia: *\"Tire o chapéu de engenheiro e coloque o de gestor\"*. O diretor capitulou, o aviso foi suprimido e a equipe assinou a autorização de voo contra a vontade dos técnicos de base.
            
            **A Consequência:**
            73 segundos após o lançamento, os O-rings falharam devido ao frio. O ônibus espacial explodiu, matando os sete tripulantes.
            
            **A Lição Sociotécnica:**
            A comissão de investigação revelou que a cultura da NASA havia desenvolvido uma complacência com o risco e uma hierarquia tão punitiva que engenheiros que queriam insistir nos alertas de segurança se calaram para proteger suas carreiras.
            """)
            
        with st.expander("✈️ 2. A Crise do Boeing 737 MAX (2018-2019)"):
            st.markdown("""
            **O Contexto:**
            Para concorrer rapidamente com o Airbus A320neo, a Boeing redesenhou o 737 instalando motores maiores e mais à frente na asa. Para compensar a tendência do bico da aeronave subir em certas manobras, a engenharia introduziu um sistema automático de software chamado MCAS (Maneuvering Characteristics Augmentation System).
            
            **O Ponto de Ruptura Ético e Hierárquico:**
            Para evitar que as companhias aéreas exigissem treinamento caro em simuladores para seus pilotos, a gestão da Boeing decidiu ocultar a existência do MCAS dos manuais e remover sensores redundantes do sistema. Engenheiros de testes e pilotos técnicos que questionaram essa postura de design foram desencorajados e repreendidos de forma velada.
            
            A cultura da empresa havia migrado de uma cultura focada estritamente na excelência de engenharia para uma cultura financeira focada no valor das ações e cumprimento de prazos. Mensagens internas revelaram engenheiros dizendo: *\"Este avião foi desenhado por palhaços que por sua vez são supervisionados por macacos\"*, demonstrando o profundo cinismo e a falta de canais de voz.
            
            **A Consequência:**
            Dois acidentes fatais na Indonésia (2018) e Etiópia (2019) ocorreram após os sensores falharem, fazendo o MCAS empurrar o bico dos aviões repetidamente para baixo sem que os pilotos soubessem como desativá-lo. 346 pessoas morreram.
            
            **A Lição Sociotécnica:**
            A ausência de segurança psicológica na Boeing permitiu que uma decisão de design falha e antiética avançasse sem questionamentos, pois os engenheiros temiam retaliações internas caso atrasassem os cronogramas de entrega.
            """)
            
    with tab3:
        st.subheader("Ferramentas de Intervenção Organizacional")
        
        st.markdown("""
        Abaixo estão três protocolos práticos que podem ser implementados imediatamente para mudar a cultura da equipe técnica.
        """)
        
        with st.expander("📋 1. Protocolo de Post-Mortem Sem Culpa (Blameless Post-Mortem)"):
            st.markdown("""
            **O que é:**
            Um ritual técnico realizado após uma falha de sistema (bug em produção, atraso de entrega crítica ou quebra de qualidade) onde o foco é compreender o contexto sistêmico do erro, e não punir o indivíduo que cometeu a ação.
            
            **Regras de Ouro:**
            1. **Premissa de Boa Fé:** Devemos assumir que todo engenheiro tomou a melhor decisão possível com base nas informações que possuía no momento.
            2. **Foco no \"Como\" e não no \"Quem\":** Perguntar *\"Como o nosso sistema de monitoramento falhou em detectar isso?\"* ou *\"Como o nosso processo permitiu que esse código subisse?\"* em vez de *\"Quem escreveu essa linha de código?\"*.
            3. **Ações Preventivas:** O resultado final do post-mortem deve ser uma lista de melhorias técnicas ou processuais para evitar a recorrência, nunca punições.
            
            **Template de Ata Rápida:**
            * **Resumo do Incidente:** O que aconteceu e qual foi o impacto?
            * **Linha do Tempo:** Desde a primeira ação até a mitigação final do problema.
            * **Fatores Contribuintes:** Que processos falharam? Que ferramentas faltaram?
            * **Planos de Ação (Próximos Passos):** Quem vai corrigir a vulnerabilidade estrutural e qual o prazo?
            """)
            
        with st.expander("🗣️ 2. Prática dos Círculos de Escuta"):
            st.markdown("""
            **O que é:**
            Uma reunião mensal de 1 hora dedicada exclusivamente à saúde do clima do time. O trabalho técnico de codificação ou projeto não é discutido.
            
            **Estrutura:**
            1. **Início sem Status:** Cada membro compartilha em 2 minutos como está se sentindo em relação à carga de trabalho e pressões.
            2. **Uso de Conversational Turn-Taking:** O líder facilita para que todos tenham tempos iguais de fala, garantindo que membros introvertidos não fiquem de fora.
            3. **Fechamento de Acordos:** Discussão de pequenas mudanças nos processos do time para aliviar pontos de estresse identificados.
            """)
            
        with st.expander("💡 3. Guia da Liderança Inclusiva e Vulnerável"):
            st.markdown("""
            Se você lidera engenheiros, sua postura é o fator número um para criar segurança psicológica. Siga estas 3 diretrizes:
            * **Admitir Limitações:** Dizer com frequência *\"Eu não sei a resposta para isso, o que vocês acham?\"* ou *\"Cometi um erro na minha projeção de prazos da semana passada\"*. Isso autoriza a equipe a ser humana.
            * **Substituir Instrução por Curiosidade:** Fazer perguntas abertas como *\"Quais são os riscos invisíveis desse plano?\"* ou *\"Se fôssemos falhar nesse projeto, onde você acha que seria o ponto crítico?\"*.
            * **Agradecer Ativamente a Discordância:** Quando alguém trouxer um problema ou discordar, responder com: *\"Obrigado por trazer esse alerta técnico. Sei que não é fácil discordar do plano, mas precisamos dessa clareza\"*.
            """)
