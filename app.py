import streamlit as st
from supabase import create_client, Client
from datetime import datetime
import pytz

st.set_page_config(layout="wide")

# Conexão Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("Tabela IFRS")

# Buscar dados
data = supabase.table("messages").select("*").order("created_at", desc=True).execute()

# Se houver dados, formata a tabela
if data.data:
    df = []
    br_tz = pytz.timezone("America/Sao_Paulo")

    for row in data.data:
        # converter data para formato BR
        dt = datetime.fromisoformat(row["created_at"].replace("Z", "+00:00"))
        dt_br = dt.astimezone(br_tz).strftime("%d/%m/%Y %H:%M")

        df.append({
            "ID": row["id"],
            "Norma": row.get("Norma", ""),
            "Descrição": row.get("Descrição", row.get("texto2", "")),  # usa Descrição se existir
            "Data Registro": dt_br
        })

    st.table(df)

else:
    st.info("Nenhum registro encontrado.")
