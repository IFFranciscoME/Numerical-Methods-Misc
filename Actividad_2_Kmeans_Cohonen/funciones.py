
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: IDI-II: Ejercicio con Kmeans
# -- codigo: funciones.py
# -- repositorio: https://github.com/IFFranciscoME/IDI_II_GIT
# -- ------------------------------------------------------------------------------------ -- #

import numpy as np
import random
import os
import copy
from PIL import Image as im


# -- ------------------------------------------------------- FUNCION: Lectura de imagenes -- #
# -- ------------------------------------------------------------------------------------ -- #
def f_entrada_imagenes(param_nombre):
    """
    Parameters
    ----------
    param_nombre : str : Nombre del archivo a leer

    Returns
    -------

    Debugging
    ---------
    param_nombre = 'bandera_mexico.jpg'

    """

    # obtener directorio de trabajo actual para encontrar ~/imagenes/archivo.jpg
    directorio = os.getcwd()
    # cargar archivo
    archivo_imagen = im.open(directorio + '/imagenes/' + param_nombre)
    # dejar como array a los datos obtenidos de la imagen
    imagen = np.array(archivo_imagen)
    # asegurarse que el array es escribible
    imagen.setflags(write=True)
    # proceso para hacer reshape y ordenar los datos en N renglones y 3 columnas
    total = archivo_imagen.size[0]*archivo_imagen.size[1]
    # reacomodar para tener todos los datos en una matriz vertical
    imagen = np.reshape(imagen, (total, 3))
    # crear un array de 0s y 4 columnas
    datos_imagen = np.zeros((total, 4))
    # escribir los datos de los pixeles (3 componentes) y una 4 para apoyo posterior
    datos_imagen[:, :-1] = imagen

    return {'datos': datos_imagen, 'dimensiones': archivo_imagen.size}


# -- --------------------------------------------------------- FUNCION: Metodo de K-Means -- #
# -- ------------------------------------------------------------------------------------ -- #
def f_kmeans(param_data, param_k, param_iter):
    """

    Parameters
    ----------
    param_data : np.array : array con N cantidad de columnas para N dimensiones
    param_k : int : cantidad de clusters a utilizar para la clasificacion
    param_iter : int : cantidad de iteraciones

    Returns
    -------
    {'datos': k_means_data, 'centroides': centroides}

    Debugging
    ---------
    param_data = imagen['datos']
    param_k = 3
    param_iter = 50

    """

    # copia original de los datos de entrada
    array_final = copy.deepcopy(param_data)

    # quitar 4 columna
    param_data = param_data[:, :-1]

    # dimensiones
    m = param_data.shape[0]
    n = param_data.shape[1]
    # objeto vacio para almacenar n cantidad de centroides
    centroides = np.array([]).reshape(n, 0)
    # objeto vacio para guardar todos los resultados de las iteraciones
    k_means_data = dict()
    # -------------------------------------------------------------------------------------- #

    # crear una param_k cantidad de centroides aleatorios
    for _ in range(param_k):
        centroides = np.c_[centroides, param_data[random.randint(0, m - 1)]]

    # -------------------------------------------------------------------------------------- #

    # iteraciones de busqueda y ajuste
    for i in range(param_iter):

        # objeto con distancias euclidianas
        euclidianas = np.array([]).reshape(m, 0)

        # para cada centroide calcular las distancias a cada punto
        for k in range(param_k):
            # distancia euclidiana de cada punto con cada centroide
            distancias = np.sum((param_data - centroides[:, k]) ** 2, axis=1)
            # concatenar para cada punto sus distancias con cada centroide
            euclidianas = np.c_[euclidianas, distancias]

        # encontrar indice de columna con la distancia minima de cada punto a cada centroide
        cent_ind = np.argmin(euclidianas, axis=1) + 1
        cent_data = {}

        # una lista de arrays, uno para cada centroide
        for lista in range(param_k):
            cent_data[lista + 1] = np.array([]).reshape(n, 0)

        # asociar datos a su centroide y concatenar todos los centroides
        for con in range(m):
            cent_data[cent_ind[con]] = np.c_[cent_data[cent_ind[con]], param_data[con]]

        # reacomodo de datos y parametro de k-mean
        for dato in range(param_k):
            # dar formato a arrays de datos en centroides
            # cent_data[dato + 1] = cent_data[dato + 1].T
            cent_data[dato + 1] = cent_data[dato + 1].T
            # calcular el promedio de distancias de datos al centroide para cada centroide
            centroides[:, dato] = np.mean(cent_data[dato + 1], axis=0)

        # Dejar resultados finales en un diccionario
        k_means_data.update(cent_data)

    # reacomodar datos con en formato original de entrada
    k_means_a_data = np.concatenate([v for k, v in sorted(k_means_data.items())], 0)

    # lista de centroides a los que pertenece cada dato
    cents = list(k_means_data.keys())
    cents = [np.repeat(i, len(k_means_data[i])) for i in cents]
    cents = np.concatenate((cents[0], cents[1], cents[2]))

    # generar array final con datos originales + centroide al que pertenencen
    nuevos_datos = np.zeros((len(cents), 4))
    nuevos_datos[:, :-1] = k_means_a_data
    array_final[:, 3] = cents

    return {'datos': array_final, 'centroides': centroides}


# -- --------------------------------------------------------- FUNCION: Metodo de K-Means -- #
# -- ------------------------------------------------------------------------------------ -- #

def f_reescribir_imagen(param_data, param_dims, param_nombre):
    """
    Parameters
    ----------
    param_data :
    param_dims : np.array : con dimensiones de la imagen de salida
    param_nombre :

    Returns
    -------


    Debugging
    ---------
    param_dims = imagen['dimensiones']
    param_data = r_kmeans['datos']
    param_nombre = 'kmeans_salida.jpg'

    """

    imagen = np.reshape(param_data[:, 0:3], (param_dims[0], param_dims[1], 3))
    datos = imagen.astype(np.uint8)
    nueva_imagen = im.fromarray(datos)

    directorio = os.getcwd()
    nueva_imagen.save(directorio + '/imagenes/' + param_nombre)

    return 1
