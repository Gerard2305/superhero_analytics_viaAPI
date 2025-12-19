import os
from pathlib import Path
from dotenv import load_dotenv

def diagnostico():
    print("🕵️ INICIANDO DIAGNÓSTICO DE ENTORNO...")
    
    # 1. Calcular la ruta RAÍZ basada en la ubicación de este script
    # Si este script está en /Users/.../marvel/src/script.py
    # La raíz debería ser /Users/.../marvel/
    script_path = Path(__file__).resolve()
    src_dir = script_path.parent
    root_dir = src_dir.parent
    
    expected_env_path = root_dir / '.env'
    
    print(f"📂 Ruta raíz calculada: {root_dir}")
    print(f"🎯 Buscando archivo en: {expected_env_path}")
    
    # 2. Verificar existencia física del archivo
    if expected_env_path.exists():
        print("✅ ¡El archivo .env EXISTE físicamente!")
    else:
        print("❌ EL ARCHIVO NO APARECE EN LA RUTA ESPERADA.")
        print("   Listando archivos en la carpeta raíz para ver qué hay:")
        archivos = os.listdir(root_dir)
        for f in archivos:
            if "env" in f:
                print(f"   👉 ¿Quizás es este?: '{f}'")
            else:
                print(f"   - {f}")
        return # Terminamos si no existe

    # 3. Intentar leer el contenido crudo (sin librerías, a lo bruto)
    try:
        with open(expected_env_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
            if "OPENAI_API_KEY" in contenido:
                print("✅ La variable OPENAI_API_KEY está escrita dentro del archivo.")
            else:
                print("❌ El archivo existe, pero NO contiene el texto 'OPENAI_API_KEY'.")
                print("   Contenido detectado:")
                print(f"   ---\n{contenido}\n   ---")
                return
    except Exception as e:
        print(f"❌ Error leyendo el archivo: {e}")
        return

    # 4. Probar con load_dotenv
    print("🔄 Probando carga con python-dotenv...")
    load_dotenv(dotenv_path=expected_env_path, override=True)
    
    valor = os.getenv("OPENAI_API_KEY")
    if valor:
        print(f"🎉 ¡ÉXITO! Variable cargada. Valor: {valor[:5]}...")
    else:
        print("❌ load_dotenv falló aunque el archivo existe y tiene texto. Esto es muy raro.")

if __name__ == "__main__":
    diagnostico()