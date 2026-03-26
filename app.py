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

    msg = st.text_input("Mensagem:")

    if st.button("Enviar"):
        if msg.strip():
            brasil_tz = pytz.timezone("America/Sao_Paulo")
            now = datetime.now(brasil_tz)

            supabase.table("messages").insert({
                "text": msg,
                "created_at": now.isoformat()
            }).execute()

            st.success("Mensagem enviada!")

with col2:
    st.markdown("## Últimas mensagens")

    data = supabase.table("messages").select("*").order("created_at", desc=True).limit(20).execute()

    if data.data:
        for row in data.data:
            st.markdown(f"**{row['created_at']}** — {row['text']}")
    else:
        st.info("Nenhuma mensagem ainda.")
