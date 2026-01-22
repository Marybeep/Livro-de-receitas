import streamlit as st
import json
import base64
from io import BytesIO
from PIL import Image
import os

# ================= CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(
    page_title="Livro de Receitas",
    page_icon="🍰",
    layout="centered"
)

# ================= ESTILO (CORES + FONTES + ANIMAÇÃO) =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.fade {
    animation: fadeIn 1.2s ease-in-out;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

.card {
    background-color: #fff3f7;
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
}

h1, h2, h3 {
    color: #b76e79;
}

</style>
""", unsafe_allow_html=True)

# ================= IMAGEM EMBUTIDA =================
img_base64 = """
iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAM1BMVEX///
8AAAD5+fn09PTn5+fV1dXZ2dnCwsLa2trf39+qqqqOjo7Pz8+vr6+ysrJr7sEAAAB+UlEQVR4nO3bS27DMAxFUZP//6fd2a4YlJZx8MIkYc6y+4YdAAQAAAAAAAAAA8N8zYF5bq3S2X0m4l7bJZKp3J8xF3n9o+5X8zM2b9bZ2y8s5n8u5Yy+uV9nWZ1n1M8m7uYp2Z6Z2m9y0V7e2p3xw5Zr8vZtZ5sX7k6n7vWZ5f7r3n5m3m9Zz4ZP9k5xk9n9z8v6m9z0v7m9n9Y7u4AAAAAAAAAAADwL8wF3Q8lZzv7XwAAAABJRU5ErkJggg==
"""

image = Image.open(BytesIO(base64.b64decode(img_base64)))

# ================= BANCO DE DADOS =================
DB_FILE = "receitas.json"

def carregar_receitas():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_receitas(receitas):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(receitas, f, indent=4, ensure_ascii=False)

receitas = carregar_receitas()

# ================= MENU =================
menu = st.sidebar.radio(
    "📚 Menu",
    ["🏠 Home", "📖 Ver Receitas", "➕ Adicionar Receita", "✏️ Editar Receitas"]
)

# ================= HOME =================
if menu == "🏠 Home":
    st.markdown("<div class='fade'>", unsafe_allow_html=True)
    st.title("🍰 Livro de Receitas")
    st.image(image, use_container_width=True)
    st.write("Um site lindo para guardar, criar e editar suas receitas favoritas 💗")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= VER RECEITAS =================
elif menu == "📖 Ver Receitas":
    st.title("📖 Receitas")

    if not receitas:
        st.info("Nenhuma receita cadastrada ainda.")
    else:
        for r in receitas:
            st.markdown(f"""
            <div class='card fade'>
                <h3>{r['nome']}</h3>
                <b>Ingredientes:</b><br>{r['ingredientes']}<br><br>
                <b>Modo de preparo:</b><br>{r['modo']}
            </div>
            """, unsafe_allow_html=True)

# ================= ADICIONAR =================
elif menu == "➕ Adicionar Receita":
    st.title("➕ Nova Receita")

    nome = st.text_input("Nome da receita")
    ingredientes = st.text_area("Ingredientes")
    modo = st.text_area("Modo de preparo")

    if st.button("Salvar Receita"):
        if nome and ingredientes and modo:
            receitas.append({
                "nome": nome,
                "ingredientes": ingredientes,
                "modo": modo
            })
            salvar_receitas(receitas)
            st.success("Receita salva com sucesso 💖")
        else:
            st.warning("Preencha todos os campos.")

# ================= EDITAR =================
elif menu == "✏️ Editar Receitas":
    st.title("✏️ Editar / Apagar")

    if not receitas:
        st.info("Nenhuma receita para editar.")
    else:
        nomes = [r["nome"] for r in receitas]
        escolha = st.selectbox("Escolha uma receita", nomes)
        receita = next(r for r in receitas if r["nome"] == escolha)

        novo_nome = st.text_input("Nome", receita["nome"])
        novos_ing = st.text_area("Ingredientes", receita["ingredientes"])
        novo_modo = st.text_area("Modo de preparo", receita["modo"])

        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 Atualizar"):
                receita["nome"] = novo_nome
                receita["ingredientes"] = novos_ing
                receita["modo"] = novo_modo
                salvar_receitas(receitas)
                st.success("Receita atualizada 💗")

        with col2:
            if st.button("🗑️ Apagar"):
                receitas.remove(receita)
                salvar_receitas(receitas)
                st.warning("Receita apagada.")
