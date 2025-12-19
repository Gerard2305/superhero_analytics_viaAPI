import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

def _load_comic_font():
    """Carga Comic Sans MS configurada para contraste alto en fondo oscuro."""
    try:
        # Intentamos cargar Comic Sans, si no está, matplotlib usará la default
        return font_manager.FontProperties(family="Comic Sans MS")
    except:
        return None

def setup_comic_style(ax, comic_font):
    """Estética de bordes y textos para modo oscuro."""
    # Ocultamos los bordes del cuadro (spines)
    for spine in ax.spines.values():
        spine.set_visible(False) 
    
    # Solo dejamos visible la línea izquierda como referencia
    ax.spines['left'].set_visible(True)
    ax.spines['left'].set_color('#FFFFFF')
    ax.spines['left'].set_linewidth(1)
    
    # Aplicar fuente y color blanco a los ejes
    if comic_font:
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontproperties(comic_font)
            label.set_color('#FFFFFF')
    
    # Asegurar que los ticks (las rayitas) sean blancos
    ax.tick_params(axis='both', colors='white')

def plot_top_heroes(heroes, stat: str, title_prefix: str = "Top 10", stat_label: str = None):
    """
    Genera gráfico de barras horizontales.
    Adaptado para recibir objetos Hero (no diccionarios).
    """
    if not heroes: 
        return None

    # 1. Extracción de datos (Usando objetos)
    names = [hero.name.upper() for hero in heroes]
    
    # CORRECCIÓN: Usamos getattr porque powerstats es un Objeto, no un dict
    values = [getattr(hero.powerstats, stat, 0) for hero in heroes]
    
    comic_font = _load_comic_font()
    
    # Determinar qué etiqueta usar en el título
    final_stat_name = stat_label if stat_label else stat.upper()

    # --- PALETA ARMÓNICA ---
    colors = ["#FFD54F" if i == 0 else "#FF8A65" if i < 3 else "#90CAF9" for i in range(len(values))]

    fig, ax = plt.subplots(figsize=(10, 5), dpi=100)
    
    # Configuración de fondo oscuro
    fig.patch.set_facecolor('#001435') 
    fig.patch.set_alpha(1.0) # Opacidad al 100 para que se vea bien
    ax.set_facecolor("#001435")

    # Crear barras
    bars = ax.barh(names, values, color=colors, edgecolor=None)
    ax.invert_yaxis() # El mejor arriba

    # TÍTULO
    ax.set_title(f"{title_prefix} {final_stat_name}", fontsize=16, 
                 fontproperties=comic_font, weight='bold', color='#FFFFFF', pad=15)
    
    setup_comic_style(ax, comic_font)

    # Etiquetas de valor en las barras
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2, f'{int(width)}', 
                va='center', fontproperties=comic_font, weight='bold', 
                fontsize=10, color='#FFFFFF')

    plt.tight_layout()
    plt.show() # Importante para que se abra la ventana
    return fig

def plot_hero_radar(hero):
    """
    Genera gráfico de radar para un solo héroe.
    Adaptado para objetos Hero.
    """
    # 1. Definimos las etiquetas fijas para asegurar el orden
    labels = ['INT', 'STR', 'SPD', 'DUR', 'POW', 'COM']
    
    # 2. Extraemos valores del objeto (CORRECCIÓN PRINCIPAL)
    if not hero.powerstats:
        return None
        
    values = [
        hero.powerstats.intelligence,
        hero.powerstats.strength,
        hero.powerstats.speed,
        hero.powerstats.durability,
        hero.powerstats.power,
        hero.powerstats.combat
    ]
    
    # Si todos son 0, no graficamos
    if not any(values): return None

    comic_font = _load_comic_font()
    
    # Cerrar el círculo (repetir el primer valor al final)
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True), dpi=100)

    # Fondo Tarjeta Azul Profundo (#001435)
    fig.patch.set_facecolor("#001435")
    ax.set_facecolor("#001435")

    # --- ESTILO RADAR ---
    ax.plot(angles, values, color="#FFF176", linewidth=2, linestyle='solid')
    ax.fill(angles, values, color="#FFF176", alpha=0.25)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Etiquetas de los ejes (TEXTO BLANCO)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    
    # Aplicar estilo a las etiquetas radiales
    for label in ax.get_xticklabels():
        if comic_font:
            label.set_fontproperties(comic_font)
        label.set_color('#FFFFFF')
        label.set_fontsize(10)

    ax.set_ylim(0, 100)
    ax.set_yticklabels([]) # Ocultar números concéntricos para limpieza visual
    
    # --- GRID (Rejilla) ---
    ax.grid(True, color="#E0E0E0", linestyle='--', alpha=0.3)
    ax.spines['polar'].set_color('#E0E0E0')
    ax.spines['polar'].set_alpha(0.4)

    ax.set_title(hero.name.upper(), size=14, fontproperties=comic_font, 
                 weight='bold', pad=30, color='#FFFFFF')

    plt.tight_layout()
    plt.show()
    return fig