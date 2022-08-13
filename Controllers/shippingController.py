import googlemaps
from flask import jsonify, request

def calculate():
    if  request.get_json:
        origin = 'Pau dos Ferros/RN'
        distanceJson = request.get_json()
        city = distanceJson['city']
        state = distanceJson['state']
        distance = city+'/'+state
        gmaps = googlemaps.Client(key = 'AIzaSyCkMRNvpwRYW5Bw99COIWmrSrRG88j1DKc')
        geocode_result = gmaps.distance_matrix(origin,distance)
        if geocode_result["status"] == 'OK':
            lista = geocode_result['rows']
            dicio =lista[0]
            elements = dicio["elements"]
            lista = elements[0]
            distance = lista["distance"]
            distanceKM = distance["value"]/1000
            if distanceKM <= 100:
                value = 0
                return jsonify({'value':value})
            else:
                value = (distanceKM/100)*10
                return jsonify({'value':value})
    return 405