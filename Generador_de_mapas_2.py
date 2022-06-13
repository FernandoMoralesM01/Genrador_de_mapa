import geopy.distance
import pandas as pd
import numpy as np
import folium
from folium import plugins

def Ingresa_nombre_de_archivo():
    nombre = input ("Dame nombre o ruta de tu archivo: ")
    return nombre

def Validar_tipo(Lat, Lon, Tipologia, Nombre):   
    esValido = True
    tipo = 'No especificado'

    Tipologia = str(Tipologia)
    Tipologia = Tipologia.lower()

    Nombre = str(Nombre)
    Nombre = Nombre.lower()

    if (Nombre.count('hospital') > 0 or Tipologia.count('hospital') > 0 or Nombre.count('cent') > 0 or Nombre.count('hg') > 0 or  Nombre.count('h. g. ') > 0):
        tipo = 'HOSPITAL'
    if (Nombre.count('cl') > 0 or Tipologia.count('cl') > 0):
        tipo = 'CLINICA'
    if(Nombre.count('sana') > 0):
        tipo = 'SANATORIO'
    if(Nombre.count('consultorio') > 0 or Nombre.count('bata') > 0):
        tipo = 'CONSULTORIO'

    
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

def  agregar_descripcion(nombre, Lat, Lon, tecnologias):
    Lat = float(Lat)
    Lon = float(Lon)
    coords1 = str(Lat) + ", " + str(Lon)
    coords2 = "19.419886, -99.298375"
    dist = float (geopy.distance.geodesic(coords1, coords2).km)
    dist = round(dist, 3)

    nombre = str(nombre)
    nombre = nombre.lower()

    Nombres_tec = pd.DataFrame(tecnologias, columns= ['Hospital / Unidad Médica'])
    Nombres_tec = np.array(Nombres_tec)
    

    Arr_Tec = pd.DataFrame(tecnologias, columns= ['Hospital / Unidad Médica', 'Equipo', 'Descripción', 'Marca', 'Modelo', 'Cantidad', 'Latitude', 'Longitude'])
    #Arr_tec                                               [0]                   [1]        [2]          [3]       [4]        [5]         [6]        [7]
    Arr_Tec = np.array(Arr_Tec)
    
    siCoincide = False
    Ncoinc = 5
    html = ""
    
    upperHtml = "<html>  <head>     <style>     {         box-sizing: content-box;     }     /* Set additional styling options for the columns*/     .column {     float: left;     width: 1%;     }      .row:after {     content: "";     display: table;     clear: both;     }     </style>  </head>  <body>"
    html += '<br class="row">' + '<div class="column" style="background-color:#FFFFFF;"> <h4>'+ 'Distancia' +' </h4> <p>' + str(dist) + ' km </p> </div>' + '<div class="column" style="background-color:#FFFFFF;"> <h4>'+ 'Tiempo' +' </h4> </div> </br></br></br></br></br></br></div>'
    html += '<br class="row">' + '<div class="column" style="background-color:#FFFFFF;"> <h4>'+ 'EQUIPO' +' </h4> </div>' + '<div class="column" style="background-color:#FFFFFF;"> <h4>'+ 'MARCA' +' </h4> </div>' + '<div class="column" style="background-color:#FFFFFF;"> <h4>'+ 'MODELO' +' </h4> </div>' + '</br></br></br></div>'
    siDatos = 0
    i = 0
    for aString in Nombres_tec:
        aString = str(aString)
        aString = (aString[2: (len(aString) - 2)])
        aString = aString.lower()

        palabras = aString.split(" /")
        aString = ""
        
        for palabra in palabras:
            aString += palabra

    

        countPalabra = 0
        palabras = aString.split()
        for palabra in palabras:
            if(nombre.count(palabra) > 0 and nombre.count(palabra) < 2):
                countPalabra += 1
        #print("...", aString)
        if(aString.count(" ") < 4):
            Ncoinc = 4
            
        if (aString.count(nombre) > 0 or countPalabra >= Ncoinc or siCoincide == True):
            #print(nombre, aString)
            siDatos = 1
            equipo = str(Arr_Tec[i][1])
            marca =  str(Arr_Tec[i][3])
            modelo = str(Arr_Tec[i][4])
            cantidad = str(Arr_Tec[i][5])

            
            equipo = '<div class="column" style="background-color:#FFFFFF;"> <p>' + cantidad + '&nbsp;-&nbsp;'+equipo +' </p> </div>'
            marca = '<div class="column" style="background-color:#FFFFFF;"> <p>' + marca +' </p> </div>'
            modelo = '<div class="column" style="background-color:#FFFFFF;"> <p>' + modelo +' </p> </div>'
            
            
            html += '<br class="row">' + equipo + marca + modelo + '</br></br></br></div>'

            
        
        i += 1

    if(siDatos == 0):
        #html = '<html>  <head>     <style>     {         box-sizing: border-box;     }     /* Set additional styling options for the columns*/     .column {     float: left;     width: 1%;     }      .row:after {     content: "";     display: table;     clear: both;     }     </style>  </head>  <body>     <div class="row">         <div class="column" style="background-color:#FFB695;">             <h2>Column 1</h2>             <p>Data..</p>         </div>         <div class="column" style="background-color:#96D1CD;">             <h2>Column 2</h2>             <p>Data..</p>         </div>     </div>      <div class="row">         <div class="column" style="background-color:#FFB695;">             <h2>Column 1</h2>             <p>Data..</p>         </div>         <div class="column" style="background-color:#96D1CD;">             <h2>Column 2</h2>             <p>Data..</p>         </div>     </div>  </body> </html>'
        html = upperHtml + '<br class="row">' + '<div class="column" style="background-color:#FFFFFF;"> <h4>'+ 'Distancia' +' </h4> <p>' + str(dist) + ' km </p> </div> </br></br></br></br></br></br>' + '<div class="column" style="background-color:#FFFFFF;"> <h4>'+ 'Tiempo' +' </h4> </div> </br></br></br></br></br></br></div>' + '  </body> </html>'
        iframe = folium.IFrame(html,
                        width= 200,
                        height=150)

    else:
        
        html = upperHtml + html + '  </body> </html>'
        iframe = folium.IFrame(html,
                        width=14000,
                        height=300)
    
    return [iframe, 450, siDatos]


def Insertar_marcador(Cords, Tipologia, Nombre, tecnologias, Mapa):

    txt_popup = "hola"
    mx_wth = 500

    Tipologia = str(Tipologia)
    Tipologia = (Tipologia[2: (len(Tipologia) - 2)])

    Nombre = str(Nombre)
    Nombre = (Nombre[2: (len(Nombre) - 2)])

    Lat = float(Cords[0])
    Lon = float(Cords[1])
    siDatos = 0
    [siValido, icono, ic_color, Lat, Lon] = Validar_tipo(Lat, Lon, Tipologia, Nombre)    
    [txt_popup, mx_wth, siDatos] = agregar_descripcion(Nombre, Lat, Lon, tecnologias)
    
    if(siValido):
        folium.Marker(location=[Lat, Lon], 
                icon= folium.Icon(icon= icono, prefix= 'fa', color= ic_color),
                tooltip= Nombre, 
                popup=folium.Popup(txt_popup, max_width= mx_wth)).add_to(Mapa)


def Generar_marcadores (hospital, tecnologias, Mapa):
    
    Cords = pd.DataFrame(hospital, columns= ['LATITUD', 'LONGITUD'])
    Cords = np.array(Cords)
    
    #Mapa.add_child(plugins.HeatMap(Cords[0:len(Cords)]))

    Nombres = pd.DataFrame(hospital, columns= ['NOMBRE DE LA UNIDAD'])
    Nombres = np.array(Nombres)

    Nombre_de_Tipologia = pd.DataFrame(hospital, columns= ['NOMBRE DE TIPOLOGIA'])
    Nombre_de_Tipologia = np.array(Nombre_de_Tipologia)

    i = 0
    for Nombre in Nombres:
        Insertar_marcador(Cords[i], Nombre_de_Tipologia[i], Nombre, tecnologias, Mapa)
        i+=1


def Generar_mapa_con_marcadores(N_arch):

    N_arch = (N_arch[1: (len(N_arch) - 1)])
    print(N_arch)

    Mapa = folium.Map(zoom_start= 12, location=[19.419886, -99.298375])   #Genera un Mapa nuevo
    
    folium.Marker(location=[19.419886, -99.298375], 
                icon= folium.Icon(icon= "hospital-o", prefix= 'fa', color= "orange"),
                tooltip= "TERRENO HADASAH", 
                popup=folium.Popup("Bosque Real Huixquilucan de Degollado, State of Mexico", max_width= 200)).add_to(Mapa)


    hospital = pd.read_excel (N_arch, sheet_name= 'HOSPITAL')
    tecnologias = pd.read_excel (N_arch, sheet_name= 'TECNOLOGÍAS MÉDICAS')

    Generar_marcadores (hospital, tecnologias, Mapa)
    
    N_arch = N_arch[0: len(N_arch) - 5]
    Mapa.save(N_arch + '_Map.html')  #Guarda el mapa en la dirección el excel

def Generar_mapa_de_calor(N_arch):
    N_arch = (N_arch[1: (len(N_arch) - 1)])
    print(N_arch)
    Mapa = folium.Map(zoom_start= 12, location=[19.419886, -99.298375])   #Genera un Mapa nuevo
    hospital = pd.read_excel (N_arch, sheet_name= 'HOSPITAL')
    Cords = pd.DataFrame(hospital, columns= ['LATITUD', 'LONGITUD'])
    Cords = np.array(Cords)
    print(Cords)
    Mapa.add_child(plugins.HeatMap(Cords[0:len(Cords)]))

    N_arch = N_arch[0: len(N_arch) - 5]
    Mapa.save(N_arch + '_HeatMap.html')  #Guarda el mapa en la dirección el excel
    return 0

#MAIN
N_arch =Ingresa_nombre_de_archivo()
Generar_mapa_con_marcadores(N_arch)
Generar_mapa_de_calor(N_arch)

#"C:\Users\fercy\Desktop\proyekta medica\PM - Hadassah_Hospital Data.xlsx"