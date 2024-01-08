import pandas as pd
import matplotlib.pyplot as plt
import json

def format_mi_band_data(master_frame):
    # Create an empty dictionary to store the sub-dataframes
    
    unique_keys = ['pai',
               'valid_stand', 
               'calories',
               'steps',
               'heart_rate',
               'intensity',
               'dynamic',
               'single_heart_rate',
               'single_spo2',
               'training_load',
               'single_stress',
               'stress',
               'watch_night_sleep',
               'resting_heart_rate',
               'watch_daytime_sleep',
               'weight']
    key_dataframes = {}

    # Replace 'true'/'false' with 'True'/'False'
    master_frame['Value'] = master_frame['Value'].str.replace('true', 'True').str.replace('false', 'False', regex=False)

    for key in unique_keys:
        # Filter master_frame for the current key and reset index
        key_df = master_frame[master_frame['Key'] == key].reset_index(drop=True)

        # Apply eval to 'Value' column and create 'Value_dict' column
        key_df['Value_dict'] = key_df['Value'].apply(eval)
        
        # Iterate through the keys in the 'Value_dict' column and add them as new columns
        for sub_key in key_df['Value_dict'][0].keys():
            key_df[sub_key] = key_df['Value_dict'].apply(lambda x: x.get(sub_key, None))
        
        # Drop the original 'Value_dict' column
        key_df = key_df.drop('Value_dict', axis=1)
        
        # Store the sub-dataframe in the dictionary
        key_dataframes[key] = key_df

    return key_dataframes

def get_wake_up_info_miband(watch_night_sleep_df, behaviour_tracking_data):

    # Convert 'wake_up_time' to datetime format
    watch_night_sleep_df['wake_up_time'] = pd.to_datetime(watch_night_sleep_df['wake_up_time'], unit='s')

    # Create a mapping from 'Date' and 'Person ID' to 'wake_up_time'
    watch_night_sleep_df['Date'] = watch_night_sleep_df['wake_up_time'].dt.date
    wake_time_mapping = watch_night_sleep_df.set_index(['Date', 'Person ID'])['wake_up_time'].dt.time.to_dict()

    # Convert 'Date created' to datetime and extract the date
    # behaviour_tracking_data['Date'] = pd.to_datetime(behaviour_tracking_data['Date created']).dt.date

    # Map the wake-up time to the 'behaviour_tracking_data' using 'Date' and 'Person ID' as keys
    behaviour_tracking_data['time_of_awakening'] = behaviour_tracking_data.set_index(['Date', 'Person ID']).index.map(wake_time_mapping.get)

    # Create a mapping from 'Date' and 'Person ID' to 'state_before_awakening'
    state_before_awakening_mapping = {}
    for date, person, value in watch_night_sleep_df[['Date', 'Person ID', 'Value']].values:
        parsed_item = json.loads(value)
        last_state = int(parsed_item['items'][-1]['state'])
        state_before_awakening_mapping[(date, person)] = last_state

    # Map the 'state_before_awakening' to the 'behaviour_tracking_data'
    behaviour_tracking_data['state_before_awakening'] = behaviour_tracking_data.apply(
        lambda row: state_before_awakening_mapping.get((row['Date'], row['Person ID']), None), axis=1
    )

    return behaviour_tracking_data

def get_wake_up_info_applewatch(apple_sleep_data, aggregated_df):
    # Ensure the 'Date' in aggregated_df is in datetime.date format
    aggregated_df['Date'] = pd.to_datetime(aggregated_df['Date']).dt.date

    # Ensure the 'wake_up_date' in apple_sleep_data is in datetime.date format
    apple_sleep_data['wake_up_date'] = pd.to_datetime(apple_sleep_data['wake_up_date']).dt.date
    
    # Merge the dataframes on the date fields
    merged_df = aggregated_df.merge(apple_sleep_data, left_on='Date', right_on='wake_up_date', how='left')

    # Rename columns for clarity
    merged_df.rename(columns={'wake_up_time': 'time_of_awakening', 'last_sleep_state': 'state_before_awakening'}, inplace=True)

    # Select relevant columns to return
    columns_to_return = list(aggregated_df.columns) + ['time_of_awakening', 'state_before_awakening']
    return merged_df[columns_to_return]

def get_heartrate_data_for_interval(heartrate_df, person, date, time_of_awakening, time_interval):
    """
    Filters the heart rate data for a specific person, date, and time interval.
    Returns selected columns including relative time in seconds.
    """
    # Ensure date is a datetime object
    date = pd.to_datetime(date).date() if not isinstance(date, pd.Timestamp) else date.date()

    # Ensure time_of_awakening is a time object
    time_of_awakening = pd.to_datetime(time_of_awakening).time() if isinstance(time_of_awakening, str) else time_of_awakening

    heartrate_df['DateTime'] = pd.to_datetime(heartrate_df['Time'], unit='s')
    heartrate_df['obs_date'] = heartrate_df['DateTime'].dt.date
    heartrate_df['obs_time'] = heartrate_df['DateTime'].dt.time

    # Calculate time interval
    start_time = time_of_awakening
    end_time = (pd.Timestamp.combine(pd.to_datetime('1900-01-01').date(), start_time) + pd.Timedelta(minutes=time_interval)).time()

    # Filter the dataframe
    filtered_df = heartrate_df[
        (heartrate_df['Person ID'] == person) &
        (heartrate_df['obs_date'] == date) &
        (heartrate_df['obs_time'] >= start_time) &
        (heartrate_df['obs_time'] < end_time)
    ]

    # Calculate relative time in seconds
    start_datetime = pd.Timestamp.combine(date, start_time)
    filtered_df['Relative Time to Awakening(s)'] = (pd.to_datetime(filtered_df['Time'], unit='s') - start_datetime).dt.total_seconds()

    # Select and return required columns
    return filtered_df[['Person ID', 'Time', 'bpm', 'Relative Time to Awakening(s)']]


def calculate_test_statistics_heartrate(filtered_df):
    # Calculate the average heart rate
    average_heart_rate = float(filtered_df['bpm'].mean())

    # Calculate the average of the lowest three heart rates
    average_lowest_three = float(filtered_df['bpm'].nsmallest(3).mean()) if len(filtered_df) >= 3 else None

    # Filter data for first 10 minutes
    first_10_min_df = filtered_df[filtered_df['Relative Time to Awakening(s)'] < 600]
    average_first_10_min = float(first_10_min_df['bpm'].mean()) if len(first_10_min_df) > 0 else None

    # Filter data for first 30 minutes
    first_30_min_df = filtered_df[filtered_df['Relative Time to Awakening(s)'] < 1800]
    average_first_30_min = float(first_30_min_df['bpm'].mean()) if len(first_30_min_df) > 0 else None

    return int(len(filtered_df)), average_heart_rate, average_lowest_three, average_first_10_min, average_first_30_min



def make_timeserie_graphs():
    aggregated_df = pd.read_csv("data/aggregated_df.csv")
    heart_rate_df = pd.read_csv("data/heart_rate.csv")
    
    time_interval = 60

    # Group the data by Person ID
    grouped_data = aggregated_df.groupby('Person ID')

    for person_id, person_data in grouped_data:
        plt.figure(figsize=(12, 7))

        smart_alarm_data_list = []
        no_smart_alarm_data_list = []

        for _, row in person_data.iterrows():
            temp_df = get_heartrate_data_for_interval(heart_rate_df, row['Person ID'], row['Date'], row['time_of_awakening'], time_interval)
            temp_df['Relative Time to Awakening (min)'] = temp_df['Relative Time to Awakening(s)'] / 60

            # this cleans data for outliers
            if len(temp_df) < 6 or len(temp_df) > 100:
                continue  # Skip this day's data
            
            if row['Smart alarm']:
                smart_alarm_data_list.append(temp_df)
            else:
                no_smart_alarm_data_list.append(temp_df)

            # Plot each morning data
            color = 'green' if row['Smart alarm'] else 'red'
            plt.plot(temp_df['Relative Time to Awakening (min)'], temp_df['bpm'], color=color, alpha=0.3)

            # Highlight lowest three observations
            lowest_three = temp_df.nsmallest(3, 'bpm')
            plt.scatter(lowest_three['Relative Time to Awakening (min)'], lowest_three['bpm'], color='orange', edgecolor='black', zorder=5)

        # Plot average lines
        if smart_alarm_data_list:
            smart_alarm_data = pd.concat(smart_alarm_data_list)
            avg_smart_alarm = smart_alarm_data.groupby('Relative Time to Awakening (min)')['bpm'].mean()
            plt.plot(avg_smart_alarm.index, avg_smart_alarm.values, color='darkgreen', label='Avg with Smart Alarm', linewidth=2)

        if no_smart_alarm_data_list:
            no_smart_alarm_data = pd.concat(no_smart_alarm_data_list)
            avg_no_smart_alarm = no_smart_alarm_data.groupby('Relative Time to Awakening (min)')['bpm'].mean()
            plt.plot(avg_no_smart_alarm.index, avg_no_smart_alarm.values, color='darkred', label='Avg without Smart Alarm', linewidth=2)        

        # Draw a horizontal line at 10 minutes
        plt.axvline(x=10, color='black', linestyle='--', linewidth=1)
        plt.xlabel('Minutes since Awakening')
        plt.ylabel('Heart Rate (bpm)')
        plt.title(f"Heart Rate Data for Person {person_id}")
        plt.legend(loc='upper right')
        plt.show()

