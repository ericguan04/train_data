# Helper functions for visualizing the ridership data

import folium
import pandas as pd

def top_station_destinations(ridership_df, top_n=5):
    top_destinations = ridership_df.groupby("Destination Station Complex Name").size().reset_index(name='Count').sort_values('Count', ascending=False).head(top_n)
    return top_destinations

def bottom_station_destinations(ridership_df, bottom_n=5):
    top_destinations = ridership_df.groupby("Destination Station Complex Name").size().reset_index(name='Count').sort_values('Count', ascending=True).head(bottom_n)
    return top_destinations

def origin_destination_visualizer(ridership_df, station_df, top_n = 5):

    # Get ridership data for the origin station and group by destination
    grouped_ridership_df = ridership_df.groupby("Destination Station Complex ID")

    # Get origin station information
    origin_station = ridership_df.iloc[0]
    origin_lat = origin_station["Origin Latitude"]
    origin_lon = origin_station["Origin Longitude"]
    origin_name = origin_station["Origin Station Complex Name"]

    # Create a Folium map centered at the origin station
    m = folium.Map(location=[origin_lat, origin_lon], zoom_start=13)

    # Add a marker for the origin station
    folium.Marker(
        location=[origin_lat, origin_lon],
        popup=f"Origin: {origin_name}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

    # Add markers for the top destinations
    for dest_id, count in grouped_ridership_df.size().sort_values(ascending=False).head(top_n).items():
        # Get destination station information
        dest_df = station_df[station_df["Complex ID"] == dest_id]
        dest_lat = dest_df["Latitude"]
        dest_lon = dest_df["Longitude"]
        dest_name = dest_df["Stop Name"]
        
        # Add a marker for the destination station
        folium.Marker(
            location=[dest_lat, dest_lon],
            popup=f"Destination: {dest_name} (Ridership: {count})",
            icon=folium.Icon(color='red')
        ).add_to(m)

    return m

station_df = pd.read_csv("datasets/MTA_Subway_Stations_and_Complexes_20250225.csv")