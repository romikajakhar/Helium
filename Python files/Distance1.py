import math
import folium

# Create a map object
# map_center = [35.85651547972094, -78.84492274671803]
# m = folium.Map(location=map_center, zoom_start=13)

def distance(lat, lon):
    R = 6371 # Radius of the earth in km
    lat_sensor=35.85651547972094
    long_sensor=-78.84492274671803
    dLat = math.radians(lat-lat_sensor)
    dLon = math.radians(lon-long_sensor)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat_sensor)) \
        * math.cos(math.radians(lat)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c # Distance in km
    return d

def pathloss(distance,f):
    ht=2
    hr=8
    ahr= 3.2*(2* math.log(11.75*hr,10)-4.97)
    L = 69.55 +26.16 * math.log(f,10) - 13.82 * math.log(ht,10) - ahr + (44.9 - 6.55 * math.log(ht,10)) * math.log(distance,10)
    return L

# Sensor location
sensor_location = [35.85651547972094, -78.84492274671803]

# Create the map centered on the sensor location
map_center = sensor_location
m = folium.Map(location=map_center, zoom_start=13)

# Add a marker for the sensor location
popup_text = f"Name: Sensor"
folium.Marker(location=sensor_location, icon=folium.Icon(color='red'), popup="Sensor").add_to(m)

hotspots = {
    'funny-jetblack-finch': [35.85245903, -78.84599908],
    'creamy-banana-beetle': [35.85147905, -78.85200282],
    'huge-pastel-bee': [35.85385978, -78.84694557],
    'dancing-brown-chinchilla': [35.85151532, -78.85220589],
    'trendy-grey-worm': [35.83589399, -78.85130916],
    "Brilliant-Macaroon-Mantis": [35.86569832,-78.85345804],
}

radius = {
    "left-rad": [35.85651547972094, -78.84503],
    "right-rad": [35.85651547972094, -78.844813],
    "top-rad": [35.85660347972094, -78.84492274671803],
    "bottom-rad": [35.85642847972094, -78.84492274671803],
}


def distanceR(rad1, rad2, lat, lon):
    R = 6371 # Radius of the earth in km
    lat_sensor=rad1
    long_sensor=rad2
    dLat = math.radians(lat-lat_sensor)
    dLon = math.radians(lon-long_sensor)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat_sensor)) \
        * math.cos(math.radians(lat)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c # Distance in km
    return d

for key in hotspots:
    lat = hotspots[key][0]
    lon = hotspots[key][1]
    d = distance(lat, lon)
    loss = pathloss(d, 903.9)
    hotspots[key].append(d)
    hotspots[key].append(loss)
    popup_text = f"Name: {key}\nDistance: {d:.2f} km\nLoss: {loss:.2f} dB"
    folium.Marker(location=[lat, lon], popup=popup_text).add_to(m)
    
for key in radius:
    for hotspot in hotspots:
        lat1 = radius[key][0]
        lon1 = radius[key][1]
        lat2 = hotspots[hotspot][0]
        lon2 = hotspots[hotspot][1]
        d = distanceR(lat1, lon1, lat2, lon2)
        loss = pathloss(d, 903.9)
        print(f"{key} to {hotspot}: {d:.2f} km, {loss:.2f} dB. Difference: {(hotspots[hotspot][3]-loss):.2f} dB")
    lat = radius[key][0]
    lon = radius[key][1]
    d = distance(lat, lon)
    loss = pathloss(d, 903.9)
    radius[key].append(d)
    radius[key].append(loss)
    popup_text = f"Name: {key}\nDistance: {d:.2f} km\nLoss: {loss:.2f} dB"
    folium.Marker(location=[lat, lon], popup=popup_text).add_to(m)
    

#print(hotspots)
folium.Circle(location=sensor_location, radius=.01*1000, color='crimson', fill=False).add_to(m)

m.save("hotspots_map2.html")

