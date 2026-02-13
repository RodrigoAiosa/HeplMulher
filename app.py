import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# Configuração da Página
st.set_page_config(
    page_title="Detector de Riscos",
    page_icon="⚠️",
    layout="centered"
)

# --- CONEXÃO COM GOOGLE SHEETS ---
def salvar_na_planilha(dados_finais):
    try:
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        creds_info = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_info, scopes=scope)
        client = gspread.authorize(creds)

        url = "https://docs.google.com/spreadsheets/d/1HOrUNzIMDhsGVIlFjfowEEsNS2UrkS57oIlYLVRZ03M/edit#gid=0"
        sheet = client.open_by_url(url).sheet1

        ultima_linha = len(sheet.get_all_values()) + 1

        sheet.update(
            f"A{ultima_linha}:E{ultima_linha + len(dados_finais) - 1}",
            dados_finais
        )

        return True

    except Exception as e:
        st.error(f"Erro técnico: {e}")
        return False


# --- CSS ---
st.markdown("""
<style>
    .main {background-color: #0e001a; color: white;}
    .stApp {background-color: #0e001a;}

    .pergunta {
        text-align: left;
        font-size: 26px !important;
        margin: 50px 0 30px;
        color: #ffffff;
        font-weight: 700;
    }

    .resultado {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        margin-top: 30px;
        padding: 15px;
        border-radius: 10px;
    }

    .baixo {
        background-color: #1b5e20;
        color: #00ff88;
    }

    .moderado {
        background-color: #665c00;
        color: #ffd600;
    }

    .alto {
        background-color: #5e0000;
        color: #ff4d4d;
    }

</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center; color:#bb86fc;'>Análise de Risco Comportamental</h1>",
    unsafe_allow_html=True
)

# --- BLOCO DE REFERÊNCIAS ---
st.info("""
Este questionário foi inspirado em estudos da OMS, CDC, UN Women,
Instituto Maria da Penha e na obra "Why Does He Do That?" de Lundy Bancroft.
""")

# ID único
if 'id_acesso' not in st.session_state:
    st.session_state['id_acesso'] = datetime.now().strftime("%Y%m%d%H%M%S")

# Perguntas
opcoes = {1: "Nunca", 2: "Raro", 3: "Às vezes", 4: "Sempre"}

perguntas = [
    "Ele demonstra um senso de posse sobre suas decisões?",
    "Ele tenta controlar o que você veste ou para onde vai?",
    "Ele faz você duvidar da sua memória ou percepção?",
    "Ele demonstra ciúme excessivo?",
    "Ele monitora suas redes sociais ou mensagens?",
    "Ele tenta isolar você de amigos ou família?",
    "Há explosões de raiva seguidas de desculpas?",
    "Ele pressiona você a fazer algo que não quer?",
    "Ele pressiona por gravidez contra sua vontade?",
    "Ele culpa você pelas reações agressivas dele?"
]

respostas_coletadas = []

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
        respostas_coletadas.append({
            "pergunta": p,
            "resposta": opcoes[escolha],
            "valor": escolha
        })

# Finalização
if len(respostas_coletadas) == len(perguntas):
    if st.button("FINALIZAR E SALVAR"):
        total = sum([r['valor'] for r in respostas_coletadas])

        if total > 28:
            nivel = "ALTO"
            classe_css = "alto"
        elif total > 18:
            nivel = "MODERADO"
            classe_css = "moderado"
        else:
            nivel = "BAIXO"
            classe_css = "baixo"

        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        id_ac = st.session_state['id_acesso']

        linhas_para_planilha = []
        for r in respostas_coletadas:
            linhas_para_planilha.append([
                agora,
                id_ac,
                r['pergunta'],
                r['resposta'],
                nivel
            ])

        if salvar_na_planilha(linhas_para_planilha):
            st.success("Análise salva com sucesso!")

            st.markdown(
                f'<div class="resultado {classe_css}">Resultado: {nivel}</div>',
                unsafe_allow_html=True
            )

st.markdown(
    "<br><p style='text-align:center; color:#888;'>📞 Disque 180</p>",
    unsafe_allow_html=True
)
