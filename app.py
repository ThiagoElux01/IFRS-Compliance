import streamlit as st
from supabase import create_client, Client
from datetime import datetime
import pytz

st.set_page_config(layout="wide")

# Conexão Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("📘 IFRS - Cadastro de Normas")

# -----------------------------
# INSERIR NOVA NORMA
# -----------------------------
st.subheader("Adicionar Nova Norma")

norma = st.text_input("Norma:")
descricao = st.text_input("Descrição:")

if st.button("Salvar"):
    if norma.strip() and descricao.strip():
        brasil_tz = pytz.timezone("America/Sao_Paulo")
        now = datetime.now(brasil_tz)

        supabase.table("messages").insert({
            "Norma": norma,
            "Descrição": descricao,
            "created_at": now.isoformat()
        }).execute()

        st.success("Norma cadastrada com sucesso!")
        st.rerun()

st.markdown("---")

# -----------------------------
# LISTAR E EXCLUIR
# -----------------------------
st.subheader("Normas Registradas")

data = supabase.table("messages") \
    .select("*") \
    .order("created_at", desc=True) \
    .execute()

if data.data:

    for row in data.data:
        colA, colB = st.columns([4, 1])

        with colA:
            st.markdown(
                f"""
                <div style="padding:10px; border:1px solid #ccc; border-radius:6px; margin-bottom:10px;">
                    <strong>ID:</strong> {row['id']}<br>
                    <strong>Norma:</strong> {row['Norma']}<br>
                    <strong>Descrição:</strong> {row['Descrição']}<br>
                </div>
                """,
                unsafe_allow_html=True
            )

        with colB:
            if st.button("🗑️ Excluir", key=f"del_{row['id']}"):
                supabase.table("messages").delete().eq("id", row["id"]).execute()
                st.rerun()

else:
    st.info("Nenhuma norma cadastrada ainda.")
