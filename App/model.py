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
               'artistID':None,
               'years':None,
               'nationalities': None,
               'tecnicas' : None}

    
    catalog['artists'] = lt.newList('ARRAY_LIST')
    catalog['artworks'] = lt.newList('ARRAY_LIST')


    ### funciones de creación de mapas #####

    """
    Este indice crea un map cuya llave es la tecnica de la obra
    """
    catalog['tecnicas'] = mp.newMap(5000,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareMapMedium)

    catalog['nationalities'] = mp.newMap(5000,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareMapNationality)

    catalog['years'] = mp.newMap(5000,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareMapYears)

    catalog['dates'] = mp.newMap(500000,
                                 maptype='CHAINING',
                                 loadfactor=4.0,
                                 comparefunction=compareMapDatess)

    catalog['artistID'] = mp.newMap(100000,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareMapIDs)

    catalog['departments'] = mp.newMap(500,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareMapDepartments)

    return catalog

# Funciones para agregar informacion al catalogo

def addArtist(catalog, artist):
    # Se adiciona el artista a la lista de artistas
    lt.addLast(catalog['artists'], artist)

    #Se añade el ID del artista al MAPA de ids
    addArtistID(catalog, artist)

    # Se añade la informacion del artista al MAPA de años
    addArtistYears(catalog, artist)
   
def addArtwork(catalog, artwork):
    # Se agrega una obra a la lista de obras
    lt.addLast(catalog['artworks'], artwork)

    # se añade la información de la obra al MAPA de dates

    addArtworkDates(catalog, artwork)

    # se añaden los detalles de la obra al MAPA de nacionalidades
    addArtworkNationlities(catalog, artwork)

    # se añaden los detalles de la obra al MAPA de departamentos

    addArtworkDepartment(catalog, artwork)
    
    # se añade la informacion al mapa de mediums

    addArtworkMedium(catalog, artwork)

def addArtworkDepartment(catalog, artwork):

    try:
        departments = catalog['departments']
        if (artwork['Department'] != ''):
            pubDepartment = (artwork['Department'])
        else:
            pubDepartment = "unknown"
        existDepartment = mp.contains(departments, pubDepartment)
        if existDepartment:
            entry = mp.get(departments, pubDepartment)
            Department = me.getValue(entry)
        else:
            Department = newDepartment(pubDepartment)
            mp.put(departments, pubDepartment, Department)
        lt.addLast(Department['artworks'], artwork)
        Department['total_artworks']+=1
    except Exception:
        return None



def newDepartment(pubDepartment):

    entry = {"department":'', 'artworks':None, 'total_artworks':0}
    entry['department'] = pubDepartment
    entry['artworks'] = lt.newList('ARRAY_LIST')
    return entry

def addArtworkDates(catalog, artwork):

    try:
        dates = catalog['dates']
        if (artwork['DateAcquired'] != ''):
            pubDate = (artwork['DateAcquired'])
        else:
            pubDate = ""
        existDate = mp.contains(dates, pubDate)
        if existDate:
            entry = mp.get(dates, pubDate)
            Date = me.getValue(entry)
        else:
            Date = newDate(pubDate)
            mp.put(dates, pubDate, Date)
        lt.addLast(Date['artworks'], artwork)
        posible = artwork["CreditLine"].lower()
        t = "purchase"
        if t in posible:
           Date['purchased'] += 1
    except Exception:
        return None


def newDate(pubDate):
    entry = {"date":'', 'artworks':None, 'purchased':0}
    entry['date'] = pubDate
    entry['artworks'] = lt.newList('ARRAY_LIST')
    
    return entry


def addArtistID(catalog, artist):

    try:
        IDs = catalog['artistID']
        if (artist['ConstituentID'] != ''):
            pubID = (artist['ConstituentID'])
        else:
            pubID = 'unknown'
        existID = mp.contains(IDs, pubID)
        if existID:
            entry = mp.get(IDs, pubID)
            ID_unico = me.getValue(entry)
        else:
            ID_unico = newID(pubID)
            mp.put(IDs, pubID, ID_unico)
        lt.addLast(ID_unico['artists'], artist)
    except Exception:
        return None

def newID(pubID):
    entry = {"id":'', 'artists':None}
    entry['id'] = pubID
    entry['artists'] = lt.newList('ARRAY_LIST')
    return entry


def addArtistYears(catalog, artist):

    try:
        years = catalog['years']
        if (artist['BeginDate'] != ''):
            pubyear = int((artist['BeginDate']))
        else:
            pubyear = 0
        existyear = mp.contains(years, pubyear)
        if existyear:
            entry = mp.get(years, pubyear)
            year = me.getValue(entry)
        else:
            year = newYear(pubyear)
            mp.put(years, pubyear, year)
        lt.addLast(year['artists'], artist)
    except Exception:
        return None


def newYear(pubyear):
    entry = {'year': "", 'artists':None}
    entry['year'] = pubyear
    entry['artists'] = lt.newList('ARRAY_LIST')
    return entry

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
    try:
        nationalities = catalog['nationalities']
        if (artist['Nationality'] != ''):
            pubnationality = (artist['Nationality'])
        else:
            pubnationality = 'Nationality unknown'
        existnationality = mp.contains(nationalities, pubnationality)
        if existnationality:
            entry = mp.get(nationalities, pubnationality)
            nationality = me.getValue(entry)
        else:
            nationality = newNationlity(pubnationality)
            mp.put(nationalities, pubnationality, nationality)
        lt.addLast(nationality['artworks'], artwork)
        nationality['artwork_number']+=1
    except Exception:
        return None


def newNationlity(pubnationality):
    """
    Crea una nueva estructura para almacenar las obras de una nacionalidad
    """
    entry ={'nationality':'', 'artworks':None, 'artwork_number':0}
    entry['nationality'] = pubnationality
    entry['artworks'] = lt.newList('ARRAY_LIST')
    return entry


# Funciones de consulta


def getArtworksByMedium(catalog, medium):
    """
    Retorna los libros publicados en un año
    """
    medium = mp.get(catalog['tecnicas'], medium)
    if medium:
        return me.getValue(medium)['artworks']
    return None

def getArtworksByNationality(catalog):

    nationalities_map = catalog['nationalities']
    nationalities_keys = mp.keySet(nationalities_map)
    nationalities_list= lt.newList(datastructure= "ARRAY_LIST")

    for nationality in lt.iterator(nationalities_keys):
        entry = mp.get(nationalities_map, nationality)
        posNationality = me.getValue(entry)
        if posNationality != None:
            lt.addLast(nationalities_list, posNationality)
    
    result = sortCountries(nationalities_list)
    return result



def getArtistsInDateRange (catalog, year1, year2):
    """"
    Retorna lista desordenada de artistas en un rango de años
    """
    years_map = catalog['years']
    years_keys = mp.keySet(years_map)

    artistsInRange= lt.newList(datastructure= "ARRAY_LIST")

    for year in lt.iterator(years_keys):
        entry = mp.get(years_map, year)
        posyear = me.getValue(entry)
        if posyear != None:
            if int(posyear["year"]) >= year1 and int(posyear["year"]) <= year2:
                artistInYear = posyear['artists']
                for artist in lt.iterator(artistInYear):
                    lt.addLast(artistsInRange, artist)

    return artistsInRange

def getArtworksInDeparment(catalog, department):
    """
    Retorna lista desordenada de artworks en un departamento en específico
    Agrega el costo de transporte a una nueva categoria dentro del artwork
    Retorna costo total, numero de obras, y peso estimado
    """

    departments_map = catalog['departments']
    existDepartment = mp.contains(departments_map, department)
    if existDepartment:
        entry = mp.get(departments_map, department)
        posDepartment = me.getValue(entry)
    artworksInDept = posDepartment['artworks']
    costo_total = 0
    peso_total = 0
    obras = posDepartment['total_artworks']
    for artwork in lt.iterator(artworksInDept):
        artwork['cost'] = getTansportCost(artwork)
        costo = artwork['cost']
        costo_total += costo
        try:
            peso = float(artwork['Weight (kg)'])
        except:
            peso = 0
        peso_total+= peso

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

def getArtworksInDateRange (catalog, date1, date2):
    """"
    Retorna lista desordenada de artworks en un rango de fechas utilizando el comparador cmpArtwork
    """

    dates_map = catalog['dates']
    dates_keys = mp.keySet(dates_map)
    purchasedAmount = 0
    artworksInRange= lt.newList(datastructure= "ARRAY_LIST")

    for date in lt.iterator(dates_keys):
        entry = mp.get(dates_map, date)
        posDate = me.getValue(entry)
        if posDate != None:
            if (cmpArtworkByDateAcquired(posDate['date'],date2)) and not (cmpArtworkByDateAcquired(posDate['date'], date1)):
                purchasedAmount += posDate['purchased']
                artistsInDate = posDate['artworks']
                for artwork in lt.iterator(artistsInDate):
                    lt.addLast(artworksInRange, artwork)

    return artworksInRange, purchasedAmount



def ArtistByID_v2(catalog, constituentids):

    ID_catalog = catalog['artistID']
    ID_list = constituentids.strip("[]").split(", ")
    result = lt.newList('ARRAY_LIST')

    for item in ID_list:
        existsID = mp.contains(ID_catalog, item)
        if existsID:
            entry = mp.get(ID_catalog, item)
            info_artistas = me.getValue(entry)
            lista_artistas = info_artistas['artists']

            for artist in lt.iterator(lista_artistas):
                lt.addLast(result, artist)
    
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

    result = country1['artwork_number'] > country2['artwork_number']
    return result

def cmpArtistsByBeginDate (artist1, artist2):

    result = int(artist1["BeginDate"]) < int(artist2["BeginDate"])
    return result

def cmpArtworkByDateAcquired(artwork1 , artwork2):

                ### Devuelve True si el 'DateAcquired' de 
                # artwork1 es menor que el de artwork2
    try:
        date1 = artwork1['DateAcquired'].split('-')
    except:
        date1 = artwork1.split('-')

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

def compareMapNationality(id, tag):
    tagentry = me.getKey(tag)
    if (id == tagentry):
        return 0
    elif (id > tagentry):
        return 1
    else:
        return 0

def compareMapYears(id, tag):
    tagentry = me.getKey(tag)
    if (int(id) == int(tagentry)):
        return 0
    elif (int(id) > int(tagentry)):
        return 1
    else:
        return 0

def compareMapIDs(id, tag):
    tagentry = me.getKey(tag)
    if (id == tagentry):
        return 0
    elif (id > tagentry):
        return 1
    else:
        return 0

def compareMapDatess(id, tag):
    tagentry = me.getKey(tag)
    if (id == tagentry):
        return 0
    elif (id > tagentry):
        return 1
    else:
        return 0

def compareMapDepartments(id, tag):
    tagentry = me.getKey(tag)
    if (id == tagentry):
        return 0
    elif (id > tagentry):
        return 1
    else:
        return 0