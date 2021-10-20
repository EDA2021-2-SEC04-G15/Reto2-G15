"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import time
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


import sys
...
default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\nBienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Listar artistas en un rango de fechas")
    print("3- Listar adquisiciones en un rango de fechas")
    print("4- Mostrar obras de artista según tecnica")
    print("5- Mostrar obras según nacionalidad")
    print("6- Calcular costo de transporte de obras según departamento")
    print("7- Mostrar nueva exposición")
    print("8- MOSTRAR OBRAS MAS ANTIGUAS DE UNA TECNICA")
    print("9- NUMERO DE OBRAS SEGUN NACIONALIDAD")
    print("0- Salir")


def initCatalog():
    """
    Inicializa el catalogo de obras y artistas 
    """
    return controller.initCatalog()

def loadData(catalog):
    """""
    Carga obras en la estructura de datos
    """
    controller.loadData(catalog)


def printArtworksSortResults(ord_artworks):

    cantidad = lt.size(ord_artworks)
    print('\nSe encontraron ' + str(cantidad) + ' obras en el rango ingresado')

    
    print("\nLas primeras 3 obras en el rango son: ")

    i=1
    while i in range(1,4):
        artwork = lt.getElement(ord_artworks,i)
        constituents = artwork["ConstituentID"]
        artistas = controller.searchArtistByID(catalog, constituents)
        cantidad_artistas = lt.size(artistas)
        
        print('\n###########\nTitulo: ' + artwork['Title'] + ' \n\nArtistas: ')

        for num in range(0,cantidad_artistas):
            artista = lt.getElement(artistas, num + 1)
            print(str(artista['DisplayName']))
        
        print('\nFecha: ' + artwork['Date'] +
           ', Fecha adquisición: ' + artwork['DateAcquired'] +
            ', Medio: ' + artwork['Medium'] +
            ' , Dimensiones: ' + artwork['Dimensions'] )
        i+=1
    
    print("\n###############\n\nLas últimas 3 obras en el rango son: ")

    k=2
    while k in range(0,3):
        pos = int(lt.size(ord_artworks))- k
        artwork = lt.getElement(ord_artworks,pos)

        constituents = artwork["ConstituentID"]
        artistas = controller.searchArtistByID(catalog, constituents)
        cantidad_artistas = lt.size(artistas)
        
        print('\n#############\nTitulo: ' + artwork['Title'] + ' \n\nArtistas: ')

        for num in range(0,cantidad_artistas):
            artista = lt.getElement(artistas, num + 1)
            print(str(artista['DisplayName']))
        
        print('\nFecha: ' + artwork['Date'] +
           ', Fecha adquisición: ' + artwork['DateAcquired'] +
            ', Medio: ' + artwork['Medium'] +
            ' , Dimensiones: ' + artwork['Dimensions'] )
        
        k-=1

def printArtistSortResults(ord_artists):

    cantidad = lt.size(ord_artists)
    print('\nSe encontraron ' + str(cantidad) + ' artistsas en el rango ingresado')
    
    print("\nLos primeros 3 artistas en el rango son: ")

    i=1
    while i in range(1,4):
        artist = lt.getElement(ord_artists,i)
        print('\nNombre: ' + artist['DisplayName'] +
         ', Año de nacimiento: ' + artist['BeginDate'] +
          ', Año de fallecimiento: ' + artist['EndDate'] +
           ', Nacionalidad: ' + artist['Nationality'] +
            ', Genero: ' + artist['Gender'] )
        i+=1

    print("\nLos ultimos 3 artistas en el rango son: ")

    k=2
    while k in range(0,3):
        pos = int(lt.size(ord_artists))- k
        artist = lt.getElement(ord_artists, pos)
        print('\nNombre: ' + artist['DisplayName'] +
         ', Año de nacimiento: ' + artist['BeginDate'] +
          ', Año de fallecimiento: ' + artist['EndDate'] +
           ', Nacionalidad: ' + artist['Nationality'] +
            ', Genero: ' + artist['Gender'] )
        k-=1

    
def printCountriesSortResult(ord_countries):

    print("\nLos 10 paises con mas obras en el MoMa son: ")

    for nationality in lt.iterator(ord_countries):
        print("\n" + nationality['name'] + " : " + str(nationality['size']))

    pais = lt.getElement(ord_countries, 1)
    print("las primeras y utlimas 3 obras de la lista de obras nacionalidad: " + pais["name"]+ ", son: ")
    obras = pais['artworks']
    size = pais['size']
    for pos in [1,2,3,size-2,size-1,size]:
        obra = lt.getElement(obras, pos)
        constituents = obra["ConstituentID"]
        artistas = controller.searchArtistByID(catalog, constituents)
        cantidad_artistas = lt.size(artistas)

        print('\n############\nTitulo: ' + obra['Title'] + ' \n\nArtistas: ')

        for num in range(0,cantidad_artistas):
            artista = lt.getElement(artistas, num + 1)
            print(str(artista))
        
        print('\nFecha: ' + obra['Date'] +
           ', Fecha adquisición: ' + obra['DateAcquired'] +
            ', Medio: ' + obra['Medium'] +
            ' , Dimensiones: ' + obra['Dimensions'] )

def printSortedDateResult(sorted_date):
    print("\n Las 5 obras mas antiguas a transportar son: ")

    lista_dates = sorted_date[1]

    i=1
    while i in range(1,6):
        artwork = lt.getElement(lista_dates,i)
        constituents = artwork["ConstituentID"]
        artistas = controller.searchArtistByID(catalog, constituents)
        cantidad_artistas = lt.size(artistas)
        
        print('\n############\nTitulo: ' + artwork['Title'] + ' \n\nArtistas: ')

        for num in range(0,cantidad_artistas):
            artista = lt.getElement(artistas, num + 1)
            print(str(artista))
        
        print('\nFecha: ' + artwork['Date'] +
            ', Medio: ' + artwork['Medium'] +
            ' , Dimensiones: ' + artwork['Dimensions'] +
            ' , Costo de transporte: ' + str((artwork['cost']).__round__(2)))
        i+=1
    
    
def printSortedCostResult(sorted_cost):
    print("\n#########\n\nLas 5 obras mas costosas a transportar son: ")

    lista_cost = sorted_cost[1]

    i=1
    while i in range(1,6):
        artwork = lt.getElement(lista_cost,i)
        constituents = artwork["ConstituentID"]
        artistas = controller.searchArtistByID(catalog, constituents)
        cantidad_artistas = lt.size(artistas)
        
        print('\n############\nTitulo: ' + artwork['Title'] + ' \n\nArtistas: ')

        for num in range(0,cantidad_artistas):
            artista = lt.getElement(artistas, num + 1)
            print(str(artista))
        
        print('\nFecha: ' + artwork['Date'] +
            ', Medio: ' + artwork['Medium'] +
            ' , Dimensiones: ' + artwork['Dimensions'] +
            ' , Costo de transporte: ' + str((artwork['cost']).__round__(2)))
        i+=1

catalog = None

def printArworksByTechniqueResult(ordArtworks):
    print("Las obras que se han realizado con esta tecnica son: ")

    listaObras = ordArtworks[1]
    artwork = lt.getElement(listaObras)
    constituents = artwork["ConstituentID"]
    obras =controller.searchArtistByID(catalog, constituents)
    cantidadArtistas = lt.size(obras)
    for num in range (0,cantidadArtistas):
        obra = lt.getElement(obras, num)
        print(str(obras))


    print (' Medio: ' + artwork['Medium'] +
            ', Dimensiones: ' + artwork['Dimensions'])
    

def printArtworksByMedium(obras, numobras):

    cantidad = lt.size(obras)

    print('\nSe encontraron ' + str(cantidad) + ' obras de la tecnica ingresada')

    
    print("\nLas primeras "+ str(numobras) +" obras en el rango son: ")

    i=1
    while i in range(1,numobras+1):
        artwork = lt.getElement(obras,i)       
        print('\n###########\nTitulo: ' + artwork['Title'])        
        print('\nFecha: ' + artwork['Date'] +
           ', Fecha adquisición: ' + artwork['DateAcquired'] +
            ', Medio: ' + artwork['Medium'] )
        i+=1



"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("\nCargando información de los archivos ....\n")
        start_time = time.process_time()
        catalog = initCatalog()
        loadData(catalog)
        sizeArtist = lt.size(catalog['artists'])
        sizeArtworks = lt.size(catalog['artworks'])

        print('Artistas cargados: ' + str(sizeArtist) + '\n')
    

        print('Obras cargadas: ' + str(sizeArtworks) + '\n')

        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print ("\ntiempo: "+ str(elapsed_time_mseg))

    elif int(inputs[0]) == 2:
        
        fecha1 = int(input('Año inicial de busqueda: '))
        fecha2 = int(input('Año final de busqueda: '))
        size = lt.size(catalog['artists'])

        result = controller.sortArtistsByBeginDate(catalog, fecha1, fecha2)
        print("\nPara la muestra de", size, " artistas, el tiempo (mseg) es: ", str(result[0]))
        printArtistSortResults(result[1])

    elif int(inputs[0]) == 3:

        fecha1 = input('Fecha inicial de busqueda (AAAA-MM-DD): ')
        est_fecha1 = {'DateAcquired':fecha1}
        fecha2 = input('Fecha final de busqueda (AAAA-MM-DD): ')
        est_fecha2 = {'DateAcquired': fecha2}
        size = lt.size(catalog['artworks'])

        result = controller.sortArtworksByBeginDate(catalog, est_fecha1, est_fecha2)
        print("\nPara la muestra de", size, " obras, el tiempo (mseg) es: ", str(result[0][0]))
        print("\nSe encontraron " + str(result[1]) + " obras compradas en el rango")
        printArtworksSortResults(result[0][1])

    elif int(inputs[0]) == 4:
        nombre_artista = input("Nombre del artista: ")
        size = lt.size(catalog['artists'])
        result = controller.sortArtworksByTechnique(catalog)
        print("\nEl total de obras de este artista son: " + str(result[1]))
        print("\nEl total de tecnicas utilizadas han sido: " + str(result[2]))
        print("\nLa tecnica más utilizada ha sido: " + str(result[3]))
        printArworksByTechniqueResult(result[4])


        

    elif int(inputs[0]) == 5:
        
        size = lt.size(catalog['nationalities'])

        result = controller.sortCountries(catalog)
        print("\n Para una muestra de", size, "paises, el tiempo (mseg) es: ", str(result[0]))
        printCountriesSortResult(result[1])

    elif int(inputs[0]) == 6:

        departament = input("Departamento: ")
        result = controller.sortArtworksByDeparment(catalog, departament)
        result_totales = result[0]
        sorted_date = result[1]
        sorted_cost = result[2]
        print("\nSe require transportar " + str(result_totales[1]) +
         " obras provenientes del departamento de " + departament)
        print("Se estima que realizar esto tendra un costo total de: " + str(result_totales[2]) +" USD")
        print("Se estima que el peso total de artefactos es de: " + str(result_totales[3]) + " KG")
        printSortedDateResult(sorted_date)
        printSortedCostResult(sorted_cost)
    
    elif int(inputs[0]) == 7:
        a_inicial = input("Año inicial de las obras: ")
        a_final = input("Año final de las obras: ")
        area = input("Area disponible para nueva exposicón: ")
        print("...")
        pass


    elif int(inputs[0]) == 8:
        medio = input("Tecnica a buscar: ")
        numobras = int(input("NUmero de obras a mostrar: "))
        obras = controller.getArtworksByMedium(catalog, medio)
        printArtworksByMedium(obras[1], numobras)


    elif int(inputs[0]) == 9:
        nacinalidad = input("Nacionalidad a buscar: ")
        resultado = controller.getNumberByNationality(catalog, nacinalidad)
        print("\n numero de obras: " + str(resultado))



    else:
        sys.exit(0)
sys.exit(0)

