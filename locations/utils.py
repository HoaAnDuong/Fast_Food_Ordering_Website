import math

def distance(location_1,location_2):
    degree = ((location_1.lat-location_2.lat)**2 + (location_1.lng-location_2.lng)**2)**0.5
    return round(degree*111.319,3)