import os
from keras.models import load_model
# import cv2
# import pandas as pd

def predecir(lista, ruta):
    # Cargamos el modelo
    model = load_model('modelo_definitivo.h5')

    # Definimos variables
    i = 1
    classes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    # Recorremos elementos de la lista y mostramos el resultado
    for j, element in enumerate(lista):
        element = element.reshape(-1, 32, 32, 1)
        predictions = model.predict(element)
        probabilities = predictions[0]

        # Obtener el nombre de la imagen actual
        image_name = os.listdir(ruta)[j]

        print(f"Predicción Imagen Nº{i}: - Imagen: {image_name}")
        for letter, probability in zip(classes, probabilities):
            print(f"{letter}: {probability * 100:.2f}%")
        i += 1