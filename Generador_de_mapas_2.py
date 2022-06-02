from re import T
import pandas as pd
import numpy as np
import folium

def Ingresa_nombre_de_archivo():
    nombre = input ("Dame nombre o ruta de tu archivo: ")
    return nombre



def Insertar_marcador(Cords, Tipologia, Nombre, tecnologias):

    Tipologia = str(Tipologia)
    Tipologia = (Tipologia[2: (len(Tipologia) - 2)])

    Nombre = str(Nombre)
    Nombre = (Nombre[2: (len(Nombre) - 2)])

    print(Nombre, Tipologia, "\n")


def Generar_marcadores (hospital, tecnologias):
    
    Cords = pd.DataFrame(hospital, columns= ['LATITUD', 'LONGITUD'])
    Cords = np.array(Cords)
    
    Nombres = pd.DataFrame(hospital, columns= ['NOMBRE DE LA UNIDAD'])
    Nombres = np.array(Nombres)

    Nombre_de_Tipologia = pd.DataFrame(hospital, columns= ['NOMBRE DE TIPOLOGIA'])
    Nombre_de_Tipologia = np.array(Nombre_de_Tipologia)

    i = 0
    for Nombre in Nombres:
        Insertar_marcador(Cords[i], Nombre_de_Tipologia[i], Nombre, tecnologias)
        i+=1


def Generar_mapa(N_arch):
    Mapa = folium.Map(zoom_start= 12, location=[19.4385309, -99.2088913])   #Genera un Mapa nuevo
    
    hospital = pd.read_excel (N_arch, sheet_name= 'HOSPITAL')
    tecnologias = pd.read_excel (N_arch, sheet_name= 'TECNOLOGÍAS MÉDICAS')

    Generar_marcadores (hospital, tecnologias)

    Mapa.save(N_arch + 'Map.html')  #Guarda el mapa en la dirección el excel

#MAIN
Generar_mapa(N_arch =Ingresa_nombre_de_archivo())