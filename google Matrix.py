import googlemaps
from datetime import datetime

def distance(origin,destination):
    gmaps = googlemaps.Client(key='AIzaSyB3sE6Ekts-GoPlZ8vJ8P8i0UL1rVFnnPI')

    my_dis = gmaps.distance_matrix(origin,destination)
    rows = my_dis['rows']
    row = rows[0]
    elements = row['elements']
    element = elements[0]
    distances = element['distance']
    distance = distances['text']
    return (distance)

print (distance('amersfoort', 'utrecht'))
