import streamlit as st
import sys
import os

# Ajuste de rutas para encontrar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Solo importamos la función remota
from src.loader import load_heroes_remote
import src.ui as ui

@st.cache_data
def get_marvel_data():
    """
    Carga los datos EXCLUSIVAMENTE desde la API.
    El loader.py se encarga de:
    1. Descargar los datos (aleatorios o completos).
    2. Validar reglas de negocio (Marvel, stats <= 15, etc).
    """
    return load_heroes_remote()

def main():
    # 1. Configuración de página
    st.set_page_config(
        page_title="Marvel App", 
        page_icon="🛡️", 
        layout="wide"
    )
    
    # 2. Inicializar estado visual
    ui.init_state()
    ui.render_header()
    
    # 3. Cargar Datos (Solo API)
    with st.spinner("Conectando a la API y descargando Universo Marvel..."):
        heroes = get_marvel_data()
        
    # 4. Validación de Carga
    if not heroes:
        st.error("❌ No se encontraron héroes válidos. Verifica la conexión o que la API esté devolviendo datos correctos.")
        return

    # 5. Control de Navegación (Router)
    if st.session_state.view == "menu":
        ui.render_menu(heroes)
    elif st.session_state.view == "hero":
        ui.render_hero_detail()
    elif st.session_state.view == "ai_image":
        ui.render_ai_view()

if __name__ == "__main__":
    main()