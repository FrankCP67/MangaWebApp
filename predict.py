import sys
import numpy
import streamlit as st
import textwrap

# Ruta de librerías
RUTA_LIBRERIAS = "./mrcnn_demo"
RUTA_LIBRERIAS2 = "./google_trans_new"

sys.path.append(RUTA_LIBRERIAS)
sys.path.append(RUTA_LIBRERIAS2)

from google_trans_new import google_translator  # traductor
from manga_ocr import MangaOcr  # OCR japones vertical
from m_rcnn import *
from visualize import random_colors, get_mask_contours, draw_mask

translator = google_translator()  # traductor
mocr = MangaOcr()  # modelo OCR

def textOnImage(text, img, rect, color=(0, 0, 0)):
    x, y, w, h = rect
    fontFace = cv2.FONT_HERSHEY_DUPLEX
    fontScale = 0.6
    lineType = cv2.LINE_AA
    fontThickness = 1
    wtext = textwrap.wrap(text, width=int((w+12)/12))
    l = len(wtext)
    for i, line in enumerate(wtext):
        textsize = cv2.getTextSize(line, fontFace, fontScale, fontThickness)[0]
        gap = textsize[1] + 10
        cy = int(y + (h - gap) / 2 + (i - l/2 + 1) * gap)
        cx = int(x + (w - textsize[0]) / 2)
        print("cy:",cy,y,h,textsize[1])
        cv2.putText(img, line, (cx, cy), fontFace,
                    fontScale,
                    color,
                    fontThickness,
                    lineType)

    return img
    
def predict(l_img_upl):
    # Ruta del modelo
    RUTA_MODELO = "mrcnn_demo/mask_rcnn_object_0005.h5"
    test_model, inference_config = load_inference_model(1, RUTA_MODELO)
    list_result = []
    for ind, img_upl in enumerate(l_img_upl):
        # Load Image
        img = cv2.cvtColor(numpy.array(img_upl), cv2.COLOR_RGB2BGR)
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Detect results
        r = test_model.detect([image])[0]
        colors = random_colors(80)

        # Get Coordinates and show it on the image
        object_count = len(r["class_ids"])
        st.write("Imagen " + str(ind+1) +
                 " - Diálogos detectados: ", object_count)
        for i in range(object_count):
            # 1. Mask
            mask = r["masks"][:, :, i]
            contours = get_mask_contours(mask)
            for cnt in contours:
                print(i)
                # rectangulo que encierra a la burbuja
                rect = cv2.boundingRect(cnt)
                x, y, w, h = rect
                croped = image[y:y+h, x:x+w].copy()
                # mascara formada por el poligono del modelo de deteccion de texto
                pts = cnt - cnt.min(axis=0)
                mask = np.zeros(croped.shape[:2], np.uint8)
                cv2.drawContours(
                    mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)
                dst = cv2.bitwise_and(croped, croped, mask=mask)

                # Solo con fines ilustrativos, se colorean las burbujas encontradas
                cv2.polylines(image, [cnt], True, colors[i], 2)
                cv2.fillPoly(image, [cnt], color=(255, 255, 255))
                image = draw_mask(image, [cnt], colors[i])

                # OCR y Traduccion
                bubble_path = "/Output/dst" + str(i) + ".png"
                cv2.imwrite(bubble_path, dst)
                bubble_text = mocr(Image.fromarray(dst))
                bubble_traduction = translator.translate(
                    bubble_text, lang_tgt='es')
                bubble_traduction = bubble_traduction.replace("á", "a")
                bubble_traduction = bubble_traduction.replace("ú", "u")
                bubble_traduction = bubble_traduction.replace("ó", "o")
                bubble_traduction = bubble_traduction.replace("é", "e")
                bubble_traduction = bubble_traduction.replace("í", "i")
                bubble_traduction = bubble_traduction.replace("Á", "A")
                bubble_traduction = bubble_traduction.replace("É", "E")
                bubble_traduction = bubble_traduction.replace("Í", "I")
                bubble_traduction = bubble_traduction.replace("Ó", "O")
                bubble_traduction = bubble_traduction.replace("Ú", "U")
                bubble_traduction = bubble_traduction.replace("ñ", "n")
                bubble_traduction = bubble_traduction.replace("Ñ", "N")
                bubble_traduction = bubble_traduction.replace("¿", " ")
                bubble_traduction = bubble_traduction.replace("¡", " ")
                bubble_traduction = bubble_traduction.replace("-", " ")
                bubble_traduction = bubble_traduction.replace("_", " ")

                print(bubble_text, bubble_traduction, sep='\t')

                # text on image
                image = textOnImage(bubble_traduction, image, rect)
        list_result.append(Image.fromarray(image))

    return list_result
