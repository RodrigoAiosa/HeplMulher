import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(
    page_title="Detector de Riscos",
    page_icon="⚠️",
    layout="centered"
)

# GOOGLE SHEETS
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


# CSS QUE ESTILIZA O CONTAINER REAL DO STREAMLIT
st.markdown("""
<style>
.stApp {
    background-color: #0e001a;
}

div[data-testid="stContainer"] {
    background: linear-gradient(145deg, #1a0033, #2a004d);
    padding: 30px;
    border-radius: 25px;
    margin-bottom: 35px;
    border: 2px solid #7b2cff;
    box-shadow:
        0 0 20px rgba(123,44,255,0.7),
        0 0 35px rgba(123,44,255,0.4),
        inset 0 0 12px rgba(123,44,255,0.3);
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center; color:#bb86fc;'>Análise de Risco Comportamental</h1>",
    unsafe_allow_html=True
)

if 'id_acesso' not in st.session_state:
    st.session_state['id_acesso'] = datetime.now().strftime("%Y%m%d%H%M%S")

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
    with st.container():
        st.markdown(f"**{i}. {p}**")

        escolha = st.radio(
            label=f"q{i}",
            options=[1,2,3,4],
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


if len(respostas_coletadas) == len(perguntas):
    if st.button("FINALIZAR E SALVAR"):
        total = sum([r['valor'] for r in respostas_coletadas])
        nivel = "ALTO" if total > 28 else ("MODERADO" if total > 18 else "BAIXO")

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
                f"<h2 style='text-align:center;'>Resultado: {nivel}</h2>",
                unsafe_allow_html=True
            )

st.markdown("<br><p style='text-align:center; color:#888;'>📞 Disque 180</p>", unsafe_allow_html=True)
