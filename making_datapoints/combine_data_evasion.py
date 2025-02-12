import pandas as pd
from fuzzywuzzy import process

main_df = pd.read_csv('station_total_ridership_data.csv')
fare_evasion_df = pd.read_csv('../fare_evasion_data/rawdata/evasion_data_trimmed.csv')



fare_evasion_df['station'] = fare_evasion_df['station'].str.replace(' STREET', ' St', regex=False)
fare_evasion_df['station'] = fare_evasion_df['station'].str.replace(' st', ' St', regex=False)
fare_evasion_df['station'] = fare_evasion_df['station'].str.replace(' ST.', ' St', regex=False)
fare_evasion_df['station'] = fare_evasion_df['station'].str.replace(' ST', ' St', regex=False)

fare_evasion_df['station'] = fare_evasion_df['station'].str.replace(' AVENUES', ' Avs', regex=False)
fare_evasion_df['station'] = fare_evasion_df['station'].str.replace(' AVENUE', ' Av', regex=False)
fare_evasion_df['station'] = fare_evasion_df['station'].str.replace(' Ave', ' Av', regex=False)
fare_evasion_df['station'] = fare_evasion_df['station'].str.replace(' AVE.', ' Av', regex=False)
fare_evasion_df['station'] = fare_evasion_df['station'].str.replace(' AV.', ' Av', regex=False)

fare_evasion_df['station'] = fare_evasion_df['station'].str.replace(' ROAD', ' Rd', regex=False)

fare_evasion_df.to_csv('corrected_evasion_data.csv', index=False)

def get_best_match(station_name, choices, threshold = 80):
    best_match = process.extractOne(station_name, choices, score_cutoff=threshold)
    return best_match[0] if best_match else None

#making fare evasion stations name list to look at to compare later
fare_evasion_stations = fare_evasion_df['station'].tolist()

#makes column with best matched station name so it can reference this when looking at fare evasion station names
main_df['matched_station'] = main_df['station_complex'].apply(lambda x: get_best_match(x, fare_evasion_stations))

main_df.info()
#merging two datasets now
combined_df = pd.merge(main_df, fare_evasion_df, left_on='matched_station', right_on='station', how='left')

combined_df = combined_df.drop(columns=['matched_station', 'station'])

# Optionally, save the combined dataframe to a CSV
combined_df.to_csv('combined_dataset.csv', index=False)
