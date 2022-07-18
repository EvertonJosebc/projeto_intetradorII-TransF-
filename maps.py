import googlemaps
from flask import jsonify
gmaps = googlemaps.Client(key = 'AIzaSyCkMRNvpwRYW5Bw99COIWmrSrRG88j1DKc')
geocode_result = gmaps.distance_matrix('Encanto','Pau dos Ferros')

print(geocode_result['status'])

#lista = geocode_result['rows']
#dicio =lista[0]
#elements = dicio["elements"]
#lista = elements[0]
#print(lista["distance"])
#distancia = lista["distance"]
#print(distancia["value"])
