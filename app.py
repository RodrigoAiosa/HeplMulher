import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="Análise de Risco Comportamental",
    layout="wide"
)

# ---------------- GOOGLE SHEETS ----------------
def salvar_no_google_sheets(respostas):
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(creds)
    planilha = client.open("AnaliseComportamental")
    aba = planilha.sheet1

    linha = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]

    for i in range(1, 11):
        linha.append(respostas.get(i, ""))

    aba.append_row(linha)

# ---------------- CSS GLOBAL ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #0b0014 0%, #140028 100%);
}

.section {
    max-width: 900px;
    margin: auto;
}

.flip-card {
    background: #140028;
    padding: 28px;
    border-radius: 20px;
    margin-bottom: 25px;
    border: 1px solid #7c3aed;
    box-shadow: 0 0 25px rgba(124,58,237,0.35);
}

.titulo {
    font-size: 42px;
    font-weight: 700;
    color: #c084fc;
    text-align: center;
    margin-bottom: 30px;
}

.divisor {
    height: 2px;
    background: linear-gradient(90deg, transparent, #7c3aed, transparent);
    margin: 40px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown('<div class="titulo">Análise de Risco Comportamental</div>', unsafe_allow_html=True)

st.markdown("""
<div class="section">
<p style="text-align:center; color:#ddd;">
Responda às perguntas abaixo para avaliar padrões de comportamento.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divisor"></div>', unsafe_allow_html=True)

# ---------------- PERGUNTAS ----------------
perguntas = [
    "Ele demonstra um senso de 'posse' ou autoridade superior sobre suas decisões?",
    "Ele tenta controlar o que você veste, com quem fala ou para onde vai?",
    "Ele desqualifica sua percepção da realidade?",
    "Ele demonstra ciúme excessivo?",
    "Ele monitora suas redes sociais?",
    "Ele isola você de amigos ou família?",
    "Há explosões de raiva seguidas de desculpas?",
    "Ele pressiona você a ter relações?",
    "Ele pressiona por gravidez?",
    "Ele culpa você pelas reações dele?"
]

respostas = {}

for i, pergunta in enumerate(perguntas, start=1):
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="flip-card">', unsafe_allow_html=True)

    st.markdown(f"### {i}. {pergunta}")
    respostas[i] = st.radio(
        "Escolha uma opção:",
        ["Nunca", "Raro", "Às vezes", "Sempre"],
        key=f"p{i}",
        label_visibility="collapsed"
    )

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- BOTÃO FINAL ----------------
st.markdown("<br>", unsafe_allow_html=True)

if st.button("Finalizar avaliação"):
    salvar_no_google_sheets(respostas)
    st.success("Respostas salvas no Google Sheets.")
