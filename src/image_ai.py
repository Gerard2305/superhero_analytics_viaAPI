import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# --- CONFIGURACIÓN DE RUTA ---
# Aseguramos que encuentre el .env sin importar desde dónde se llame
base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# Configuración Azure
API_KEY = os.getenv("OPENAI_API_KEY")
ENDPOINT_URL = "https://iebs-resource.cognitiveservices.azure.com/openai/deployments/dall-e-3/images/generations?api-version=2024-02-01"

def generate_hero_image(hero_name: str):
    """
    Intenta generar la imagen del héroe. 
    Si Azure la bloquea por Copyright (Error 400), retornará None.
    """
    
    if not API_KEY:
        print("❌ Error: No se encontró la API KEY.")
        return None

    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY 
    }

    # Prompt original solicitado + Inyección del estilo visual
    # Azure requiere que 'style' en el payload sea 'vivid' o 'natural',
    # así que metemos 'comic-noir' dentro del texto del prompt.
    prompt_text = (
        f"Creame un personaje similar en cuanto a aspecto a {hero_name} "
        f"pero que no tenga problemas de filtro de contenidos. "
        f"Estilo visual: comic-noir."
    )

    payload = {
        "model": "dall-e-3",
        "prompt": prompt_text,
        "size": "1024x1024", 
        "quality": "standard",
        "style": "vivid", # Parámetro técnico obligatorio de Azure (vivid/natural)
        "n": 1
    }

    try:
        response = requests.post(ENDPOINT_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return result['data'][0]['url']
        else:
            # Si falla (ej: filtro de contenido), imprimimos el error en consola para ti
            # y retornamos None para que la UI sepa que debe mostrar el mensaje de disculpa.
            print(f"⚠️ API Azure rechazada ({response.status_code}): {response.text}")
            return None

    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None