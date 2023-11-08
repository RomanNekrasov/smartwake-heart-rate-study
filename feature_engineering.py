'''
We want to make the following functions:
- get_wake_up_times
- calculate_sleep_duration
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
        last_state = parsed_item['items'][-1]['state']
        state_before_awakening_mapping[(date, person)] = last_state

    # Map the 'state_before_awakening' to the 'behaviour_tracking_data'
    behaviour_tracking_data['state_before_awakening'] = behaviour_tracking_data.apply(
        lambda row: state_before_awakening_mapping.get((row['Date'], row['Name']), None), axis=1
    )

    return behaviour_tracking_data
