import argostranslate.translate
import argostranslate.package
from pathlib import Path
import time
import sys

def cargar_modelo():
    """Carga el modelo manualmente instalado"""
    try:
        # Listar paquetes instalados
        installed_packages = argostranslate.package.get_installed_packages()
        
        # Si no está registrado el modelo, forzar su carga
        if not any(pkg.from_code == 'en' and pkg.to_code == 'es' for pkg in installed_packages):
            print("Registrando modelo manualmente...")
            package_path = "/root/.local/share/argos-translate/packages/translate-en_es-1_0.argosmodel"
            argostranslate.package.install_from_path(package_path)
    except Exception as e:
        print(f"Error cargando modelo: {str(e)}")
        sys.exit(1)

def traducir_archivos():
    entrada_dir = "/mnt/novels-in-english"
    salida_dir = "/mnt/novelas-en-espanol"
    
    cargar_modelo()  # Asegurar que el modelo está cargado
    
    entrada = Path(entrada_dir)
    salida = Path(salida_dir)
    salida.mkdir(parents=True, exist_ok=True)
    
    archivos = list(entrada.glob("*.txt"))
    if not archivos:
        print(f"No se encontraron archivos .txt en {entrada_dir}")
        return
    
    print(f"\nIniciando traducción de {len(archivos)} archivos...")
    
    for archivo in archivos:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                texto = f.read()
            
            texto_traducido = argostranslate.translate.translate(texto, 'en', 'es')
            
            nombre_salida = f"{archivo.stem}-es{archivo.suffix}"
            output_path = salida / nombre_salida
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(texto_traducido)
            
            print(f"✔ Traducido: {archivo.name} → {nombre_salida}")
            
        except Exception as e:
            print(f"✖ Error con {archivo.name}: {str(e)}")

if __name__ == "__main__":
    traducir_archivos()