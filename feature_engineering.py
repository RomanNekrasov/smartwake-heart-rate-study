'''
We want to make the following functions:
- get_wake_up_times
- calculate_test_interval
- get_heartrate_data_for_interval
- check_if_woke_up_in_light_sleep
'''

import pandas as pd
import json

def get_wake_up_info(watch_night_sleep_df, behaviour_tracking_data):
    # Convert 'wake_up_time' to datetime format
    watch_night_sleep_df['wake_up_time'] = pd.to_datetime(watch_night_sleep_df['wake_up_time'], unit='s')

    # Create a mapping from 'Date' and 'Person ID' to 'wake_up_time'
    watch_night_sleep_df['Date'] = watch_night_sleep_df['wake_up_time'].dt.date
    wake_time_mapping = watch_night_sleep_df.set_index(['Date', 'Person ID'])['wake_up_time'].dt.time.to_dict()

    # Convert 'Date created' to datetime and extract the date
    behaviour_tracking_data['Date'] = pd.to_datetime(behaviour_tracking_data['Date created']).dt.date

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
