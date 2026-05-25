import os
import pandas as pd
import osmnx as ox
import networkx as nx
import folium

import pickle

STATS_CSV = "data/statistiques_trajets.csv"
COORDS_CSV = "data/bixi_stations.csv"
MAP_FILE = "data/montreal_bike.graphml"
PLACE = "Montreal, Canada"
CACHE_FILE = "data/route_cache.pkl"



def get_graph():
    if os.path.exists(MAP_FILE):
        print(f"Chargement de la carte locale...")
        return ox.load_graphml(MAP_FILE)
    else:
        print(f"Téléchargement de la carte (Montreal)...")
        G = ox.graph_from_place(PLACE, network_type="bike")
        ox.save_graphml(G, filepath=MAP_FILE)
        return G

def main():
    try:
        df_stats = pd.read_csv(STATS_CSV)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {STATS_CSV} est introuvable.")
        return
    
    try:
        stations_df = pd.read_csv(COORDS_CSV)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {COORDS_CSV} est introuvable.")
        return

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "rb") as f:
            route_cache = pickle.load(f)
        print(f"Loaded {len(route_cache)} cached routes")
    else:
        route_cache = {}


    station_to_lat = dict(zip(stations_df["name"], stations_df["lat"]))
    station_to_lon = dict(zip(stations_df["name"], stations_df["lon"]))

    G = get_graph()
    for u, v, k, data in G.edges(data=True, keys=True):
        data['bike_weight'] = data['length']
        # Si ce n'est pas une infrastructure cyclable connue
        if not any(key in data for key in ['cycleway', 'bicycle', 'amenity']):
            data['bike_weight'] *= 5 # On pénalise fortement les routes standards

    m = folium.Map(location=[45.5088, -73.5878], zoom_start=13, tiles="cartodbpositron")

    print(f"Calcul des trajets pour {len(df_stats)} lignes...")

    heat_data = []
    for index, row in df_stats.iterrows():
        try:
            key = (row["depart"], row["arrivee"])
            if key in route_cache:
                route_coords = route_cache[key]
            #     heat_data.append([dep_lat, dep_lon, row["nb"]])
            #     heat_data.append([arr_lat, arr_lon, row["nb"]])
            else : 
                dep_lat = station_to_lat.get(row["depart"],0)
                dep_lon = station_to_lon.get(row["depart"],0)

                arr_lat = station_to_lat.get(row["arrivee"],0)
                arr_lon = station_to_lon.get(row["arrivee"],0)

                # heat_data.append([dep_lat, dep_lon, row["nb"]])
                # heat_data.append([arr_lat, arr_lon, row["nb"]])

                dep = (dep_lat,dep_lon)
                arr = (arr_lat, arr_lon)

                # ox.nearest_nodes  (G, X=longitude, Y=latitude)
                orig_node = ox.nearest_nodes(G, dep[1], dep[0])
                dest_node = ox.nearest_nodes(G, arr[1], arr[0])

                route = nx.shortest_path(G, orig_node, dest_node, weight="length")
                
                route_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in route]

                route_cache[key] = route_coords
                
            folium.PolyLine(route_coords, 
                            weight=row['nb']*3,
                            color="blue",
                            opacity=0.5
                            ).add_to(m)

        except Exception as e:
            print(f"Erreur à la ligne {index}: {e}")
            continue

    #HeatMap(heat_data, radius=15, blur=10, max_zoom=13).add_to(m)       
    # 5. Sauvegarde
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(route_cache, f)
        print(f"Saved {len(route_cache)} cached routes")

    m.save("data/resultat_bixi_csv.html")
    print("Visualisation générée dans : resultat_bixi_csv.html")

if __name__ == "__main__":
    main()