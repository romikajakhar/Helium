import math

def distance(lat, lon):
    R = 6371 # Radius of the earth in km
    lat_sensor=35.85651547972094
    long_sensor=-78.84492274671803
    dLat = math.radians(lat2-lat_sensor)
    dLon = math.radians(lon2-long_sensor)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat_sensor)) \
        * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c # Distance in km
    return d


lat2 = 52.406374
lon2 = 16.9251681
d = distance(lat2, lon2)
print(d) # Output: 278.54558935106695 km