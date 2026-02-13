import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# Configuração da Página
st.set_page_config(page_title="Detector de Riscos", page_icon="⚠️", layout="centered")

# --- CONEXÃO COM GOOGLE SHEETS ---
def salvar_na_planilha(lista_de_linhas):
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds_info = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_info, scopes=scope)
        client = gspread.authorize(creds)
        
        # Abre a planilha log_acesso [cite: 2026-02-13]
        url = "https://docs.google.com/spreadsheets/d/1HOrUNzIMDhsGVIlFjfowEEsNS2UrkS57oIlYLVRZ03M/edit#gid=0"
        sheet = client.open_by_url(url).sheet1
        
        # O comando append_rows com a lista correta garante gravação na Coluna A [cite: 2026-01-18]
        sheet.append_rows(lista_de_linhas, value_input_option="USER_ENTERED")
        return True
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        return False

# --- CSS: DESIGN NEON E FONTES 26px ---
st.markdown("""
<style>
    .main {background-color: #0e001a; color: white;}
    .stApp {background-color: #0e001a;}
    .pergunta {text-align: center; font-size: 26px !important; margin: 50px 0 30px; color: #ffffff; font-weight: 700;}
    
    div.row-widget.stRadio > div { flex-direction: row !important; justify-content: center !important; gap: 35px !important; }
    div.row-widget.stRadio div[data-testid="stMarkdownContainer"] { display: none !important; }
    div.row-widget.stRadio label div[dir="ltr"] {
        background-color: #b784f7 !important; color: #000 !important;
        width: 80px !important; height: 80px !important; border-radius: 50% !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        font-size: 26px !important; font-weight: 900 !important;
        box-shadow: 0 0 20px rgba(183, 132, 247, 0.8) !important; margin-bottom: 10px !important;
    }
    div.row-widget.stRadio label p { font-size: 18px !important; color: #d1d1d1 !important; text-align: center; }
    div.row-widget.stRadio label[data-checked="true"] div[dir="ltr"] {
        background-color: #ffffff !important; box-shadow: 0 0 35px #b784f7 !important; transform: scale(1.1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#bb86fc;'>Análise de Risco Comportamental</h1>", unsafe_allow_html=True)

# Gera ID único para o acesso
if 'id_acesso' not in st.session_state:
    st.session_state['id_acesso'] = datetime.now().strftime("%Y%m%d%H%M%S")

# Perguntas Completas
opcoes_texto = {1: "Nunca", 2: "Raro", 3: "Às vezes", 4: "Sempre"}
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

respostas_coletadas = []
for i, p in enumerate(perguntas, 1):
    st.markdown(f'<div class="pergunta">{i}. {p}</div>', unsafe_allow_html=True)
    escolha = st.radio(label=f"q{i}", options=[1, 2, 3, 4], index=None, horizontal=True, key=f"q{i}", format_func=lambda x: opcoes_texto[x], label_visibility="collapsed")
    if escolha:
        respostas_coletadas.append({"p": p, "r": opcoes_texto[escolha], "v": escolha})

# Botão Final
if len(respostas_coletadas) == len(perguntas):
    if st.button("Finalizar e Enviar"):
        total = sum([x['v'] for x in respostas_coletadas])
        nivel = "ALTO" if total > 28 else ("MODERADO" if total > 18 else "BAIXO")
        
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        id_ac = st.session_state['id_acesso']
        
        # MONTAGEM DAS LINHAS - GARANTINDO COLUNA A, B, C, D, E
        # data_hora (A); id_acesso (B); perguntas (C); respostas (D); resultado (E)
        dados_finais = []
        for item in respostas_coletadas:
            dados_finais.append([agora, id_ac, item['p'], item['r'], nivel])
        
        if salvar_na_planilha(dados_finais):
            st.success("Dados gravados corretamente na Coluna A!")
            st.markdown(f"<h2 style='text-align:center;'>Risco {nivel}</h2>", unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#888;'>📞 Disque 180</p>", unsafe_allow_html=True)
