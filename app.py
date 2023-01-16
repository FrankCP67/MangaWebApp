import io
from predict import predict
from PIL import Image
import streamlit as st


def load_images():
    st.subheader("Seleccione imagenes para procesar:")
    list_uploaded_file = st.file_uploader(label="Input", type=['png', 'jpg', 'jpeg'] , label_visibility="collapsed", accept_multiple_files=True)
    with st.container():
        if list_uploaded_file is not None:
            list = []
            for i, uploaded_file in enumerate(list_uploaded_file):
                image_data = uploaded_file.getvalue()
                st.write("##### Imagen " + str(i+1) + ":")
                st.image(image_data)
                st.write("")
                list.append(Image.open(io.BytesIO(image_data)))
            return list
        else:
            return None


def main():
    st.set_page_config(page_title="Manga WebApp", layout="wide", menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "FIIS UNI 2022"
    })
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)
    st.title('Manga WebApp')
    col1, col2 = st.columns(2, gap="large")
    with col1:
        list_img = load_images()
    with col2:
        if list_img:
            st.subheader('Ahora presione el botón para procesar:')
            result = st.button('Procesar')
            if result:
                l_im2 = None
                if l_im2 is None:
                    st.write("Procesando ...")
                l_im2 = predict(list_img)
                st.subheader("Paneles reconocidos:")
                for i, im2 in enumerate(l_im2):
                    st.write("##### Imagen " + str(i+1) + ":")
                    st.image(im2)
                    st.write("")


if __name__ == '__main__':
    main()
