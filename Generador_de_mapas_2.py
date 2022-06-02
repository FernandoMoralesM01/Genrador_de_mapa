import pandas as pd
import numpy as np
import folium

def Ingresa_nombre_de_archivo():
    nombre = input ("Dame nombre o ruta de tu archivo: ")
    return nombre

def Validar_tipo(Lat, Lon, Tipologia, Nombre):   
    esValido = True
    tipo = 'NOSE'

    Tipologia = str(Tipologia)
    Tipologia = Tipologia.lower()

    Nombre = str(Nombre)
    Nombre = Nombre.lower()

    if (Nombre.count('hospital') > 0 or Tipologia.count('hospital') > 0 or Nombre.count('centro') > 0):
        tipo = 'HOSPITAL'
    if (Nombre.count('cl') > 0 or Tipologia.count('cl') > 0):
        tipo = 'CLINICA'
    if(Nombre.count('sana') > 0):
        tipo = 'SANATORIO'
    if(Nombre.count('consultorio') > 0):
        tipo = 'CONSULTORIO'

    
    print(tipo)
    if(tipo == 'HOSPITAL'):
        icon = "hospital-o"
        icon_color = "red"
    else:
        if(tipo == 'CLINICA'):
            icon = "user-md "
            icon_color = "blue"
        else:
            if(tipo == 'SANATORIO'):
                icon = "medkit "
                icon_color = "green"
            else:
                if(tipo == 'CONSULTORIO'):
                    icon = "stethoscope"
                    icon_color = "pink"
                else:
                    icon = "binoculars"
                    icon_color = "black"
        
    return [esValido, icon, icon_color, Lat, Lon]

def Insertar_marcador(Cords, Tipologia, Nombre, tecnologias, Mapa):

    txt_popit = "hola"
    mx_wth = 500

    Tipologia = str(Tipologia)
    Tipologia = (Tipologia[2: (len(Tipologia) - 2)])

    Nombre = str(Nombre)
    Nombre = (Nombre[2: (len(Nombre) - 2)])

    Lat = float(Cords[0])
    Lon = float(Cords[1])

    [siValido, icono, ic_color, Lat, Lon] = Validar_tipo(Lat, Lon, Tipologia, Nombre)    
    if(siValido):
        folium.Marker(location=[Lat, Lon], 
                icon= folium.Icon(icon= icono, prefix= 'fa', color= ic_color),
                tooltip= Nombre, 
                popup=folium.Popup(txt_popit, max_width= mx_wth)).add_to(Mapa)


def Generar_marcadores (hospital, tecnologias, Mapa):
    
    Cords = pd.DataFrame(hospital, columns= ['LATITUD', 'LONGITUD'])
    Cords = np.array(Cords)
    
    Nombres = pd.DataFrame(hospital, columns= ['NOMBRE DE LA UNIDAD'])
    Nombres = np.array(Nombres)

    Nombre_de_Tipologia = pd.DataFrame(hospital, columns= ['NOMBRE DE TIPOLOGIA'])
    Nombre_de_Tipologia = np.array(Nombre_de_Tipologia)

    i = 0
    for Nombre in Nombres:
        Insertar_marcador(Cords[i], Nombre_de_Tipologia[i], Nombre, tecnologias, Mapa)
        i+=1


def Generar_mapa(N_arch):

    N_arch = (N_arch[1: (len(N_arch) - 1)])
    print(N_arch)

    Mapa = folium.Map(zoom_start= 12, location=[19.4385309, -99.2088913])   #Genera un Mapa nuevo
    
    hospital = pd.read_excel (N_arch, sheet_name= 'HOSPITAL')
    tecnologias = pd.read_excel (N_arch, sheet_name= 'TECNOLOGÍAS MÉDICAS')

    Generar_marcadores (hospital, tecnologias, Mapa)

    Mapa.save(N_arch + 'Map.html')  #Guarda el mapa en la dirección el excel

#MAIN
Generar_mapa(N_arch =Ingresa_nombre_de_archivo())