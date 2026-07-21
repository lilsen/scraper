import os
import requests
from bs4 import BeautifulSoup
import time

def descargar_imagenes(url_pagina, base_path, nombre_producto):
    #carpeta nombre del producto
    carpeta_destino = os.path.join(base_path, nombre_producto)
    
    #Creacion la carpeta automáticamente si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
        print(f"📁 Carpeta creada: {carpeta_destino}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": url_pagina
    }

    print(f"🌐 Conectando al álbum...")
    respuesta = requests.get(url_pagina, headers=headers)
    soup = BeautifulSoup(respuesta.text, 'html.parser')
    
    # Buscador de imagenes en alta resolucion (las que necesito)
    imagenes = soup.find_all('img', {'data-origin-src': True})
    
    print(f"🔍 Se encontraron {len(imagenes)} imágenes posibles.")

    urls_unicas = set()
    contador = 1
    
    for img in imagenes:
        url = img['data-origin-src']
        if url.startswith('//'):
            url = 'https:' + url

        if 'photo.yupoo.com' in url and url not in urls_unicas:
            urls_unicas.add(url)
            
            try:
                print(f"⬇️ Descargando imagen {contador}...")
                response = requests.get(url, headers=headers)
                
                # Nombre del archivo dinámico
                nombre_archivo = f"{nombre_producto} {contador}.jpg"
                ruta = os.path.join(carpeta_destino, nombre_archivo)
                
                with open(ruta, 'wb') as f:
                    f.write(response.content)
                
                contador += 1
                time.sleep(0.5) 
            except Exception as e:
                print(f"❌ Error al bajar imagen: {e}")

    print(f"🎉 ¡Listo! Se guardaron {contador - 1} imágenes en '{carpeta_destino}'")

if __name__ == "__main__":
    # --- CONFIGURACIÓN  ---
    NOMBRE = ""  # Nombre de la carpeta y del archivo a guardar
    
    URL_ALBUM = "" # Url del producto a scrapear 
    RUTA_BASE = r""  # Ruta en la que se guardan las imagenes
    
    descargar_imagenes(URL_ALBUM, RUTA_BASE, NOMBRE)
