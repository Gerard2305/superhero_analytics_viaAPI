import streamlit as st
from src.filters import top_10_highest, top_10_lowest, top_10_balanced
from src.plots import plot_top_heroes, plot_hero_radar

# --- CONFIGURACIÓN VISUAL ---
TRADUCCIONES = {
    "intelligence": "Inteligencia", "strength": "Fuerza",
    "speed": "Velocidad", "durability": "Durabilidad",
    "power": "Poder", "combat": "Combate"
}

def init_state():
    if "selected_hero" not in st.session_state:
        st.session_state.selected_hero = None
    if "view" not in st.session_state:
        st.session_state.view = "menu"

def change_view(view_name, hero=None):
    st.session_state.view = view_name
    if hero:
        st.session_state.selected_hero = hero

def render_header():
    st.markdown("""
        <style>
        .main-title { font-family: 'Arial'; font-weight: 800; font-size: 4rem; color: #FFFFFF; }
        .subtitle { font-family: 'Arial'; font-size: 1.2rem; color: #CCCCCC; margin-bottom: 30px; }
        .stButton button { border-radius: 8px; }
        </style>
        <div class="main-title">Marvel on Your Desk</div>
        <div class="subtitle">Exploración interactiva de héroes</div>
        """, unsafe_allow_html=True)

# --- VISTA 1: MENÚ PRINCIPAL ---
def render_menu(heroes):
    st.markdown("### 🔍 Buscar héroe")
    hero_names = sorted([h.name for h in heroes])
    
    selected = st.selectbox("Escribe un nombre:", [""] + hero_names, label_visibility="collapsed")
    if selected:
        hero = next(h for h in heroes if h.name == selected)
        change_view("hero", hero)
        st.rerun()

    st.divider()
    
    # Rankings
    c1, c2 = st.columns(2)
    with c1:
        stat_key = st.selectbox("Estadística:", list(TRADUCCIONES.keys()), format_func=lambda x: TRADUCCIONES[x])
    with c2:
        rtype = st.radio("Criterio:", ["Más fuertes", "Más débiles", "Balanceados"], horizontal=True)

    if rtype == "Más fuertes":
        ranking = top_10_highest(heroes, stat_key)
        prefix = "Top 10 Superior"
    elif rtype == "Más débiles":
        ranking = top_10_lowest(heroes, stat_key)
        prefix = "Top 10 Inferior"
    else:
        ranking = top_10_balanced(heroes, stat_key)
        prefix = "Top 10 Balanceado"

    stat_label = TRADUCCIONES[stat_key]
    st.subheader(f"🏆 {prefix} - {stat_label}")
    
    fig = plot_top_heroes(ranking, stat_key, prefix, stat_label)
    if fig: st.pyplot(fig, use_container_width=True)

    st.write("#### Detalle")
    for i, h in enumerate(ranking, 1):
        val = getattr(h.powerstats, stat_key, 0)
        st.button(f"#{i} {h.name} ({val})", key=f"b_{h.id}", on_click=change_view, args=("hero", h), use_container_width=True)

# --- VISTA 2: DETALLE DEL HÉROE ---
def render_hero_detail():
    h = st.session_state.selected_hero
    st.button("⬅ Volver", on_click=change_view, args=("menu",))
    
    if not h: return
    
    st.title(h.name.upper())
    c1, c2 = st.columns([1.2, 1])
    
    with c1:
        img_url = h.images.get('lg') or h.images.get('sm') or ""
        
        # Corrección de atributos (Evita el AttributeError)
        full_name = h.biography.fullName if h.biography.fullName else "Desconocido"
        place = h.biography.placeOfBirth if h.biography.placeOfBirth != "-" else "Desconocido"
        race = h.appearance.race if h.appearance.race else "Desconocida"

        st.markdown(f"""
        - **Nombre Real:** {full_name}
        - **Lugar de Nacimiento:** {place}
        - **Raza:** {race}
        - [Ver Imagen Original]({img_url})
        """)
        
        # Stats métricas
        s_cols = st.columns(3)
        stats_map = [("intelligence", "Int"), ("strength", "Fza"), ("speed", "Vel"), 
                     ("durability", "Res"), ("power", "Pod"), ("combat", "Com")]
        
        for i, (k, l) in enumerate(stats_map):
            with s_cols[i%3]: st.metric(l, getattr(h.powerstats, k, 0))

        st.divider()
        
        # --- SECCIÓN IA RESTAURADA ---
        st.markdown("""
        <div style="background-color: #262730; padding: 15px; border-radius: 10px; border-left: 5px solid #FF4B4B;">
            <p style="margin:0; font-style: italic;">
            "¿Esa foto oficial te parece aburrida? A mí también. 😏<br>
            Vamos a darle un giro creativo con IA. Pulsa el botón de abajo y prepárate para ver a tu héroe favorito como nunca antes lo habías imaginado."
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("") 
        
        st.button(
            "✨ ¡Reimaginar con IA!", 
            on_click=change_view, 
            args=("ai_image",),
            type="primary",
            use_container_width=True
        )

    with c2:
        fig = plot_hero_radar(h)
        if fig: st.pyplot(fig, use_container_width=True)

# --- VISTA 3: LABORATORIO IA ---
def render_ai_view():
    h = st.session_state.selected_hero
    st.button("⬅ Volver a ficha del héroe", on_click=change_view, args=("hero",))
    
    st.header(f"🎨 Laboratorio Creativo: {h.name}")
    
    st.info("🚧 Módulo de DALL·E en construcción...")
    st.markdown(f"""
        Estás a un paso de generar una variante única de **{h.name}**.
        
        En la versión final, aquí verás:
        1. El prompt de generación optimizado.
        2. La imagen generada en estilo Cómic/Dark.
    """)