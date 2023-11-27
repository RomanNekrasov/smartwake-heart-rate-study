import os
import pandas as pd

def process_fitness_data():
    # Set the directory (adjust this to your local directory)
    path = '/Users/Gerard/Downloads'

    # Define the file names (adjust these if the names change)
    fitness_files = [
        '20231030_8210796956_MiFitness_hlth_center_fitness_data.csv',
        '20231030_8211531339_MiFitness_hlth_center_fitness_data.csv',
        '20231031_8210564343_MiFitness_hlth_center_fitness_data.csv',
        '20231110_8210586841_MiFitness_hlth_center_fitness_data.csv'
    ]
    behavior_file = 'Behavioural data app.csv'

    # Reading and concatenating the fitness data files with automated Person IDs
    master_frame = pd.DataFrame()
    for idx, file in enumerate(fitness_files, start=1):
        temp_df = pd.read_csv(os.path.join(path, file))
        temp_df['Person ID'] = idx
        master_frame = pd.concat([master_frame, temp_df], ignore_index=True)

    # Read behavior tracking data
    behaviour_tracking_data = pd.read_csv(os.path.join(path, behavior_file))

    # Unique keys
    unique_keys = ['pai', 'valid_stand', 'calories', 'steps', 'heart_rate',
                   'intensity', 'dynamic', 'single_heart_rate', 'single_spo2',
                   'training_load', 'single_stress', 'stress', 'watch_night_sleep',
                   'resting_heart_rate', 'watch_daytime_sleep', 'weight']

    # Formatting data
    key_dataframes = {key: master_frame.filter(like=key) for key in unique_keys}

    return key_dataframes

# You can call the function like this:
# key_dataframes = process_fitness_data()
