import streamlit as st
from datetime import datetime
from supabase import create_client, Client
import pytz

st.set_page_config(layout="wide")

# ---- SUPABASE CONNECTION ----
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(url, key)

# ---- UI LAYOUT ----
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("## IFRS")
    st.write("Insira uma mensagem abaixo:")

    # CAMPO TEXTO 1
    msg = st.text_input("Mensagem:")

    # BOTÃO PARA INSERIR TEXTO 1
    if st.button("Enviar"):
        if msg.strip():
            brasil_tz = pytz.timezone("America/Sao_Paulo")
            now = datetime.now(brasil_tz)

            supabase.table("messages").insert({
                "text": msg,
                "created_at": now.isoformat()
            }).execute()

            st.success("Mensagem enviada!")

    st.markdown("---")
    st.subheader("Adicionar Texto 2")

    # CARREGAR LISTA DE MENSAGENS PARA O SELECTBOX
    existing = supabase.table("messages").select("id, text").order("created_at", desc=True).execute()

    options = {f"{row['id']} - {row['text']}": row["id"] for row in existing.data}

    selected = st.selectbox("Escolha uma mensagem existente:", list(options.keys()))

    texto2 = st.text_input("Texto 2:")

    if st.button("Salvar Texto 2"):
        if texto2.strip():
            brasil_tz = pytz.timezone("America/Sao_Paulo")
            now = datetime.now(brasil_tz)

            selected_id = options[selected]

            supabase.table("messages").update({
                "texto2": texto2,
                "created_at": now.isoformat()
            }).eq("id", selected_id).execute()

            st.success("Texto 2 salvo e data atualizada!")

with col2:
    st.markdown("## Últimas mensagens")

    data = supabase.table("messages") \
        .select("*") \
        .order("created_at", desc=True) \
        .limit(20) \
        .execute()

    br_tz = pytz.timezone("America/Sao_Paulo")

    if data.data:
        for row in data.data:
            dt = datetime.fromisoformat(row["created_at"].replace("Z", "+00:00"))
            dt_br = dt.astimezone(br_tz)
            dt_formatado = dt_br.strftime("%d/%m/%Y %H:%M")
            st.markdown(f"**{dt_formatado}** — {row['text']}")
    else:
        st.info("Nenhuma mensagem ainda.")
