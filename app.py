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
    from datetime import datetime
    import pytz
    
    # timezone Brasil
    br_tz = pytz.timezone("America/Sao_Paulo")
    
    for row in data.data:
        # Converter string ISO para datetime
        dt = datetime.fromisoformat(row["created_at"].replace("Z", "+00:00"))
    
        # Converter para Brasil
        dt_br = dt.astimezone(br_tz)
    
        # Formatar dd/mm/yyyy HH:MM
        dt_formatado = dt_br.strftime("%d/%m/%Y %H:%M")
    
        # Exibir
        st.markdown(f"**{dt_formatado}** — {row['text']}")
