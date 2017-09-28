import googlemaps


def distance(origin, destination):
    google_maps = googlemaps.Client(key='AIzaSyB3sE6Ekts-GoPlZ8vJ8P8i0UL1rVFnnPI')

    delta = google_maps.distance_matrix(origin, destination)['rows'][0]['elements'][0]['distance']['text']
    return delta


print(distance('amersfoort', 'utrecht'))
