import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# Configuração da Página
st.set_page_config(
    page_title="Detector de Riscos: Perfil de Agressor",
    page_icon="⚠️",
    layout="centered"
)

# Conexão com sua planilha específica
conn = st.connection("gsheets", type=GSheetsConnection)

# FUNÇÃO DE REGISTRO: Salva na planilha e em .txt local [cite: 2026-02-13, 2026-01-18]
def registrar_dados(pontos=None, respostas=None, tipo="acesso"):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Registro em .txt local (backup) [cite: 2026-02-13]
    with open("log_geral.txt", "a", encoding="utf-8") as f:
        f.write(f"{data_hora} | {tipo} | Pontos: {pontos} | Respostas: {respostas}\n")
    
    # Registro na Planilha Google (Sempre preservando dados) [cite: 2026-01-18]
    try:
        df_atual = conn.read(worksheet="Sheet1")
        novo_registro = pd.DataFrame([{
            "Data/Hora": data_hora, 
            "Tipo": tipo, 
            "Pontuacao": pontos, 
            "Respostas": str(respostas)
        }])
        df_final = pd.concat([df_atual, novo_registro], ignore_index=True)
        conn.update(worksheet="Sheet1", data=df_final)
    except Exception:
        # Se a planilha estiver vazia, cria o primeiro registro
        novo_registro = pd.DataFrame([{
            "Data/Hora": data_hora, 
            "Tipo": tipo, 
            "Pontuacao": pontos, 
            "Respostas": str(respostas)
        }])
        conn.update(worksheet="Sheet1", data=novo_registro)

# Log de acesso ao carregar
if 'log_feito' not in st.session_state:
    registrar_dados(tipo="Acesso ao App")
    st.session_state['log_feito'] = True

# CSS PARA DESIGN NEON (FONTES 26px E CÍRCULOS GRANDES) [cite: 2026-02-13]
st.markdown("""
<style>
    .main {background-color: #0e001a; color: white;}
    .stApp {background-color: #0e001a;}
    h1 {color: #bb86fc !important; text-align: center; font-size: 2.8rem !important; margin-bottom: 10px;}
    .intro-text {
        font-size: 16px; color: #d1d1d1; text-align: justify; 
        background: rgba(187, 134, 252, 0.1); padding: 20px; 
        border-radius: 15px; border-left: 5px solid #bb86fc;
        margin-bottom: 30px; line-height: 1.6;
    }
    .pergunta {
        text-align: center; font-size: 26px !important; 
        margin: 60px 0 30px; color: #ffffff; font-weight: 700;
    }
    div.row-widget.stRadio > div { flex-direction: row !important; justify-content: center !important; gap: 40px !important; }
    div.row-widget.stRadio div[data-testid="stMarkdownContainer"] { display: none !important; }
    div.row-widget.stRadio label div[dir="ltr"] {
        background-color: #b784f7 !important; color: #000 !important;
        width: 85px !important; height: 85px !important; border-radius: 50% !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        font-size: 28px !important; font-weight: 900 !important;
        box-shadow: 0 0 25px rgba(183, 132, 247, 0.8) !important; margin-bottom: 15px !important;
    }
    div.row-widget.stRadio label p { font-size: 18px !important; color: #ffffff !important; font-weight: 500 !important; }
    div.row-widget.stRadio label[data-checked="true"] div[dir="ltr"] {
        background-color: #ffffff !important; box-shadow: 0 0 45px #b784f7 !important; transform: scale(1.15);
    }
    .resultado-box {
        background: linear-gradient(135deg, #1a0033, #2d0055);
        padding: 40px; border-radius: 25px; border: 3px solid #bb86fc; text-align: center; margin-top: 60px;
    }
    .pontuacao-num { font-size: 5rem; font-weight: 900; color: #bb86fc; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Análise de Risco Comportamental</h1>", unsafe_allow_html=True)

st.markdown("""
<div class="intro-text">
    <b>Por que estas perguntas são vitais?</b><br>
    Este protocolo foi estruturado com base em estudos de <b>Psicologia Forense</b>. As perguntas focam em comportamentos preditores de alta letalidade, permitindo a identificação do risco em estágios precoces.
</div>
""", unsafe_allow_html=True)

with st.expander("🔬 Ver Embasamento Científico e Referências"):
    st.markdown("""
    <div style="font-size:16px; color:#bbb;">
    • <b>Modelo de Duluth:</b> Poder e controle.<br>
    • <b>Escala de Charlot (2025):</b> Sinais preditivos precoces.<br>
    • <b>Danger Assessment (Campbell):</b> Avaliação de risco grave.
    </div>
    """, unsafe_allow_html=True)

opcoes = {1: "Nunca", 2: "Raro", 3: "Às vezes", 4: "Sempre"}
perguntas = [
    "Ele demonstra um senso de 'posse' ou autoridade superior sobre suas decisões?",
    "Ele tenta controlar o que você veste, com quem fala ou para onde vai?",
    "Ele desqualifica sua percepção da realidade (faz você duvidar da sua memória)?",
    "Ele demonstra ciúme excessivo e justifica isso como 'excesso de amor'?",
    "Ele monitora suas redes sociais, mensagens ou exige saber suas senhas?",
    "Ele isola você de sua rede de apoio (família/amigos)?",
    "Há um ciclo de 'explosão de raiva' seguido por 'pedidos de desculpas'?",
    "Ele pressiona ou obriga você a ter relações sexuais quando você não quer?",
    "Ele sabota seus métodos contraceptivos ou pressiona por uma gravidez?",
    "Ele costuma culpar você pelas reações agressivas dele?"
]

respostas = []
for i, p in enumerate(perguntas, 1):
    st.markdown(f'<div class="pergunta">{i}. {p}</div>', unsafe_allow_html=True)
    escolha = st.radio(label=f"q{i}", options=[1, 2, 3, 4], index=None, horizontal=True, key=f"q{i}", format_func=lambda x: opcoes[x], label_visibility="collapsed")
    if escolha: respostas.append(escolha)

if len(respostas) == len(perguntas):
    pontuacao_total = sum(respostas)
    registrar_dados(pontos=pontuacao_total, respostas=respostas, tipo="Teste Finalizado")
    
    st.markdown("<div class='resultado-box'>", unsafe_allow_html=True)
    cor = "#f44336" if pontuacao_total > 28 else ("#ffeb3b" if pontuacao_total > 18 else "#4caf50")
    nivel = "ALTO RISCO" if pontuacao_total > 28 else ("RISCO MODERADO" if pontuacao_total > 18 else "BAIXO RISCO")
    st.markdown(f"<h2 style='color:{cor}'>{nivel}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='pontuacao-num'>{pontuacao_total}/40</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><br><div style='text-align:center; color:#888; font-size:16px;'>📞 Ajuda Imediata? <b>Disque 180</b></div>", unsafe_allow_html=True)
