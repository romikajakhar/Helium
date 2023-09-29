import math
import folium
from folium.vector_layers import CircleMarker

# Create a map object
# map_center = [35.85651547972094, -78.84492274671803]
# m = folium.Map(location=map_center, zoom_start=13)

import math

def calculate_distance(lat2, lon2):
    """
    Calculate the distance between two points on the Earth's surface using the haversine formula.

    Arguments:
    lat1 -- latitude of the first point in degrees
    lon1 -- longitude of the first point in degrees
    lat2 -- latitude of the second point in degrees
    lon2 -- longitude of the second point in degrees
    radius -- radius of the Earth in kilometers (default: 6371)

    Returns:
    Distance between the two points in kilometers.
    """
    lat1 = 35.85651547972094
    lon1 = -78.84492274671803
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    R = 6371  # Radius of the earth in km
    # Calculate the differences in latitude and longitude
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    # Calculate the square of half the chord length
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2

    # Calculate the angular distance in radians
    angular_distance = 2 * math.asin(math.sqrt(a))

    # Calculate the distance in kilometers
    distance = R * angular_distance

    return distance


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


def Suburbspathloss(distance,f,ht,hr):
    ahrs= (1.1 * math.log(f,10)-0.7) * hr - 1.56 * (math.log(f,10)) - 0.8
    C = -4 * math.log(f/28,10) - 5.4
    L=69.55 +26.16*math.log(f,10) - 13.82*math.log(ht,10) -ahrs + C + (44.9 -6.55*math.log(ht,10))*math.log(distance,10)
    return L

def SuburbsdistanceFrom_loss(L, f,ht,hr):
    ahrs= (1.1 * math.log(f,10)-0.7) * hr - 1.56 * (math.log(f,10)) - 0.8
    C = -4 * math.log(f/28) - 5.4
    distance = 10 ** ((L - 69.55 - 26.16 * math.log(f, 10) + 13.82 * math.log(ht, 10) + ahrs - C) / (44.9 - 6.55 * math.log(ht, 10)))
    return distance

def km_pixel(r,zoom_level):
    zoom = zoom_level
    tile_size = 256  # Tile size in pixels
    pixels_per_meter = tile_size * (2 ** zoom) / 40075016.686  # Earth's circumference in meters
    distance_pixels = r * 1000 * pixels_per_meter
    return distance_pixels
# Sensor location
sensor_location = [35.85651547972094, -78.84492274671803]

# Create the map centered on the sensor location
#map_center = sensor_location
m = folium.Map(location=sensor_location, zoom_start=15)
zoom_level = 15
Freq = 903.9
txs=10
txj=22
sensitivity= 135
# Add a marker for the sensor location
popup_text = f"Name: Sensor"
folium.Marker(location=sensor_location, icon=folium.Icon(color='green'), popup="Sensor").add_to(m)
radius=SuburbsdistanceFrom_loss(sensitivity+txs, Freq,8,8)
print(radius)
r_pixel = km_pixel(radius, zoom_level)
print(r_pixel)
C_S = CircleMarker(location=sensor_location, radius=r_pixel, color='green', fill=True, fill_color='green')
C_S.add_to(m)

hotspots = {
    'funny-jetblack-finch': [35.85245903, -78.84599908],
#    'creamy-banana-beetle': [35.85147905, -78.85200282],
    'huge-pastel-bee': [35.85385978, -78.84694557],
#    'dancing-brown-chinchilla': [35.85151532, -78.85220589],
#    'trendy-grey-worm': [35.83589399, -78.85130916],
#    "Brilliant-Macaroon-Mantis": [35.86569832,-78.85345804]
}
# jammer_location=[35.85736,-78.84516]
# popup_text = f"Name: Jammer D"
# folium.Marker(location=jammer_location, icon=folium.Icon(color='red'), popup="Jammer").add_to(m)
#
# jammer1=[35.85686,-78.84849]
# popup_text = f"Name: Jammer A"
# folium.Marker(location=jammer1, icon=folium.Icon(color='red'), popup="Jammer").add_to(m)
#
# jammer2=[35.85701,-78.84872]
# popup_text = f"Name: Jammer B"
# folium.Marker(location=jammer2, icon=folium.Icon(color='red'), popup="Jammer").add_to(m)
#
# jammer3=[35.85497,-78.84573]
# popup_text = f"Name: Jammer C"
# folium.Marker(location=jammer3, icon=folium.Icon(color='red'), popup="Jammer").add_to(m)

for key in hotspots:
    lat = hotspots[key][0]
    lon = hotspots[key][1]
    d = calculate_distance(lat, lon)
    L_sh = Suburbspathloss(d, Freq,8,8)

    L_jh= - txs + txj + L_sh + 3   # Tx(s)=15 Tx(j)=21
    d_jh=SuburbsdistanceFrom_loss(L_jh, Freq,2,8)
    djh_pixel = km_pixel(d_jh,zoom_level)
    print(L_sh)
    hotspots[key].append(d)
    hotspots[key].append(L_sh)

    popup_text = f"Name: {key}\nDistance: {d:.2f} km\nLoss: {L_sh:.2f} dB"
    folium.Marker(location=[lat, lon], popup=popup_text).add_to(m)
    circle = CircleMarker(location=[lat, lon], radius=djh_pixel, color='red', fill=True, fill_color='red')
    circle.add_to(m)

#print(hotspots)

m.save("plot_suburbs.html")

