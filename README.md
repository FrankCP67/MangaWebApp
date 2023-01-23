# MangaWebApp
Permite traducir imagenes de mangas japoneses usando la detección de burbujas de texto mediante un modelo Mask R-CNN.

## Librerias usadas
- Python 3.8
- streamlit
- tensorflow 2.5 (importante)
- manga-ocr 0.1.8

## Compilación 

1. Crear un entorno virtual (a fin de evitar conflictos entre versiones).

2. Instalar las librerías y sus dependencias.

3. Colocar los archivos de la aplicación en una carpeta principal.

## Ejecución
Para iniciar la aplicación, ejecute el siguiente comando:

    streamlit run app.py

Abrir el enlace en el navegador web.

## Funcionamiento

1. Subir las imagenes en el panel izquierdo, luego se mostrará las imagenes que se subieron.
<p align="center">
    <img src="https://user-images.githubusercontent.com/87890299/214146266-ce1c4be3-8d27-437c-ac8e-e123e8f9e7ea.png" width="500">
</p>


2. Presionar el boton **Procesar**, esperar unos segundos.

3. El resultado se muestra a continuación:
<p align="center">
    <img src="https://user-images.githubusercontent.com/87890299/214149066-3954078a-70f0-4e2f-9b9f-d23832818766.png" width="800">
</p>


***Disclaimer:** Las imagenes mostradas son usadas con fines educativos y pertenecen a sus respectivos autores.*
