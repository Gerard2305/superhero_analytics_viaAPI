from difflib import get_close_matches
from typing import List

# Bloque de importación seguro (para evitar errores de ruta)
try:
    from src.models import Hero
except ImportError:
    from models import Hero

def search_hero(heroes: List[Hero], query: str, limit: int = 5) -> List[Hero]:
    """
    Busca héroes por nombre.
    Prioridad:
    1. Coincidencia exacta.
    2. Coincidencia parcial (substring).
    3. Coincidencia difusa (fuzzy search) para errores tipográficos.
    """
    # Creamos un diccionario para búsqueda rápida: {nombre_minuscula: objeto_heroe}
    names_map = {h.name.lower(): h for h in heroes}
    query = query.lower().strip()

    # 1. Match Exacto (Rápido)
    if query in names_map:
        return [names_map[query]]

    # 2. Match Parcial (Contiene el texto)
    partials = [
        h for h in heroes
        if query in h.name.lower()
    ]
    
    if partials:
        # Devolvemos los parciales, limitando la cantidad
        return partials[:limit]

    # 3. Sugerencias / Fuzzy Match (Si escribió mal el nombre)
    # cutoff=0.6 significa que debe parecerse al menos un 60%
    suggestions = get_close_matches(
        query,
        names_map.keys(),
        n=limit,
        cutoff=0.6
    )

    # Recuperamos los objetos Hero basados en los nombres sugeridos
    return [names_map[name] for name in suggestions]