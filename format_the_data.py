import json
import pandas as pd
def format_data(unique_keys, master_frame):
# Create an empty dictionary to store the sub-dataframes
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