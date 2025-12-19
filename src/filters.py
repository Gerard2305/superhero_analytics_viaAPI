from typing import List
# Bloque de importación seguro para evitar errores de ruta
try:
    from src.models import Hero
except ImportError:
    from models import Hero

def _get_stat_value(hero: Hero, stat: str) -> int:
    """Función auxiliar para obtener el valor de una estadística de forma segura."""
    # Como powerstats es un Objeto, usamos getattr en lugar de diccionario['clave']
    if not hero.powerstats:
        return 0
    return getattr(hero.powerstats, stat, 0)

def _calculate_average(hero: Hero) -> float:
    """Calcula el promedio de poder del héroe."""
    if not hero.powerstats:
        return 0.0
    
    stats = [
        hero.powerstats.intelligence,
        hero.powerstats.strength,
        hero.powerstats.speed,
        hero.powerstats.durability,
        hero.powerstats.power,
        hero.powerstats.combat
    ]
    return sum(stats) / len(stats)

def top_10_highest(heroes: List[Hero], stat: str) -> List[Hero]:
    """
    Obtiene los 10 héroes con el valor MÁS ALTO en una estadística específica.
    """
    # 1. Filtrado: Validamos que tengan la estadística mayor a 0
    valid_heroes = [
        h for h in heroes
        if _get_stat_value(h, stat) > 0
    ]

    # 2. Ordenamiento Descendente
    return sorted(
        valid_heroes,
        key=lambda h: _get_stat_value(h, stat),
        reverse=True
    )[:10]

def top_10_lowest(heroes: List[Hero], stat: str) -> List[Hero]:
    """
    Obtiene los 10 héroes con el valor MÁS BAJO en una estadística específica.
    """
    valid_heroes = [
        h for h in heroes
        if _get_stat_value(h, stat) > 0
    ]

    # 2. Ordenamiento Ascendente (sin reverse)
    return sorted(
        valid_heroes,
        key=lambda h: _get_stat_value(h, stat)
    )[:10]

def top_10_balanced(heroes: List[Hero], stat: str) -> List[Hero]:
    """
    Encuentra los héroes cuyo valor en 'stat' está más cerca de su propio promedio.
    """
    valid_heroes = [
        h for h in heroes
        if _get_stat_value(h, stat) > 0
    ]

    # 2. Ordenamiento por menor desviación (abs) respecto a su promedio
    return sorted(
        valid_heroes,
        key=lambda h: abs(_get_stat_value(h, stat) - _calculate_average(h))
    )[:10]

# Esta función es necesaria porque app.py la llama genéricamente
def get_top_heroes(heroes: List[Hero], stat: str) -> List[Hero]:
    """Envoltura para mantener compatibilidad con app.py"""
    return top_10_highest(heroes, stat)