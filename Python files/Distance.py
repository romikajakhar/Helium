import math
import folium
from folium.vector_layers import CircleMarker

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
    L=69.55 + 26.16*math.log(f,10) - 13.82*math.log(ht,10) -ahr +(44.9 -6.55*math.log(ht,10))*math.log(distance,10)
    Lsu= L- 2*(math.log(f/28,10)**2) - 5.4
    return L

def radius_6DBloss(L, f):
    ht = 2
    hr = 5
    ahr = 0.8 + (1.1 * math.log(f, 10) - 0.7)*hr - 1.56*math.log(f, 10)
    distance = 10 ** ((L - 69.55 - 26.16 * math.log(f, 10) + 13.82 * math.log(ht, 10) + ahr) / (44.9 - 6.55 * math.log(ht, 10)))
    return distance

def km_pixel(r,zoom_level):
    zoom = zoom_level
    tile_size = 256  # Tile size in pixels
    pixels_per_meter = tile_size * (2 ** zoom) / 40075016.686  # Earth's circumference in meters
    distance_pixels = r * 1000 * pixels_per_meter
    return distance_pixels
# Sensor location
sensor_location = [35.85651547972094, -78.84492274671803]
sensor_power = 10
sensitivity = 132 #SPF 10
# Create the map centered on the sensor location
map_center = sensor_location
m = folium.Map(location=map_center, zoom_start=15)

# Add a marker for the sensor location
R_Sensor=radius_6DBloss(142,903.9)
R_3db=radius_6DBloss(3,903.9)
R_pixel=km_pixel(R_Sensor,15)
R6db_pxel=km_pixel(R_3db,15)
popup_text = f"Name: Sensor"
folium.Marker(location=sensor_location, icon=folium.Icon(color='green'), popup="Sensor").add_to(m)
circle = CircleMarker(location=sensor_location, radius=R_pixel, color='green', fill=True, fill_color='green')
circle.add_to(m)

hotspots = {
    'funny-jetblack-finch': [35.85245903, -78.84599908],
    'creamy-banana-beetle': [35.85147905, -78.85200282],
    'huge-pastel-bee': [35.85385978, -78.84694557],
    'dancing-brown-chinchilla': [35.85151532, -78.85220589],
    'trendy-grey-worm': [35.83589399, -78.85130916],
  #  "Brilliant-Macaroon-Mantis": [35.86569832,-78.85345804]
}
jammer_location=[35.85475,-78.84557]
popup_text = f"Name: Jammer"
folium.Marker(location=jammer_location, icon=folium.Icon(color='red'), popup="Jammer").add_to(m)

for key in hotspots:
    lat = hotspots[key][0]
    lon = hotspots[key][1]
    RH = radius_6DBloss(147, 903.9)
    R = RH - R_3db

    d = distance(lat, lon)
    loss = pathloss(d, 903.9)
#    R=radius_6DBloss(loss-6, 903.9)

    hotspots[key].append(d)
    hotspots[key].append(loss)
    zoom_level = 15
    RH_pixel = km_pixel(R,zoom_level)
    popup_text = f"Name: {key}\nDistance: {d:.2f} km\nLoss: {loss:.2f} dB"
    folium.Marker(location=[lat, lon], popup=popup_text).add_to(m)
    c1 = CircleMarker(location=[lat, lon], radius=RH_pixel, color='blue', fill=True, fill_color='blue')
    c1.add_to(m)


#print(hotspots)

m.save("intersection_plot2.html")

