import json
from typing import List

# Importación robusta para evitar errores de ruta
try:
    from src.models import Hero, PowerStats, Appearance, Biography
    from src.api_marvel import get_heroes_from_api
except ImportError:
    from models import Hero, PowerStats, Appearance, Biography
    from api_marvel import get_heroes_from_api

def load_heroes_local(path: str) -> List[Hero]:
    """Carga desde archivo local manejando la estructura de diccionario o lista."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Si es un diccionario con "results", extraemos la lista
        if isinstance(data, dict) and "results" in data:
            data = data["results"]
        # Si es un diccionario sin "results", lo convertimos en lista de 1 elemento
        elif isinstance(data, dict):
            data = [data]

        return _parse_and_filter_data(data)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {path}")
        return []

def load_heroes_remote() -> List[Hero]:
    """Carga desde la API manejando la estructura de respuesta."""
    raw_data = get_heroes_from_api()
    
    # Verificación de estructura API (Diccionario vs Lista)
    if isinstance(raw_data, dict) and "results" in raw_data:
        raw_data = raw_data["results"]
    elif isinstance(raw_data, dict):
        # Caso raro: API devuelve un solo objeto
        raw_data = [raw_data]
        
    return _parse_and_filter_data(raw_data)

def _safe_int(value) -> int:
    """Convierte string a int, devolviendo 0 si es 'null' o inválido."""
    try:
        if value == "null" or value is None: 
            return 0
        return int(value)
    except (ValueError, TypeError):
        return 0

def _parse_and_filter_data(data_list: List[dict]) -> List[Hero]:
    """
    Convierte la data cruda en objetos Hero y aplica el filtro estricto.
    """
    heroes_list = []
    
    # Validación de seguridad por si data_list no es una lista
    if not isinstance(data_list, list):
        return []

    for item in data_list:
        try:
            # Si el item no es diccionario, saltar
            if not isinstance(item, dict): continue

            # 1. Parsing de Stats (Conversión segura de texto a número)
            raw_stats = item.get('powerstats', {})
            stats = PowerStats(
                intelligence=_safe_int(raw_stats.get('intelligence')),
                strength=_safe_int(raw_stats.get('strength')),
                speed=_safe_int(raw_stats.get('speed')),
                durability=_safe_int(raw_stats.get('durability')),
                power=_safe_int(raw_stats.get('power')),
                combat=_safe_int(raw_stats.get('combat'))
            )

            # 2. Parsing de Biografía (Mapeo de claves API con guiones)
            raw_bio = item.get('biography', {})
            bio = Biography(
                fullName=raw_bio.get('full-name', raw_bio.get('fullName', '')),
                alterEgos=raw_bio.get('alter-egos', raw_bio.get('alterEgos', '')),
                aliases=raw_bio.get('aliases', []),
                placeOfBirth=raw_bio.get('place-of-birth', raw_bio.get('placeOfBirth', '')),
                firstAppearance=raw_bio.get('first-appearance', raw_bio.get('firstAppearance', '')),
                publisher=raw_bio.get('publisher', 'Unknown'),
                alignment=raw_bio.get('alignment', 'neutral')
            )

            # 3. Parsing de Apariencia
            raw_app = item.get('appearance', {})
            app = Appearance(
                gender=raw_app.get('gender', 'Unknown'),
                race=raw_app.get('race', 'Unknown'),
                height=raw_app.get('height', []),
                weight=raw_app.get('weight', []),
                eyeColor=raw_app.get('eye-color', '-'),
                hairColor=raw_app.get('hair-color', '-')
            )

            # 4. Parsing de Imágenes (Soporte dual: 'image.url' o 'images.lg')
            raw_img = item.get('image', {})
            images = {}
            if 'url' in raw_img:
                images = {'lg': raw_img['url'], 'sm': raw_img['url']}
            else:
                images = item.get('images', {})

            # 5. Creación del Objeto Hero
            hero = Hero(
                id=int(item.get('id', 0)),
                name=item.get('name', 'Unknown'),
                slug=item.get('slug', ''),
                powerstats=stats,
                appearance=app,
                biography=bio,
                images=images
            )

            # 6. VALIDACIÓN ESTRICTA
            # Aquí se aplican las reglas definidas en models.py 
            # (Marvel, <=15, >=3 ceros, etc.)
            if hero.validate_hero():
                heroes_list.append(hero)

        except Exception:
            # Si un registro está muy roto, lo saltamos silenciosamente
            continue
            
    return heroes_list