import requests

# Origin Destination 2024 Dataset - Auguest to September, 
url = "https://data.ny.gov/resource/jsu2-fbtj.csv?$query=SELECT%20%60year%60,%20%60month%60,%20%60day_of_week%60,%20%60hour_of_day%60,%20%60timestamp%60,%20%60origin_station_complex_id%60,%20%60origin_station_complex_name%60,%20%60origin_latitude%60,%20%60origin_longitude%60,%20%60destination_station_complex_id%60,%20%60destination_station_complex_name%60,%20%60destination_latitude%60,%20%60destination_longitude%60,%20%60estimated_average_ridership%60,%20%60origin_point%60,%20%60destination_point%60%20WHERE%20(%60month%60%20BETWEEN%208%20AND%209)%20AND%20(%60hour_of_day%60%20BETWEEN%206%20AND%2020)%20ORDER%20BY%20%60month%60%20DESC%20NULL%20LAST,%20%60hour_of_day%60%20DESC%20NULL%20LAST"

response = requests.get(url)

with open("ny_ridership_aug_sep.csv", "wb") as f:
    f.write(response.content)

print("Download complete: ny_ridership_aug_sep.csv")
