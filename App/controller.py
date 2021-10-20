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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de obras y artistas

def initCatalog():
    """""
    Llama la función de inicialización del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog


# Funciones para la carga de datos

def loadData(catalog):
    """""
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadArtists(catalog)
    loadArtworks(catalog)


def loadArtists(catalog):
    """
    Carga los artistas del archivo.
    """
    artistsfile = cf.data_dir + 'Artists-utf8-small.csv'
    input_file = csv.DictReader(open(artistsfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)


def loadArtworks(catalog):
    """
    Carga las obras del archivo.
    """
    artworksfile = cf.data_dir + 'Artworks-utf8-small.csv'
    input_file = csv.DictReader(open(artworksfile, encoding='utf-8'))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)


# Funciones de ordenamiento

def sortArtistsByBeginDate(catalog, year1, year2):
    
    artistsInRange = model.getArtistsInDateRange(catalog, year1, year2)
    sortedResult = model.sortArtists(artistsInRange)
    return sortedResult

def sortArtworksByBeginDate(catalog, year1, year2):
    
    artworksInRange = model.getArtworksInDateRange(catalog, year1, year2)
    purchasedAmount = model.purchasedAmount(artworksInRange)
    sortedResult = model.sortArtworks(artworksInRange)
    return sortedResult,purchasedAmount
    

def sortCountries(catalog):

    countries = catalog['nationalities']
    sortedResult = model.sortCountries(countries)
    return sortedResult

def sortArtworksByDeparment(catalog, department):

    artowrksInDeptResult = model.getArtworksInDeparment(catalog, department)
    artworksInDept = artowrksInDeptResult[0]
    sortedResultByDate = model.sortArtworksInDeptByDate(artworksInDept)
    sortedResultByTransportCost = model.sortArtworksInDeptByTransportCost(artworksInDept)
    return artowrksInDeptResult, sortedResultByDate, sortedResultByTransportCost

def sortArtworksByTechnique(catalog, technique):
    artworksByTechResult = model.getArtworksByTechnique


# Funciones de consulta sobre el catálogo

def searchArtistByID(catalog, constituentids):
    return model.searchArtistByID(catalog, constituentids)

def getArtworksByMedium(catalog, medio):

    artworksByMedium = model.getArtworksByMedium(catalog, medio)
    sortedResult = model.sortArtworks(artworksByMedium)
    return sortedResult

def getNumberByNationality(catalog, nacinalidad):

    result = model.getArtworksByNationality(catalog, nacinalidad)
    return result
    

