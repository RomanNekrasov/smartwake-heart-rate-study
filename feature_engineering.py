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

def get_wake_up_info(watch_night_sleep_df,behaviour_tracking_data):
    # Convert 'wake_up_time' to datetime format
    watch_night_sleep_df['wake_up_time'] = pd.to_datetime(watch_night_sleep_df['wake_up_time'], unit='s')

    # Create a mapping from 'Date' and 'Person' to 'wake_up_time'
    watch_night_sleep_df['Date'] = watch_night_sleep_df['wake_up_time'].dt.date
    wake_time_mapping = watch_night_sleep_df.set_index(['Date', 'Person'])['wake_up_time'].dt.time.to_dict()

    # Convert 'Date created' to datetime and extract the date
    behaviour_tracking_data['Date'] = pd.to_datetime(behaviour_tracking_data['Date created']).dt.date

    # Map the wake-up time to the 'behaviour_tracking_data' using 'Date' and 'Name' as keys
    behaviour_tracking_data['time_of_awakening'] = behaviour_tracking_data.set_index(['Date', 'Name']).index.map(wake_time_mapping.get)

    state_before_awakening = []
    '''

    This should be corrected to the following:
    length is not same -> probably not all have items???
    
    for item in watch_night_sleep_df['Value']:
        # Parse the JSON string into a Python dictionary
        parsed_item = json.loads(item)
        
        # Extract the state of the last item in the 'items' list
        last_state = parsed_item['items'][-1]['state']
        
        # Append the extracted state to the list
        state_before_awakening.append(last_state)

    # Now, we can add this list as a new column to the DataFrame
    # If you're planning to add it to the original DataFrame, ensure that the index aligns correctly
    behaviour_tracking_data['state_before_awakening'] = state_before_awakening
    '''

    return behaviour_tracking_data