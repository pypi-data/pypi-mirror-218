import os
from keras.models import load_model
import cv2
import pandas as pd

def conversor_imagen_modelo(ruta):
    """
    Preprocesa la imagen antes de poderla predecir, para que se ajuste con las imágenes del modelo entrenado.
    Requisitos de la imagen: Debe verse solamente una letra y el fondo debe ser de un color homogéneo. Además debe exsitir un claro contraste entre el color del fondo y el de la letra.

    Args:
        ruta (str): La ruta donde se ubican la imágenes a procesar

    Returns:
        list : Lista que contiene las imágenes preprocesadas.

    Raises:
        FileNotFoundError: Si la ruta o el nombre de archivo no son válidos.
    """

    # Creamos lista para apendear las imágenes leídas
    lista_imagenes=[]
    
    for file in os.listdir(ruta):
        # Leer la imagen
        imagen = cv2.imread(os.path.join(ruta, file))
        # Apendear la imagen en una lista
        lista_imagenes.append(imagen)

    # Creamos listado de imagenes salientes
    lista_imagenes_proc=[]
    # Aplicamos la transformación a cada una de las imágenes
    for imagen in lista_imagenes:

        ############ BÚSQUEDA DE LETRA #############

        # Convierte la imagen a escala de grises
        grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        # Si el contorno de la imagen es menor a 150 (píxeles oscuros) entonces los oscuros los hace más oscuros
        if (imagen[:,0].mean()+imagen[:,-1].mean()+imagen[0,:].mean()+imagen[-1,:].mean())/4<150:
            # Aplica un umbral para separar la letra del ruido
            _, umbral = cv2.threshold(grises, 127, 255, cv2.THRESH_BINARY+ cv2.THRESH_OTSU)
        # Si el contorno de la imagen es menor a 150 (píxeles oscuros) entonces los oscuros los hace blancos
        else:
            _, umbral = cv2.threshold(grises, 127, 255, cv2.THRESH_BINARY_INV+ cv2.THRESH_OTSU)
        # Encuentra los contornos en la imagen umbralizada
        contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Encuentra el contorno más grande
        contorno_letra = max(contornos, key=cv2.contourArea)
        # Encuentra las coordenadas del rectángulo que encierra el contorno
        x, y, w, h = cv2.boundingRect(contorno_letra)
        dim_rectangulo=(x, y, w, h)

        ############## RECORTE CUADRADO #############
        ############ ELIMINACIÓN BORDES #############

        largo=imagen.shape[0]
        ancho=imagen.shape[1]
        # Según el lado más ancho del rectángulo aplicamos unos recortes u otros
        if h>w:
            # Las imágenes usadas en entrenamiento tienen un borde con proporcionalidad 2/28 píxeles, es decir, 2 píxeles por 28 píxeles de tamaña de letra
            # Recortamos la imagen para que se cumpla esa proporcionalidad antes de aplicar el resize
            imagen=imagen[max(y-int(h*(2/28)),4):y+h+int(h*(2/28)), max(x-int(h/2-w/2+h*(2/28)),4):x+int(w/2+h/2+h*(2/28))]
        else:
            imagen=imagen[max(y-int(w*(2/28)),4):y+w+int(w*(2/28)), max(x-int(w/2-h/2+w*(2/28)),4):x+int(h/2+w/2+w*(2/28))]

        ########### COLOR BLANCO Y NEGRO ############

        # Pasamos la imagen a gris paras facilitar el treshold siguiente. Además esto implica pasar de 3 capas a 1
        imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        # Aplicamos threshold para que los píxeles por debajo de 127 los ponga en blanco y por arriba en negro
        (thresh, imagen) = cv2.threshold(imagen_gris, 127, 255, cv2.THRESH_BINARY)
        # Si los colores de los pixeles de los extremos (que representan el contorno) son negros, aplicamos transformación
        if (imagen[:,0].mean()+imagen[:,-1].mean()+imagen[0,:].mean()+imagen[-1,:].mean())/4 >= 150:
            # Cambiamos píxeles negros por blancos y viceversa
            imagen = cv2.bitwise_not(imagen)
        else:
            pass

        ################## RESIZE ###################

        # Aplicamos resiez al tamaño de las imágenes del dataset de entrenamiento
        imagen=cv2.resize(imagen, (32,32), interpolation = cv2.INTER_AREA)
        # Apendeamos imagen resultante a la lista
        lista_imagenes_proc.append(imagen)

    return lista_imagenes_proc

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