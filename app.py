import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# Configuração da Página
st.set_page_config(
    page_title="Detector de Riscos: Perfil de Agressor",
    page_icon="⚠️",
    layout="centered"
)

# FUNÇÃO PARA CONECTAR E REGISTRAR (Google Sheets)
def registrar_na_planilha(dados):
    try:
        # Tenta conectar usando as secrets do Streamlit
        # Você deve colocar suas credenciais JSON nas Secrets ou usar login por link público se configurado
        # Para fins de simplicidade e evitar o erro de 'Unsupported', usamos gspread
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        
        # Se você tiver o JSON da conta de serviço nas secrets:
        if "gcp_service_account" in st.secrets:
            creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
            client = gspread.authorize(creds)
            # Abre pela URL que você forneceu
            sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1HOrUNzIMDhsGVIlFjfowEEsNS2UrkS57oIlYLVRZ03M/edit#gid=0").sheet1
            sheet.append_row(dados)
    except Exception as e:
        # Se falhar o Google Sheets, salva no TXT local para não perder o dado [cite: 2026-02-13]
        with open("backup_dados.txt", "a", encoding="utf-8") as f:
            f.write(f"{dados}\n")

def registrar_evento(pontos=None, respostas=None, tipo="acesso"):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = [data_hora, tipo, str(pontos), str(respostas)]
    registrar_na_planilha(linha)

# Log de acesso único por sessão
if 'log_feito' not in st.session_state:
    registrar_evento(tipo="Acesso ao App")
    st.session_state['log_feito'] = True

# --- INTERFACE (DESIGN NEON 26px) ---
st.markdown("""
<style>
    .main {background-color: #0e001a; color: white;}
    .stApp {background-color: #0e001a;}
    h1 {color: #bb86fc !important; text-align: center; font-size: 2.8rem !important;}
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
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Análise de Risco Comportamental</h1>", unsafe_allow_html=True)

st.markdown("""
<div class="intro-text">
    <b>Por que estas perguntas são vitais?</b><br>
    Este protocolo foi estruturado com base em estudos de <b>Psicologia Forense</b>. As perguntas identificam "preditores de alta letalidade", permitindo a identificação do risco em estágios precoces.
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
    registrar_evento(pontos=pontuacao_total, respostas=respostas, tipo="Teste Finalizado")
    
    st.markdown("<div class='resultado-box'>", unsafe_allow_html=True)
    cor = "#f44336" if pontuacao_total > 28 else ("#ffeb3b" if pontuacao_total > 18 else "#4caf50")
    nivel = "ALTO RISCO" if pontuacao_total > 28 else ("RISCO MODERADO" if pontuacao_total > 18 else "BAIXO RISCO")
    st.markdown(f"<h2 style='color:{cor}'>{nivel}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:5rem; font-weight:900; color:#bb86fc;'>{pontuacao_total}/40</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><br><div style='text-align:center; color:#888; font-size:16px;'>📞 Ajuda Imediata? <b>Disque 180</b></div>", unsafe_allow_html=True)
