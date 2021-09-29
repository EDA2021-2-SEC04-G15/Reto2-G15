"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import time
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Sorting import quicksort as qs
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo de obrs y artistar. Crea una lista vacia para guardar
    todos  Retorna el catalogo inicializado.
    """
    catalog = {'artists': None,
               'artworks': None,
               'nationalities': None,
               'tecnicas' : None}

    
    catalog['artists'] = lt.newList('ARRAY_LIST')
    catalog['artworks'] = lt.newList('ARRAY_LIST')
    catalog['nationalities'] = lt.newList('ARRAY_LIST')


    ### funciones de creación de mapas #####

    """
    Este indice crea un map cuya llave es la tecnica de la obra
    """
    catalog['tecnicas'] = mp.newMap(300,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareMapMedium)

    return catalog

# Funciones para agregar informacion al catalogo

def addArtist(catalog, artist):
    # Se adiciona el artista a la lista de artistas
    lt.addLast(catalog['artists'], artist)
   
def addArtwork(catalog, artwork):
    # Se agrega una obra a la lista de obras
    lt.addLast(catalog['artworks'], artwork)
    # se añaden los detalles de la obra a la lista de nacionalidades
    addArtworkNationlities(catalog, artwork)

    # se añade la informacion al mapa de mediums

    addArtworkMedium(catalog, artwork)


def addArtworkMedium(catalog, artwork):

    try:
        mediums = catalog['tecnicas']
        if (artwork['Medium'] != ''):
            pubmedium = (artwork['Medium'])
        else:
            pubmedium = 'unknown'
        existmedium = mp.contains(mediums, pubmedium)
        if existmedium:
            entry = mp.get(mediums, pubmedium)
            medium = me.getValue(entry)
        else:
            medium = newMedium(pubmedium)
            mp.put(mediums, pubmedium, medium)
        lt.addLast(medium['artworks'], artwork)
    except Exception:
        return None


def newMedium(pubmedium):
    entry ={'medium':'', 'artworks':None}
    entry['medium'] = pubmedium
    entry['artworks'] = lt.newList('ARRAY_LIST')
    return entry



def addArtworkNationlities(catalog, artwork):

    constituentids = artwork['ConstituentID']
    artists = ArtistByID_v2(catalog, constituentids)

    for artist in lt.iterator(artists):
        addNationality(catalog, artwork, artist)



# Funciones para creacion de datos

def addNationality(catalog, artwork, artist):
    nationality = artist['Nationality']
    if nationality == "":
        nationality = "Nationality unknown"
    nationalities = catalog['nationalities']
    encontro = False
    for country in lt.iterator(nationalities):
        compare = country['name']
        if compare == nationality:
            lt.addLast(country['artworks'], artwork)
            country['size'] +=1
            encontro = True
    
    if encontro == False:
        country2 = newNationlity(nationality)
        artworks2 = country2['artworks']
        lt.addLast(artworks2, artwork)
        country2['size'] +=1
        encontro = True
        lt.addLast(nationalities, country2)


def newNationlity(nationality):
    """
    Crea una nueva estructura para almacenar las obras de una nacionalidad
    """
    country = {'name': "", "artworks": None, "size" : 0 }
    country['name'] = nationality
    country['artworks'] = lt.newList('ARRAY_LIST')
    return country


# Funciones de consulta


def getArtworksByMedium(catalog, medium):
    """
    Retorna los libros publicados en un año
    """
    medium = mp.get(catalog['tecnicas'], medium)
    if medium:
        return me.getValue(medium)['artworks']
    return None


def getArtistsInDateRange (catalog, year1, year2):
    """"
    Retorna lista desordenada de artistas en un rango de años
    """
    artists = catalog["artists"]
    artistsInRange= lt.newList(datastructure= "ARRAY_LIST")
    for artist in lt.iterator(artists):
        if int(artist["BeginDate"]) >= year1 and int(artist["BeginDate"]) <= year2:
            lt.addLast(artistsInRange, artist)
    return artistsInRange

def getArtworksInDeparment(catalog, department):
    """
    Retorna lista desordenada de artworks en un departamento en específico
    Agrega el costo de transporte a una nueva categoria dentro del artwork
    Retorna costo total, numero de obras, y peso estimado
    """
    artworks = catalog['artworks']
    artworksInDept = lt.newList(datastructure="ARRAY_LIST")
    costo_total = 0
    peso_total = 0
    obras = 0
    for artwork in lt.iterator(artworks):
        if artwork['Department'] == department:
            lt.addLast(artworksInDept,artwork)
            artwork['cost'] = getTansportCost(artwork)
            costo = artwork['cost']
            costo_total += costo
            try:
                peso = float(artwork['Weight (kg)'])
            except:
                peso = 0
            peso_total+= peso
            obras+=1

    costo_total = costo_total.__round__(2)
    peso_total = peso_total.__round__(2)

    return artworksInDept, obras, costo_total, peso_total


def getTansportCost(artwork):
    weight = artwork['Weight (kg)']
    width = artwork['Width (cm)']
    height = artwork['Height (cm)']
    depth = artwork['Depth (cm)']

    posibles_costos =[]
    costo_final = 0

    if weight == "":
        weight = "0"
    if width == "":
        width = "0"
    if height == "":
        height = "0"
    if depth == "":
        depth = "0"

    r1 = float(weight)*72
    r2 = (float(width)/100)*(float(height)/100)*(float(depth)/100)*72
    r3 = (float(width)/100)*(float(height)/100)*72
    r4 = (float(width)/100)*(float(depth)/100)*72
    r5 = (float(height)/100)*(float(depth)/100)*72

    posibles_costos.append(r1)
    posibles_costos.append(r2)
    posibles_costos.append(r3)
    posibles_costos.append(r4)
    posibles_costos.append(r5)
    posibles_costos.sort()

    if posibles_costos[4] != 0:
        costo_final = posibles_costos[4]
    else:
        costo_final = 48.0

    return costo_final

def getArtworksInDateRange (catalog, year1, year2):
    """"
    Retorna lista desordenada de artworks en un rango de fechas utilizando el comparador cmpArtwork
    """
    artworks = catalog["artworks"]
    artworksInRange= lt.newList(datastructure= "ARRAY_LIST")
    for artwork in lt.iterator(artworks):
        if (cmpArtworkByDateAcquired(artwork,year2)) and not (cmpArtworkByDateAcquired(artwork, year1)):
            lt.addLast(artworksInRange, artwork)
    return artworksInRange

def purchasedAmount (artworksInRange):

    k = 0
    t = "purchase"
    for artwork in lt.iterator(artworksInRange):
       posible = artwork["CreditLine"].lower()
       if t in posible:
           k+=1
    return k

def searchArtistByID(catalog, constituentids):

    artists = catalog['artists']
    ID_list = constituentids.strip("[]").split(", ")
    artists_names=lt.newList('ARRAY_LIST')
    for id in ID_list:
        corte = 0
        while corte == 0:
            for artist in lt.iterator(artists):
                if artist["ConstituentID"] == id:
                    lt.addLast(artists_names,artist['DisplayName'])
                    corte = 1

    return artists_names

def ArtistByID_v2(catalog, constituentids):

    artists = catalog['artists']
    ID_list = constituentids.strip("[]").split(", ")
    result = lt.newList('ARRAY_LIST')
    number_artists = len(ID_list)
    corte = 0
    for artist in lt.iterator(artists):
        if artist['ConstituentID'] in ID_list:
            lt.addLast(result,artist)
            corte+=1
        if corte == number_artists:
            break
    
    return result
                
def getArtworksByTechnique(catalog, technique):
    artworks = catalog['artworks']
    techniqueList = technique.strip("[]").split(", ")
    artworksNames = lt.newList('ARRAY_LIST')
    numberArtworks = len(techniqueList)
    
 

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpArtworkByTransportCost(artwork1, artwork2):
    cost1 = artwork1['cost']
    cost2 = artwork2['cost']
    result = cost1 > cost2
    return result

def cmpArtworkByDate(artwork1, artwork2):
    
    try:
        date1= int(artwork1['Date'])
    except:
        date1 = 3000
    
    try:
        date2= int(artwork2['Date'])
    except:
        date2 = 3000

    result = date1 < date2
    return result

def cmpCountryByArtworksStored(country1, country2):

    result = country1['size'] > country2['size']
    return result

def cmpArtistsByBeginDate (artist1, artist2):

    result = int(artist1["BeginDate"]) < int(artist2["BeginDate"])
    return result

def cmpArtworkByDateAcquired(artwork1 , artwork2):

                ### Devuelve True si el 'DateAcquired' de 
                # artwork1 es menor que el de artwork2

    date1 = artwork1['DateAcquired'].split('-')
    date2 = artwork2['DateAcquired'].split('-')

    if date1 == [""]:
        date1=["3000","00","00"]
    if date2 == [""]:
        date2=["3000","00","00"]

    resultado = True

    if date1[0] > date2[0]:
        resultado = False
    elif date1[0] == date2[0]:
        if date1[1] > date2[1]:
            resultado = False
        elif date1[1] == date2[1]:
            if date1[2] > date2[2]:
                resultado = False
    
    return(resultado)

def cmpArtworksByTechnique(technique1, technique2):
    result = technique1['Medium'] > technique2['Medium']
    return result


# Funciones de ordenamiento

def sortArtists (artistsInRange):
    sub_list = lt.subList(artistsInRange, 1, lt.size(artistsInRange))
    sub_list = sub_list.copy()
    start_time = time.process_time()
    sorted_list = ms.sort(sub_list, cmpArtistsByBeginDate)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list

def sortArtworksInDeptByDate(artworksInDept):
    sub_list = lt.subList(artworksInDept, 1, lt.size(artworksInDept))
    sub_list = sub_list.copy()
    start_time = time.process_time()
    sorted_list = ms.sort(sub_list, cmpArtworkByDate)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list

def sortArtworksInDeptByTransportCost(artworksInDept):
    sub_list = lt.subList(artworksInDept, 1, lt.size(artworksInDept))
    sub_list = sub_list.copy()
    start_time = time.process_time()
    sorted_list = ms.sort(sub_list, cmpArtworkByTransportCost)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list


def sortArtworks(artworksInRange):
    sub_list = lt.subList(artworksInRange, 1, lt.size(artworksInRange))
    sub_list = sub_list.copy()
    start_time = time.process_time()
    sorted_list = ms.sort(sub_list, cmpArtworkByDateAcquired)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list

def sortCountries(countries):
    sub_list = lt.subList(countries, 1, lt.size(countries))
    sub_list = sub_list.copy()
    start_time = time.process_time()
    sorted_list = ms.sort(sub_list, cmpCountryByArtworksStored)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    top10sorted = lt.subList(sorted_list, 1, 10)
    return elapsed_time_mseg, top10sorted

def sortArtworksByTechnique(artworksByTech):
    sub_list = lt.subList(artworksByTech, 1, lt.size(artworksByTech))
    sub_list = sub_list.copy()
    start_time = time.process_time()
    sorted_list = ms.sort(sub_list, cmpArtworksByTechnique)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    top10sorted = lt.subList(sorted_list, 1, 10)
    return elapsed_time_mseg, top10sorted


#### funciones comparación mapas ############


def compareMapMedium(id, tag):
    tagentry = me.getKey(tag)
    if (id == tagentry):
        return 0
    elif (id > tagentry):
        return 1
    else:
        return 0
