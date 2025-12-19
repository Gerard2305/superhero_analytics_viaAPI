import os
import requests
import concurrent.futures
import random  # Importamos random para el muestreo
from dotenv import load_dotenv
from typing import List, Dict, Any

# Cargar variables de entorno
load_dotenv()

TOKEN = os.getenv("SUPERHERO_TOKEN")
BASE_URL = f"https://superheroapi.com/api/{TOKEN}"

# Límites de la API (Existen IDs del 1 al 731 aprox)
MIN_ID = 1
MAX_ID = 732
CANTIDAD_A_CARGAR = 400  # Tu petición

def get_hero_by_id(hero_id: int) -> Dict[str, Any]:
    """Descarga un solo héroe por ID."""
    try:
        url = f"{BASE_URL}/{hero_id}"
        # Timeout corto para no bloquear si un ID falla
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get('response') == 'success':
                return data
    except Exception:
        pass
    return None

def get_heroes_from_api() -> List[Dict[str, Any]]:
    """
    Selecciona 400 IDs al azar y los descarga en paralelo.
    """
    if not TOKEN:
        print("❌ Error: Falta SUPERHERO_TOKEN en .env")
        return []

    print(f"🎲 Seleccionando {CANTIDAD_A_CARGAR} IDs al azar entre {MIN_ID} y {MAX_ID}...")
    
    # --- AQUÍ ESTÁ LA MAGIA ---
    # random.sample genera una lista de números únicos, no repetidos.
    ids_de_la_suerte = random.sample(range(MIN_ID, MAX_ID + 1), CANTIDAD_A_CARGAR)
    
    print(f"🌐 Conectando a SuperHero API (Descargando lote aleatorio)...")
    
    heroes_data = []
    
    # Lanzamos 20 hilos simultáneos para procesar los 400 IDs rápidamente
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        # Mapeamos la función de descarga a nuestra lista de IDs aleatorios
        future_to_id = {executor.submit(get_hero_by_id, i): i for i in ids_de_la_suerte}
        
        for future in concurrent.futures.as_completed(future_to_id):
            data = future.result()
            if data:
                heroes_data.append(data)
                # Feedback visual en consola cada 50 héroes
                if len(heroes_data) % 50 == 0:
                    print(f"   ⚡ {len(heroes_data)} héroes procesados...")

    print(f"✅ Carga completa: {len(heroes_data)} héroes obtenidos.")
    return heroes_data