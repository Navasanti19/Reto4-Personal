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
 Siuu
 """


from csv import list_dialects
import config as cf
import time
import networkx as nx
import graphviz
import matplotlib.pyplot as plt
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mer
from DISClib.Utils import error as error
from math import radians, cos, sin, asin, sqrt
assert cf


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos



def newCatalog():

    
    try:
        

        catalog = {
            'stops': None,
            'connections': None,
            'components': None,
            'paths': None,
            'search': None,
            'G':None
            
        }
        catalog['G'] = nx.Graph()
        catalog['vertices']=lt.newList('ARRAY_LIST',None)
        catalog['transbordo']=lt.newList('ARRAY_LIST',None)
        catalog['arcos']=lt.newList('ARRAY_LIST',None)

        catalog['stops'] = mp.newMap(numelements=140,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        catalog['grafo'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo

def addVertice(analyzer, vertice):
    lt.addLast(analyzer["vertices"], vertice)

    mp.put(analyzer['stops'],formatVertex(vertice),vertice)
    if vertice['Transbordo']=='S':
        lt.addLast(analyzer['transbordo'],vertice)

    
    addStop(analyzer, formatVertex(vertice))
    return analyzer

def addArco(analyzer, arco):
    lt.addLast(analyzer["arcos"], arco)
    stop1=arco['Code']+'-'+arco['Bus_Stop'][4:]
    stop2=arco['Code_Destiny']+'-'+arco['Bus_Stop'][4:]

    mapa=analyzer['stops']

    vertex1=mp.get(mapa,stop1)
    vertex1=me.getValue(vertex1)
    vertex1=[float(vertex1['Longitude']),float(vertex1['Latitude'])]
        
    vertex2=mp.get(mapa,stop2)
    vertex2=me.getValue(vertex2)
    vertex2=[float(vertex2['Longitude']),float(vertex2['Latitude'])]
    dist=haversine(vertex1[0],vertex1[1],vertex2[0],vertex2[1])
    addConnection(analyzer,stop1,stop2,dist)
    return analyzer

def addTransbordo(analyzer):
    for i in lt.iterator(analyzer['transbordo']):
        vertex='T-'+i['Code']
        vertex2=formatVertex(i)
        if gr.containsVertex(analyzer['grafo'],vertex):
            addConnection(analyzer,vertex,vertex2,0)
        else:
            addStop(analyzer,vertex)
            addConnection(analyzer,vertex,vertex2,0)
    
    #nx.draw_networkx(analyzer['G'])
    #plt.show()
    return analyzer['G']

def addStop(analyzer, stopid):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['grafo'], stopid):
            #analyzer['G'].add_node(stopid)
            gr.insertVertex(analyzer['grafo'], stopid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')

def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['grafo'], origin, destination)
    if edge is None:
        #analyzer['G'].add_edge(origin, destination)
        gr.addEdge(analyzer['grafo'], origin, destination, distance)
    return analyzer



# Funciones de consulta

def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['grafo'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['grafo'])


def getReq1():
    pass

def getReq2 ():
    pass

def getReq3():
    pass

def getReq4():
    pass

def getReq5():
    pass

def getReq6():
    pass

def getReq7():
    pass

def getReq8():
    pass
    

# Funciones de comparación

def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

#Funciones de Tiempo

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)

def deltaTime(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

# Funciones de Ayuda

def formatVertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['Code'] + '-'
    name = name + service['Bus_Stop'][6:]
    return name

def formatArco(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['Code'] + '-'
    name = name + service['Bus_Stop'][4:]
    return name

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r