import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# Configuração da Página
st.set_page_config(page_title="Detector de Riscos", page_icon="⚠️", layout="centered")

# --- CONEXÃO COM GOOGLE SHEETS ---
def salvar_na_planilha(linha):
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        
        # Carrega credenciais formatadas do Streamlit Secrets
        creds_dict = {
            "type": st.secrets["gcp_service_account"]["type"],
            "project_id": st.secrets["gcp_service_account"]["project_id"],
            "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
            "private_key": st.secrets["gcp_service_account"]["private_key"],
            "client_email": st.secrets["gcp_service_account"]["client_email"],
            "client_id": st.secrets["gcp_service_account"]["client_id"],
            "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
            "token_uri": st.secrets["gcp_service_account"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"],
            "universe_domain": st.secrets["gcp_service_account"]["universe_domain"],
        }
        
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        
        # Acesso à planilha [cite: 2026-02-13]
        url = "https://docs.google.com/spreadsheets/d/1HOrUNzIMDhsGVIlFjfowEEsNS2UrkS57oIlYLVRZ03M/edit#gid=0"
        sheet = client.open_by_url(url).sheet1
        
        # Salva mantendo dados anteriores [cite: 2026-01-18]
        sheet.append_row(linha)
    except Exception as e:
        # Registro local caso a nuvem falhe
        with open("dados_analise.txt", "a", encoding="utf-8") as f:
            f.write(f"{';'.join(map(str, linha))}\n")

# --- DESIGN NEON E FONTES 26px ---
st.markdown("""
<style>
    .main {background-color: #0e001a; color: white;}
    .stApp {background-color: #0e001a;}
    .pergunta {text-align: center; font-size: 26px !important; margin: 50px 0 30px; color: #ffffff; font-weight: 700;}
    
    /* BOTÕES CIRCULARES NEON */
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

# Lista de Perguntas
opcoes = {1: "Nunca", 2: "Raro", 3: "Às vezes", 4: "Sempre"}
perguntas = [
    "Ele demonstra um senso de 'posse' ou autoridade superior sobre suas decisões?",
    "Ele tenta controlar o que você veste, com quem fala ou para onde vai?",
    "Ele desqualifica sua percepção da realidade (faz você duvidar da sua memória)?",
    "Ele demonstra ciúme excessivo e justifica isso como 'excesso de amor'?",
    "Ele monitora suas redes sociais, mensagens ou exige saber suas senhas?"
]

respostas = []
for i, p in enumerate(perguntas, 1):
    st.markdown(f'<div class="pergunta">{i}. {p}</div>', unsafe_allow_html=True)
    escolha = st.radio(label=f"q{i}", options=[1, 2, 3, 4], index=None, horizontal=True, key=f"q{i}", format_func=lambda x: opcoes[x], label_visibility="collapsed")
    if escolha: respostas.append(escolha)

if len(respostas) == len(perguntas):
    pontos = sum(respostas)
    nivel = "ALTO" if pontos > 14 else ("MODERADO" if pontos > 9 else "BAIXO")
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Linha para a planilha: data_hora;perguntas;resposta;resultado
    linha = [data_hora, "; ".join(perguntas), ", ".join(map(str, respostas)), nivel]
    salvar_na_planilha(linha)
    
    st.markdown(f"<div style='text-align:center; background:#1a0033; padding:20px; border-radius:20px; border:2px solid #bb86fc;'><h2>{nivel} RISCO ({pontos}/20)</h2></div>", unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#888;'>📞 Ajuda? Disque 180</p>", unsafe_allow_html=True)
