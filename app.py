import streamlit as st

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="Análise de Risco Comportamental",
    layout="wide"
)

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

.card {
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
    "Ele demonstra um senso de posse sobre suas decisões?",
    "Ele tenta controlar o que você veste ou para onde vai?",
    "Ele verifica seu celular ou redes sociais?",
    "Ele fica irritado quando você sai sem ele?",
    "Ele tenta afastar você de amigos ou família?",
    "Ele faz você se sentir culpado(a) frequentemente?",
    "Ele muda de humor de forma imprevisível?",
    "Ele desvaloriza suas opiniões?",
    "Ele exige saber onde você está o tempo todo?",
    "Ele reage mal quando contrariado?"
]

respostas = {}

for i, pergunta in enumerate(perguntas, start=1):
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

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
    st.success("Respostas registradas.")
    st.write(respostas)
