import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

if 'historial' not in st.session_state:
    st.session_state['historial'] = []


def analizar_codigo(entrada_usuario):

    promp_sistema= """
        Eres un experto en revisión de código.
        Analiza el siguiente código y proporciona feedback detallado.

        Devuelve ÚNICAMENTE un JSON válido con exactamente estas claves:
        - "calidad"
        - "legibilidad"
        - "mejoras"
        - "codigo_refactorizado"
        - "explicacion_refactorizado"
        - "complejidad_escalado_mantenible"ademas esta llave de complejidad_escalado_mantenible debes explciar si el cdoigo efactorizado es escalable manteilbe y que psoibl fallos peude tener a futuro con el escalado y mantenibilidad del codigo refactorizado
        """


    respuesta = client.chat.completions.create(
        model= "deepseek-chat",
        messages=[
            #estas son las instrcuccion que se le dan ala ia que es el system con si contexto
            {"role":"system", "content": promp_sistema},
            #aquí es donde le doy el código a analizar que es el user
            {"role":"user", "content": entrada_usuario}
        ],
        response_format={"type": "json_object"},#obligar qeu sea formato json
        temperature=0.2
    )
    # Extraemos el contenido de la respuesta y lo convertimos a un diccionario de Python
    return json.loads(respuesta.choices[0].message.content)
# --- INTERFAZ WEB ---
st.title("🐍 The Clean Coder: AI Analyzer")
st.subheader("Mejora tu lógica para la universidad con IA")

col1, col2 = st.columns(2)

with col1:
    st.header("📋 Instrucciones")
    codigo= st.text_area("Pega tu código aquí para recibir feedback de la IA", height=300,key="codigo_usuario",placeholder="Ejemplo:\n\n```python\ndef sumar(a, b):\n    return a + b\n```")
    boton = st.button("Analizar código")
with col2:
    st.header("diagnosico ")


    if boton and codigo:
        if codigo:
            with st.spinner("Analizando tu código..."):
                data = analizar_codigo(codigo)
                st.success("Análisis completado:")
                 # Mostramos la info organizada
                st.info(f"**calidad:** {data.get('calidad', 'No disponible')}")
                st.error(f"**legibilidad:** {data.get('legibilidad', 'No disponible')}")
                st.success("**Sugerencia de Refactorización:**")
                st.code(data.get('codigo_refactorizado', 'No disponible'), language='python')
                st.write(f"**explicacion refactorizado:** {data.get('explicacion_refactorizado', 'No disponible')}")
                st.info(f"**complejidad de escalado y mantenibilidad:** {data.get('complejidad_escalado_mantenible', 'No disponible')}")
                st.session_state['historial'].append(data)

                if len(st.session_state['historial'])>3:
                    st.session_state['historial'].pop(0)  # Elimina el análisis más antiguo para mantener solo los últimos 3
                
        else:
            st.warning("Por favor, pega tu código en el área de texto antes de analizar.")

for resultado in st.session_state['historial']:
    with st.expander(f"**Análisis Anterior** {len(st.session_state['historial']) - st.session_state['historial'].index(resultado)}", expanded=False):
        st.markdown("---")
        st.info(f"**calidad:** {resultado.get('calidad', 'No disponible')}")
        st.error(f"**legibilidad:** {resultado.get('legibilidad', 'No disponible')}")
        st.success("**Sugerencia de Refactorización:**")
        st.code(resultado.get('codigo_refactorizado', 'No disponible'), language='python')
        st.write(f"**explicacion refactorizado:** {resultado.get('explicacion_refactorizado', 'No disponible')}")
        st.info(f"**complejidad de escalado y mantenibilidad:** {resultado.get('complejidad_escalado_mantenible', 'No disponible')}")
        