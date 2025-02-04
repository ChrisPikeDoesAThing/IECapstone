import folium
import numpy as np
import csv

def csv_to_list_of_lists(csv_file):
    """Reads a CSV file and returns its contents as a list of lists."""

    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=",")
        return list(reader)

factories = csv_to_list_of_lists('factories.csv')
counties  = csv_to_list_of_lists('counties.csv')

def plot_points_on_map(factories,counties, map_center, zoom_start=10):
    """
    Plots multiple latitude/longitude points on a map using Folium.
    
    :param points: List of tuples [(lat, lon, 'Label')]
    :param map_center: Tuple (lat, lon) for map center
    :param zoom_start: Initial zoom level
    :return: Folium map object
    """
    # Create a folium map centered at the specified location
    m = folium.Map(location=map_center, zoom_start=zoom_start)
    
    # Add markers for each point

    for i in range(len(factories)):
        folium.Marker([factories[i][1], factories[i][2]], popup=factories[i][0], tooltip=factories[i][0], icon=folium.CustomIcon('factory.png',icon_size=(40,40))).add_to(m)
    for i in range(len(counties)):
        folium.Marker([counties[i][1], counties[i][2]], popup=counties[i][0], tooltip=counties[i][0], icon=folium.CustomIcon('county.png',icon_size=(40,40))).add_to(m)
    return m

# Example usage:


map_center = (28.414289381046988, -81.7597650824977)  # Approximate center of the US
map_object = plot_points_on_map(factories, counties, map_center)


# Save the map to an HTML file and display it
map_object.save("map.html")
print("Map saved as map.html. Open it in a browser to view.")