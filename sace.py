import pandas as pd
from geopy.distance import geodesic
import folium

# ----- Step 1: Load CSV -----
data = pd.read_csv(r"C:\Users\grtej\OneDrive\Desktop\Delivery_Route_Optimisation\locations.csv")

# ----- Step 2: Create map centered at average location -----
map_route = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=12)

# ----- Step 3: Simple nearest neighbor route -----
visited = [0]
current = 0

while len(visited) < len(data):
    distances = []
    for i in range(len(data)):
        if i not in visited:
            dist = geodesic(
                (data.loc[current, 'Latitude'], data.loc[current, 'Longitude']),
                (data.loc[i, 'Latitude'], data.loc[i, 'Longitude'])
            ).km
            distances.append((i, dist))
    next_point = min(distances, key=lambda x: x[1])[0]
    folium.PolyLine(
        [(data.loc[current, 'Latitude'], data.loc[current, 'Longitude']),
         (data.loc[next_point, 'Latitude'], data.loc[next_point, 'Longitude'])],
        color='blue', weight=2.5, opacity=1
    ).add_to(map_route)
    current = next_point
    visited.append(current)

# ----- Step 4: Add markers -----
for i in range(len(data)):
    folium.Marker(
        [data.loc[i, 'Latitude'], data.loc[i, 'Longitude']],
        popup=data.loc[i, 'Location']
    ).add_to(map_route)

# ----- Step 5: Save map -----
map_route.save("route_map.html")
print("Route map created: route_map.html")
