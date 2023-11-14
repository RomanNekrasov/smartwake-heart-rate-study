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

    # Create a mapping from 'Date' and 'Person' to 'wake_up_time'
    watch_night_sleep_df['Date'] = watch_night_sleep_df['wake_up_time'].dt.date
    wake_time_mapping = watch_night_sleep_df.set_index(['Date', 'Person'])['wake_up_time'].dt.time.to_dict()

    # Convert 'Date created' to datetime and extract the date
    behaviour_tracking_data['Date'] = pd.to_datetime(behaviour_tracking_data['Date created']).dt.date

    # Map the wake-up time to the 'behaviour_tracking_data' using 'Date' and 'Name' as keys
    behaviour_tracking_data['time_of_awakening'] = behaviour_tracking_data.set_index(['Date', 'Name']).index.map(wake_time_mapping.get)

    # Create a mapping from 'Date' and 'Person' to 'state_before_awakening'
    state_before_awakening_mapping = {}
    for date, person, value in watch_night_sleep_df[['Date', 'Person', 'Value']].values:
        parsed_item = json.loads(value)
        last_state = int(parsed_item['items'][-1]['state'])
        state_before_awakening_mapping[(date, person)] = last_state

    # Map the 'state_before_awakening' to the 'behaviour_tracking_data'
    behaviour_tracking_data['state_before_awakening'] = behaviour_tracking_data.apply(
        lambda row: state_before_awakening_mapping.get((row['Date'], row['Name']), None), axis=1
    )

    return behaviour_tracking_data

def get_heartrate_data_for_interval(heartrate_df, person, date, time_of_awakening, time_interval):
    # Ensure date is a datetime object
    print(person, date, time_of_awakening, time_interval)
    if not isinstance(date, pd.Timestamp):
        date = pd.to_datetime(date).date()  # Get only the date part

    # Ensure time_of_awakening is a time object
    if isinstance(time_of_awakening, str):
        time_of_awakening = pd.to_datetime(time_of_awakening).time()

    heartrate_df['DateTime'] = pd.to_datetime(heartrate_df['Time'], unit='s')
    heartrate_df['obs_date'] = heartrate_df['DateTime'].dt.date
    heartrate_df['obs_time'] = heartrate_df['DateTime'].dt.time

    # Calculate start_time directly from time_of_awakening
    start_time = time_of_awakening
    generic_date = pd.to_datetime('1900-01-01').date()
    end_time = (pd.Timestamp.combine(generic_date, start_time) + pd.Timedelta(minutes=time_interval)).time()

    # First, filter the dataframe for the person and the matching date
    filtered_df = heartrate_df[(heartrate_df['Person'] == person) & (heartrate_df['obs_date'] == date)]

    # calculate average over that day
    #day_average_heart_rate = filtered_df['bpm'].mean()
    # Then, filter by the time interval
    filtered_df = filtered_df[(filtered_df['obs_time'] >= start_time) & (filtered_df['obs_time'] < end_time)]

    # Calculate the average heart rate
    average_heart_rate = float(filtered_df['bpm'].mean())

    # Calculate the average of the lowest three heart rates
    if len(filtered_df) >= 3:
        average_lowest_three = float(filtered_df['bpm'].nsmallest(3).mean())
    else:
        average_lowest_three = None
    print(len(filtered_df), average_heart_rate, average_lowest_three)

    return int(len(filtered_df)), average_heart_rate, average_lowest_three

