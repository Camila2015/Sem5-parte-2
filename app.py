import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

st.title("Conversión de Texto a Audio")

# Cambiar imagen por Caperucita-Roja.jpg
image = Image.open('Caperucita-Roja.jpg')
st.image(image, width=350)

with st.sidebar:
    st.subheader("Escribe y/o selecciona texto para ser escuchado.")

# Crear carpeta temporal si no existe
try:
    os.mkdir("temp")
except:
    pass

# Texto de la fábula de Caperucita Roja
st.subheader("La fábula de Caperucita Roja")
st.write('''Había una vez una niña muy bonita. Su madre le había hecho una pequeña capa roja, 
    y como le sentaba tan bien, todos la llamaban Caperucita Roja. Un día su madre le pidió que 
    llevase unos pastelillos a su abuela, que vivía al otro lado del bosque, recomendándole que no 
    se entretuviese por el camino, pues cruzar el bosque era muy peligroso, ya que siempre andaba 
    por allí el lobo. Caperucita Roja recogió la cesta con los pastelillos y se puso en camino. 
    La niña tuvo que atravesar el bosque para llegar a casa de su abuelita. Cuando estaba en el bosque, 
    se encontró con el lobo, pero Caperucita no sabía que era un animal tan peligroso, así que no tuvo miedo.''')

st.markdown(f"¿Quieres escucharlo? Copia el texto a continuación para convertirlo en audio.")

# Campo de texto para que el usuario copie la fábula u otro texto
text = st.text_area("Ingrese el texto a escuchar.")

# Selección del lenguaje
option_lang = st.selectbox(
    "Selecciona el lenguaje",
    ("Español", "English")
)

lg = 'es' if option_lang == "Español" else 'en'

# Función para convertir texto a audio
def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20]  # Nombre del archivo con los primeros 20 caracteres del texto
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name

# Definir la animación con CSS
def add_custom_css():
    custom_css = """
    <style>
    .spinner {
        border: 8px solid #f3f3f3;
        border-radius: 50%;
        border-top: 8px solid #3498db;
        width: 60px;
        height: 60px;
        -webkit-animation: spin 2s linear infinite; /* Safari */
        animation: spin 2s linear infinite;
        margin: auto;
    }

    @-webkit-keyframes spin {
        0% { -webkit-transform: rotate(0deg); }
        100% { -webkit-transform: rotate(360deg); }
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# Mostrar la animación al convertir el texto a audio
if st.button("Convertir a Audio"):
    add_custom_css()  # Añadir la animación CSS
    st.markdown('<div class="spinner"></div>', unsafe_allow_html=True)  # Mostrar la animación

    time.sleep(2)  # Simula el tiempo de procesamiento

    # Convertir el texto a audio
    result = text_to_speech(text, lg)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    
    # Mostrar el audio
    st.markdown(f"## Tú audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

# Función para eliminar archivos antiguos
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

# Eliminar archivos después de 7 días
remove_files(7)
