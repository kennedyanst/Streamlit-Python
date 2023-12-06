import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

st.set_page_config(layout="wide")

@st.cache_data
def gerar_df():
    df = pd.read_excel(
        io = "data.xlsx",
        engine = "openpyxl",
        sheet_name= "Sheet1",
        usecols="A:Q",
        nrows= 89106
    )

    return df


df = gerar_df()

colunas = ["DATA FINAL", "PRODUTO", "REGIÃO", "ESTADO", "PREÇO MÉDIO REVENDA"]

df = df[colunas]

with st.sidebar:
    st.subheader("OLÁ, MUNDO!")
    st.subheader("SELEÇÃO DE FILTROS")
    fProduto = st.selectbox("PRODUTO", df["PRODUTO"].unique())
    fRegiao = st.selectbox("REGIÃO", df["REGIÃO"].unique())
    fEstado = st.selectbox("ESTADO", df["ESTADO"].unique())

    dadosUsuario = df.loc[(
        df["PRODUTO"] == fProduto) & (df["REGIÃO"] == fRegiao)]
    
updateDatas = dadosUsuario["DATA FINAL"].dt.strftime('%b/%Y')
dadosUsuario["DATA FINAL"] = updateDatas[0:]

st.header("DADOS DE PREÇOS DE COMBUSTÍVEIS")
st.subheader("FILTROS SELECIONADOS")
st.markdown(f"**PRODUTO:** {fProduto}")
st.markdown(f"**REGIÃO:** {fRegiao}")
st.markdown(f"**ESTADO:** {fEstado}")


grafico = alt.Chart(dadosUsuario).mark_line(
    point=alt.OverlayMarkDef(color="red", size=20)
    ).encode(
        x="DATA FINAL", 
        y="PREÇO MÉDIO REVENDA", 
        strokeWidth=alt.value(2)
).properties(
    width=1080,
    height=700
)

st.altair_chart(grafico)