# Helper functions for visualizing the ridership data

import folium
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to get the top station origins
def top_station_destinations(ridership_df, top_n=5):
    top_destinations = ridership_df.groupby("Destination Station Complex Name")["Estimated Average Ridership"].sum().sort_values(ascending=False).head(top_n)
    return top_destinations


# Function to get the bottom station destinations
def bottom_station_destinations(ridership_df, bottom_n=5):
    top_destinations = ridership_df.groupby("Destination Station Complex Name")["Estimated Average Ridership"].sum().sort_values(ascending=True).head(bottom_n)
    return top_destinations


# Function to visualize the top destinations for a given station
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
    for dest_id, count in grouped_ridership_df["Estimated Average Ridership"].sum().sort_values(ascending=False).head(top_n).items():
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



# Function to plot a histogram of ridership for a given month
def plot_weekday_histogram(df, year, month):
    df_filtered = df[(df["Year"] == year) & (df["Month"] == month) & (df["DayOfWeek"] != "Total")]

    # Set plot style
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_filtered, x="DayOfWeek", y="Ridership", order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], palette="Blues")

    # Labels and title
    plt.xlabel("Day of the Week")
    plt.ylabel("Ridership")
    plt.title(f"Ridership Histogram for January {year}")
    plt.xticks(rotation=45)

    # Show plot
    plt.show()



# Function to calculate average ridership for a station and return a DataFrame
def average_ridership_df(station_id, dataset):
    data = []  # List to store dictionary records
    
    average_ridership = dataset[dataset["Destination Station Complex ID"] == station_id]
    
    for year in [2021, 2022, 2023, 2024]:
        yearly_ridership = 0

        for month in range(1, 13):
            monthly_ridership = 0

            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                amount = average_ridership[
                    (average_ridership["Year"] == year) & 
                    (average_ridership["Month"] == month) & 
                    (average_ridership["Day of Week"] == day)
                ]["Estimated Average Ridership"].sum()
                
                adjusted_amount = amount * 4  # Adjusted for 4 weeks per month
                
                # Append data in structured format
                data.append({
                    "Year": year,
                    "Month": month,
                    "DayOfWeek": day,
                    "Ridership": adjusted_amount
                })

                monthly_ridership += adjusted_amount

            # Append monthly total
            data.append({
                "Year": year,
                "Month": month,
                "DayOfWeek": "Total",
                "Ridership": monthly_ridership
            })

            yearly_ridership += monthly_ridership

        # Append yearly total
        data.append({
            "Year": year,
            "Month": "Total",
            "DayOfWeek": "Total",
            "Ridership": yearly_ridership
        })
    
    # Convert list of records into a DataFrame
    df = pd.DataFrame(data)
    return df



# Function to write average ridership information to a file
def average_ridership_info(station_id, dataset, output_file):
    with open(output_file, "w") as file:
        average_ridership = dataset[(dataset["Destination Station Complex ID"] == station_id)]

        total_ridership_four_years = 0
        for year in [2021, 2022, 2023, 2024]:
            file.write(f"Year: {year}\n")
            yearly_ridership = 0
            
            for month in range(1, 13):
                file.write(f"Month: {month}\n")
                monthly_ridership = 0
                
                for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                    amount = average_ridership[(average_ridership["Year"] == year) & 
                                               (average_ridership["Month"] == month) & 
                                               (average_ridership["Day of Week"] == day)]["Estimated Average Ridership"].sum()
                    file.write(f"{day}: {amount * 4}\n")
                    monthly_ridership += amount * 4

                file.write(f"All Ridership in Month: {monthly_ridership}\n\n")
                yearly_ridership += monthly_ridership

            file.write(f"All Ridership in Year: {yearly_ridership}\n\n")
            total_ridership_four_years += yearly_ridership

        file.write(f"All Ridership in Four Years: {total_ridership_four_years}\n")



# Function to plot the ridership histogram
def plot_yearly_ridership(df):
    """Plots the yearly ridership histogram."""
    df_filtered = df[df["DayOfWeek"] != "Total"]
    df_filtered["Ridership"] = pd.to_numeric(df_filtered["Ridership"])
    
    yearly_ridership = df_filtered.groupby("Year")["Ridership"].sum()

    plt.figure(figsize=(10, 5))
    plt.bar(yearly_ridership.index, yearly_ridership.values, color="blue", alpha=0.7)
    plt.xlabel("Year")
    plt.ylabel("Total Ridership")
    plt.title("Yearly Ridership")
    plt.xticks(yearly_ridership.index)
    plt.show()



# Function to plot the monthly ridership histogram
def plot_monthly_ridership(df):
    """Plots the monthly ridership histogram."""
    df_filtered = df[df["DayOfWeek"] != "Total"]  # Remove "Total" rows
    df_filtered["Ridership"] = pd.to_numeric(df_filtered["Ridership"])
    
    monthly_ridership = df_filtered.groupby("Month")["Ridership"].sum()

    plt.figure(figsize=(10, 5))
    plt.bar(monthly_ridership.index, monthly_ridership.values, color="green", alpha=0.7)
    plt.xlabel("Month")
    plt.ylabel("Total Ridership")
    plt.title("Monthly Ridership")
    plt.xticks(range(1, 13))
    plt.show()



# Function to plot the yearly ridership across the different stations
def compare_annual_ridership(year, df_hunter, df_ccny, df_medgar, df_columbia, df_nyu):
    """
    Plots the total annual ridership for a given year across five predefined datasets.
    
    Parameters:
    - year (int): The year to filter the data
    - df_135_hunter, df_135_ccny, df_135_medgar, df_135_columbia, df_135_nyu (DataFrames): Ridership data for each station
    """
    datasets = [df_hunter, df_ccny, df_medgar, df_columbia, df_nyu]
    station_names = ["Hunter College", "CCNY", "Medgar Evers", "Columbia", "NYU"]
    total_ridership = []

    for df in datasets:
        # Filter for the given year and the "Total" row
        df_filtered = df[(df["Year"] == year) & 
                         (df["Month"] == "Total") & 
                         (df["DayOfWeek"] == "Total")]
        
        if not df_filtered.empty:
            total_ridership.append(df_filtered["Ridership"].values[0])  # Extract ridership value
        else:
            total_ridership.append(0)  # Default to 0 if no data is found

    # Plot the bar chart
    plt.figure(figsize=(8, 5))
    plt.bar(station_names, total_ridership, color=['blue', 'green', 'red', 'purple', 'orange'])
    
    # Formatting
    plt.xlabel("Station")
    plt.ylabel("Total Ridership")
    plt.title(f"Total Annual Ridership for {year}")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    
    plt.show()