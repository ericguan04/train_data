import os
import uuid
import json
import dash
import folium
import pandas as pd
import geopandas as gpd

from dash import dcc, html
from dash.dependencies import Input, Output, State

# === Load and Merge All Your Data ===
hunter1 = pd.read_csv("datasets/hunter/MTA_Subway_Origin-Destination_2021_Hunter_Origin.csv")
hunter2 = pd.read_csv("datasets/hunter/MTA_Subway_Origin-Destination_2022_Hunter_Origin.csv")
hunter3 = pd.read_csv("datasets/hunter/MTA_Subway_Origin-Destination_2023_Hunter_Origin.csv")
hunter4 = pd.read_csv("datasets/hunter/MTA_Subway_Origin-Destination_2024_Hunter_Origin.csv")
hunter_total = pd.concat([hunter1, hunter2, hunter3, hunter4])

geojson_file = "datasets/nyc_zipcode_geodata/nyc-zip-code-tabulation-areas-polygons.geojson"
gdf = gpd.read_file(geojson_file)
zip_coords = pd.read_csv("datasets/nyc_zipcode_geodata/uszipcodes_geodata.csv")
income_data = pd.read_csv("datasets/nyc_median_income_zipcode.csv")
mta_stations = pd.read_csv("datasets/MTA_Subway_Stations_and_Complexes_20250225.csv")

gdf["postalCode"] = gdf["postalCode"].astype(str)
zip_coords["ZIP"] = zip_coords["ZIP"].astype(str)
income_data["zipcode"] = income_data["zipcode"].astype(str)

gdf = gdf.merge(zip_coords, left_on="postalCode", right_on="ZIP", how="left")
gdf = gdf.merge(income_data, left_on="postalCode", right_on="zipcode", how="left")
geojson_data = json.loads(gdf.to_json())

# === Utility Functions ===
def get_income_color(income):
    if pd.isna(income):
        return "gray"
    elif income < 50000:
        return "red"
    elif income < 100000:
        return "orange"
    elif income < 150000:
        return "yellow"
    elif income < 200000:
        return "lightgreen"
    else:
        return "green"

def top_station_destinations(ridership_df, top_n=5):
    top_destinations = ridership_df.groupby(
        ["Destination Station Complex Name", "Destination Station Complex ID", "Destination Latitude", "Destination Longitude"]
    )["Estimated Average Ridership"].sum().sort_values(ascending=False).head(top_n)
    return top_destinations

def top_destination_income_map(ridership_df, top_n, start_time, end_time, day_of_week, month, year):
    df = ridership_df[
        (ridership_df["Hour of Day"] >= start_time) &
        (ridership_df["Hour of Day"] <= end_time) &
        (ridership_df["Day of Week"] == day_of_week) &
        (ridership_df["Month"] == month) &
        (ridership_df["Year"] == year)
    ]

    m = folium.Map(location=[40.7128, -74.0060], zoom_start=11)

    folium.GeoJson(
        geojson_data,
        name="NYC Neighborhoods",
        style_function=lambda x: {
            "fillColor": get_income_color(x["properties"].get("income_household_median", None)),
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.6,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["postalCode", "income_household_median"],
            aliases=["ZIP Code", "Median Household Income"],
            localize=True,
        ),
    ).add_to(m)

    top_destinations_df = top_station_destinations(df, top_n)
    if isinstance(top_destinations_df, pd.Series):
        top_destinations_df = top_destinations_df.reset_index()

    max_ridership = top_destinations_df["Estimated Average Ridership"].max()
    min_radius = 5
    max_radius = 15

    for _, row in top_destinations_df.iterrows():
        if pd.notna(row["Destination Latitude"]) and pd.notna(row["Destination Longitude"]):
            ridership = row["Estimated Average Ridership"]
            radius = min_radius + (ridership / max_ridership) * (max_radius - min_radius)

            folium.CircleMarker(
                location=[row["Destination Latitude"], row["Destination Longitude"]],
                radius=radius,
                color="blue",
                fill=True,
                fill_color="blue",
                fill_opacity=0.7,
                popup=folium.Popup(
                    f"Station: {row['Destination Station Complex Name']}<br>"
                    f"Station ID: {row['Destination Station Complex ID']}<br>"
                    f"Ridership: {ridership:,.0f}",
                    max_width=300,
                ),
                tooltip=row["Destination Station Complex Name"],
            ).add_to(m)

    if not df.empty:
        origin_df = df.iloc[0]
        folium.CircleMarker(
            location=[origin_df["Origin Latitude"], origin_df["Origin Longitude"]],
            radius=10,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.7,
            popup=folium.Popup(
                f"Station: {origin_df['Origin Station Complex Name']}<br>"
                f"Station ID: {origin_df['Origin Station Complex ID']}",
                max_width=300,
            ),
            tooltip=origin_df["Origin Station Complex Name"],
        ).add_to(m)

    return m

# === Dash App ===
app = dash.Dash(__name__)

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

app.layout = html.Div([
    html.H1("Top Ridership Destination Timelapse", style={"textAlign": "center"}),

    html.Div([
        html.Button("Play / Pause", id="play-button", n_clicks=0),
        dcc.Interval(id="play-interval", interval=2000, n_intervals=0, disabled=True),
    ], style={"padding": "10px"}),

    html.Div([
        html.Label("Month"),
        dcc.Slider(id="month-slider", min=1, max=12, step=1, value=1,
                   marks={i: str(i) for i in range(1, 13)}),
    ], style={"padding": "10px"}),

    html.Div([
        html.Label("Hour"),
        dcc.Slider(id="hour-slider", min=0, max=23, step=1, value=8,
                   marks={i: str(i) for i in range(0, 24, 3)}),
    ], style={"padding": "10px"}),

    html.Div([
        html.Label("Day of Week"),
        dcc.Dropdown(
            id="day-dropdown",
            options=[{"label": day, "value": day} for day in days],
            value="Monday"
        )
    ], style={"padding": "10px", "width": "300px"}),

    html.Div([
        html.Label("Top N Destinations"),
        dcc.Slider(id="top-n-slider", min=5, max=30, step=5, value=15,
                   marks={i: str(i) for i in range(5, 31, 5)}),
    ], style={"padding": "10px"}),

    html.Div([
        html.Label("Year"),
        dcc.Slider(id="year-slider", min=2021, max=2024, step=1, value=2021,
                marks={i: str(i) for i in range(2021, 2025)}),
    ], style={"padding": "10px"}),

    html.Iframe(id="map", width="100%", height="600")
])

# === Toggle Play Button ===
@app.callback(
    Output("play-interval", "disabled"),
    Input("play-button", "n_clicks"),
    State("play-interval", "disabled")
)
def toggle_play(n_clicks, disabled):
    return not disabled

# === Advance Time Every Tick ===
@app.callback(
    Output("hour-slider", "value"),
    Output("day-dropdown", "value"),
    Output("year-slider", "value"),
    Output("month-slider", "value"),
    Input("play-interval", "n_intervals"),
    State("hour-slider", "value"),
    State("day-dropdown", "value"),
    State("year-slider", "value"),
    State("month-slider", "value"),
)
def advance_time(n, hour, day, year, month):
    day_index = days.index(day)
    hour += 1
    if hour > 23:
        hour = 0
        day_index += 1
        if day_index >= len(days):
            day_index = 0
            month += 1
            if month > 12:
                month = 1
                year += 1
                if year > 2024:
                    year = 2021
    return hour, days[day_index], year, month

# === Update Map ===
@app.callback(
    Output("map", "srcDoc"),
    Input("year-slider", "value"),
    Input("month-slider", "value"),
    Input("hour-slider", "value"),
    Input("day-dropdown", "value"),
    Input("top-n-slider", "value"),
)
def update_map(year, month, hour, day, top_n):
    folium_map = top_destination_income_map(
        hunter_total,
        top_n=top_n,
        start_time=hour,
        end_time=hour + 1,
        day_of_week=day,
        month=month,
        year=year,
    )

    tmp_file = f"temp_map_{uuid.uuid4().hex}.html"
    folium_map.save(tmp_file)
    with open(tmp_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    os.remove(tmp_file)
    return html_content

if __name__ == "__main__":
    app.run(debug=True)
