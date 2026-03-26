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

# =====================================================================
# COLUNA ESQUERDA
# =====================================================================
with col1:
    st.markdown("## IFRS")
    st.write("Insira uma norma abaixo:")

    # CAMPO NORMA
    norma = st.text_input("Norma:")

    # BOTÃO PARA INSERIR TEXTO 1
    if st.button("Enviar Norma"):
        if norma.strip():
            brasil_tz = pytz.timezone("America/Sao_Paulo")
            now = datetime.now(brasil_tz)

            supabase.table("messages").insert({
                "Norma": norma,
                "created_at": now.isoformat()
            }).execute()

            st.success("Norma enviada!")
            st.rerun()

    st.markdown("---")
    st.subheader("Adicionar Texto 2")

    # CARREGAR LISTA DE MENSAGENS PARA O SELECTBOX
    existing = supabase.table("messages").select("id, Norma").order("created_at", desc=True).execute()

    lista_opcoes = [f"{row['id']} - {row['Norma']}" for row in existing.data]
    lista_ids = {f"{row['id']} - {row['Norma']}": row['id'] for row in existing.data}

    # Selectbox COM KEY (evita reset na rerender)
    selected = st.selectbox("Escolha uma Norma existente:", lista_opcoes, key="select_norma")

    # GUARDA O ID NA SESSION_STATE
    st.session_state["selected_id"] = lista_ids[selected]

    texto2 = st.text_input("Texto 2:")

    if st.button("Salvar Texto 2"):
        if texto2.strip():
            selected_id = st.session_state["selected_id"]

            supabase.table("messages").update({
                "texto2": texto2
            }).eq("id", selected_id).execute()

            st.success("Texto 2 salvo com sucesso!")
            st.rerun()


# =====================================================================
# COLUNA DIREITA
# =====================================================================
with col2:
    st.markdown("## Últimas Normas")

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

            norma_valor = row.get("Norma", "")
            texto2_valor = row.get("texto2", "")

            st.markdown(
                f"""
                <div style="padding:10px; border:1px solid #ddd; border-radius:5px; margin-bottom:10px;">
                    <strong>Data:</strong> {dt_formatado}<br>
                    <strong>Norma:</strong> {norma_valor}<br>
                    <strong>Texto 2:</strong> {texto2_valor if texto2_valor else "<em>(vazio)</em>"}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("Nenhuma norma cadastrada.")
