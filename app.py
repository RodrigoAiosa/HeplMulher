import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração da Página
st.set_page_config(
    page_title="Detector de Riscos: Perfil de Agressor",
    page_icon="⚠️",
    layout="centered"
)

# FUNÇÃO DE LOG: Registra data/hora sempre que o app é carregado
def registrar_log():
    data_hora_acesso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log_acessos.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"Aplicativo acessado em: {data_hora_acesso}\n")

# Executa o log de acesso ao iniciar
registrar_log()

# CSS PARA DESIGN NEON (CÍRCULOS GRANDES) E FONTES 26px
st.markdown("""
<style>
    .main {background-color: #0e001a; color: white;}
    .stApp {background-color: #0e001a;}
    
    h1 {color: #bb86fc !important; text-align: center; font-size: 2.8rem !important; margin-bottom: 10px;}
    .intro-text {
        font-size: 16px; 
        color: #d1d1d1; 
        text-align: justify; 
        background: rgba(187, 134, 252, 0.1); 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 5px solid #bb86fc;
        margin-bottom: 30px;
        line-height: 1.6;
    }

    .pergunta {
        text-align: center; 
        font-size: 26px !important; 
        margin: 60px 0 30px; 
        color: #ffffff; 
        font-weight: 700;
        line-height: 1.4;
    }

    /* ESTILIZAÇÃO DOS BOTÕES RÁDIO NEON - IGUAL À IMAGEM */
    div.row-widget.stRadio > div {
        flex-direction: row !important; 
        justify-content: center !important; 
        gap: 40px !important;
    }

    div.row-widget.stRadio div[data-testid="stMarkdownContainer"] {
        display: none !important;
    }

    div.row-widget.stRadio label div[dir="ltr"] {
        background-color: #b784f7 !important;
        color: #000 !important;
        width: 85px !important;
        height: 85px !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 28px !important;
        font-weight: 900 !important;
        box-shadow: 0 0 25px rgba(183, 132, 247, 0.8) !important;
        border: none !important;
        margin-bottom: 15px !important;
        transition: all 0.3s ease;
    }

    div.row-widget.stRadio label p {
        font-size: 18px !important;
        color: #ffffff !important;
        font-weight: 500 !important;
        text-align: center;
    }

    div.row-widget.stRadio label[data-checked="true"] div[dir="ltr"] {
        background-color: #ffffff !important;
        box-shadow: 0 0 45px #b784f7 !important;
        transform: scale(1.15);
    }

    .resultado-box {
        background: linear-gradient(135deg, #1a0033, #2d0055);
        padding: 40px; border-radius: 25px; border: 3px solid #bb86fc;
        text-align: center; margin-top: 60px;
    }
    .pontuacao-num { font-size: 5rem; font-weight: 900; color: #bb86fc; }
</style>
""", unsafe_allow_html=True)

# Título Principal
st.markdown("<h1>Análise de Risco Comportamental</h1>", unsafe_allow_html=True)

# Texto Introdutório Justificando as Perguntas
st.markdown("""
<div class="intro-text">
    <b>Por que estas perguntas são vitais?</b><br>
    Este protocolo foi estruturado com base em estudos de <b>Psicologia Forense</b> e <b>Coerção Coercitiva</b>. 
    As perguntas identificam "preditores de alta letalidade". A ciência demonstra que o controle invisível 
    e o isolamento social antecedem a violência física grave. Responder a este questionário ajuda a 
    identificar o risco em estágios precoces antes que a integridade física seja comprometida.
</div>
""", unsafe_allow_html=True)

# Embasamento Científico no Topo
with st.expander("🔬 Ver Embasamento Científico e Referências"):
    st.markdown("""
    <div style="font-size:16px; color:#bbb;">
    1. <b>Modelo de Duluth:</b> Baseado na roda de poder e controle.<br>
    2. <b>Escala de Charlot (2025):</b> Focada na validade preditiva de sinais precoces.<br>
    3. <b>Danger Assessment:</b> Ferramenta padrão ouro para avaliar risco de feminicídio.<br><br>
    <b>Referências:</b><br>
    • Charlot, A. et al. (2025). <i>The Predictive Validity of IPV Warning Signs.</i><br>
    • Dutton, D. G. (2006). <i>The Abusive Personality.</i><br>
    • Pence, E. (1993). <i>The Duluth Model.</i>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border-color:#333'>", unsafe_allow_html=True)

# Configuração de Perguntas
opcoes = {1: "Nunca", 2: "Raro", 3: "Às vezes", 4: "Sempre"}
perguntas = [
    "Ele demonstra um senso de 'posse' ou autoridade superior sobre suas decisões?",
    "Ele tenta controlar o que você veste, com quem fala ou para onde vai?",
    "Ele desqualifica sua percepção da realidade (faz você duvidar da sua memória)?",
    "Ele demonstra ciúme excessivo e justifica isso como 'excesso de amor'?",
    "Ele monitora suas redes sociais, mensagens ou exige saber suas senhas?",
    "Ele isola você de sua rede de apoio (família/amigos) criticando-os constantemente?",
    "Há um ciclo de 'explosão de raiva' seguido por 'pedidos de desculpas intensos'?",
    "Ele pressiona ou obriga você a ter relações sexuais quando você não quer?",
    "Ele sabota seus métodos contraceptivos ou pressiona por uma gravidez?",
    "Ele costuma culpar você pelas reações agressivas dele?"
]

respostas = []
for i, p in enumerate(perguntas, 1):
    st.markdown(f'<div class="pergunta">{i}. {p}</div>', unsafe_allow_html=True)
    escolha = st.radio(
        label=f"q{i}", 
        options=[1, 2, 3, 4], 
        index=None, 
        horizontal=True, 
        key=f"q{i}", 
        format_func=lambda x: opcoes[x], 
        label_visibility="collapsed"
    )
    if escolha:
        respostas.append(escolha)

# Resultados e Registro de Dados de Resposta
if len(respostas) == len(perguntas):
    pontuacao_total = sum(respostas)
    data_hora_fim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Salva preservando dados anteriores [cite: 2026-01-18]
    with open("dados_analise.txt", "a", encoding="utf-8") as f:
        f.write(f"Teste Finalizado em: {data_hora_fim} | Pontos: {pontuacao_total} | Respostas: {respostas}\n")
    
    st.markdown("<div class='resultado-box'>", unsafe_allow_html=True)
    if pontuacao_total <= 18:
        nivel, cor, desc = "BAIXO RISCO", "#4caf50", "Mantenha sua autonomia preservada."
    elif pontuacao_total <= 28:
        nivel, cor, desc = "RISCO MODERADO", "#ffeb3b", "Procure apoio e fortaleça seus limites."
    else:
        nivel, cor, desc = "ALTO RISCO", "#f44336", "Procure ajuda profissional imediatamente."

    st.markdown(f"<h2 style='color:{cor}'>{nivel}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='pontuacao-num'>{pontuacao_total}/40</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:20px;'>{desc}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Rodapé
st.markdown("<br><br><br><div style='text-align:center; color:#888; font-size:16px;'>📞 Ajuda Imediata? <b>Disque 180</b></div>", unsafe_allow_html=True)
