import folium
import numpy as np
import csv
import pandas as pd
import os

def join_path(filename):
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    file_path = os.path.join(parent_dir, filename)
    return file_path

def csv_to_list_of_lists(csv_file):
    """Reads a CSV file and returns its contents as a list of lists."""

    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=",")
        return list(reader)

def plot_points_on_map(routefile, factories,counties, map_center, zoom_start=10):
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
        folium.Marker([factories[i][1], factories[i][2]], popup=factories[i][0], tooltip=factories[i][0], icon=folium.CustomIcon(join_path('Model/ASsets/factory.png'),icon_size=(40,40))).add_to(m)
    for i in range(len(counties)):
        folium.Marker([counties[i][1], counties[i][2]], popup=counties[i][0], tooltip=counties[i][0], icon=folium.CustomIcon(join_path('Model/Assets/county.png'),icon_size=(40,40))).add_to(m)
        
    routes = pd.read_csv(routefile, header=1)
    for i in range(routes.shape[0]):
        #coordinates =[[routes.values[i][2],routes.values[i][3]],[routes.values[i][5],routes.values[i][6]]]
        coordinates =[[routes.values[i][1],routes.values[i][2]],[routes.values[i][4],routes.values[i][5]]]
        folium.PolyLine(coordinates, color="blue", weight=2.5, opacity=1).add_to(m)
        
    return m


def create_supply_distribution_with_coordinates(optimal_distribution_path, locations_path, output_path):
    locations_df = pd.read_csv(locations_path)
    locations_dict = locations_df.set_index('ID')[['Lat', 'Lon']].to_dict('index')
    optimal_distribution_df = pd.read_csv(optimal_distribution_path)
    new_rows = []
    for _, row in optimal_distribution_df.iterrows():
        supplier_id = row['SupplierID']
        demander_id = row['DemanderID']
        supply_amount = row['SupplyAmount']
        supplier_coords = locations_dict[supplier_id]
        demander_coords = locations_dict[demander_id]
        new_row = {
            'SupplierID': supplier_id,
            'Supplier Latitude': supplier_coords['Lat'],
            'Supplier Longitude': supplier_coords['Lon'],
            'DemanderID': demander_id,
            'Demander Latitude': demander_coords['Lat'],
            'Demander Longitude': demander_coords['Lon'],
            'Supply Amount / Demand': supply_amount
        }
        
        new_rows.append(new_row)
    new_df = pd.DataFrame(new_rows)
    new_df.to_csv(output_path, index=False)


def Mapping(optimal_distribution_path, output_path):

    # Read the CSV files
    factories = csv_to_list_of_lists(join_path('Model/CSVLib/factories.csv'))
    counties  = csv_to_list_of_lists(join_path('Model/CSVLib/counties.csv'))
    locations_path = join_path('Model/CSVLib/LocationsHeader.csv')

    IntermediateRouteCSV = join_path('Model/CSVCSVWorking/DistributionConnected.csv')
    create_supply_distribution_with_coordinates(join_path(optimal_distribution_path), locations_path, IntermediateRouteCSV)

    map_center = (28.414289381046988, -81.7597650824977)  # Approximate center of the US
    map_object = plot_points_on_map(IntermediateRouteCSV, factories, counties, map_center)

    # Save the map to an HTML file and display it
    map_object.save(join_path(output_path))
