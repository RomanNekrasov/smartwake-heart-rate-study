import xml.etree.ElementTree as ET
import pandas as pd
import os

def format_apple_data():
    df = read_apple_health_xml()
    df = clean_and_filter_data(df)
    df_filtered = df[df['type'].isin(['SleepAnalysis', 'HeartRate'])]
    heart_rate_df = make_heart_rate_df(df_filtered)
    sleep_summary_df = make_sleep_df(df_filtered)
    sleep_summary_df.to_csv('Data/sleep_apple.csv', index=False)
    heart_rate_df.to_csv('Data/heart_rate_apple.csv', index=False)

def read_apple_health_xml():
    # Load and parse the XML file
    current_path = os.getcwd()
    tree = ET.parse(current_path + '/Data/export_5.xml')  # Replace with the path to your XML file
    root = tree.getroot()

    # Extract data into a list of dictionaries
    data = []
    for record in root.findall('Record'):
        record_data = record.attrib  # Extract attributes of the Record tag
        for metadata in record.findall('MetadataEntry'):
            record_data[metadata.get('key')] = metadata.get('value')
        data.append(record_data)

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(data)
    return df

def clean_and_filter_data(df):
    df['type'] = df['type'].str.replace('HKQuantityTypeIdentifier', '')
    df['type'] = df['type'].str.replace('HKCategoryTypeIdentifier', '')
    df['creationDate'] = pd.to_datetime(df['creationDate'])

    # Filter for the date range
    start_date = '2023-09-30'
    end_date = '2023-10-28'
    df = df[(df['creationDate'] >= start_date) & (df['creationDate'] <= end_date)]

    df['startDate'] = pd.to_datetime(df['startDate'])
    df['endDate'] = pd.to_datetime(df['endDate'])
    return df

def make_heart_rate_df(df):
    heart_rate_df = df[df['type'] == 'HeartRate']
    heart_rate_df = heart_rate_df[['creationDate', 'startDate', 'endDate', 'value']]
    return heart_rate_df

def make_sleep_df(df):
    sleep_analysis_df = df[df['type'] == 'SleepAnalysis']
    sleep_analysis_df['startDate'] = pd.to_datetime(sleep_analysis_df['startDate'])
    sleep_analysis_df['endDate'] = pd.to_datetime(sleep_analysis_df['endDate'])
    sleep_analysis_df['creationDate'] = pd.to_datetime(sleep_analysis_df['creationDate'])

    # Filter out 'HKCategoryValueSleepAnalysisInBed'
    sleep_analysis_df = sleep_analysis_df[sleep_analysis_df['value'] != 'HKCategoryValueSleepAnalysisInBed']

    # Define a function to categorize sleep states
    def categorize_sleep_state(value):
        if 'Deep' in value:
            return 4
        elif 'REM' in value:
            return 2
        elif 'Core' in value:  # Assuming 'Core' is light sleep
            return 3
        elif 'Awake' in value:
            return 1
        else:
            return 'unknown'

    # Categorize each record
    sleep_analysis_df['sleep_state'] = sleep_analysis_df['value'].apply(categorize_sleep_state)

    # Calculate the duration for each record in minutes
    sleep_analysis_df['duration'] = (sleep_analysis_df['endDate'] - sleep_analysis_df['startDate']).dt.total_seconds() / 60
    aggregated_data = []

    # Process each day's data
    for creation_date, day_data in sleep_analysis_df.groupby('creationDate'):
        # Ensure day_data is sorted by startDate to get the correct last record
        day_data_sorted = day_data.sort_values(by='startDate')

        # Fetch the wake-up time from the last record's creationDate
        wake_up_date = day_data_sorted['creationDate'].iloc[-1].date()
        wake_up_time = day_data_sorted['creationDate'].iloc[-1].time()

        # Calculate the total duration for each sleep state
        sleep_durations = day_data_sorted.groupby('sleep_state')['duration'].sum()

        day_summary = {
            'creation_date': creation_date,
            'wake_up_date': wake_up_date, 
            'wake_up_time': wake_up_time,
            'last_sleep_state': day_data_sorted['sleep_state'].iloc[-1],
            'sleep_deep_duration': sleep_durations.get(4, 0),  
            'sleep_light_duration': sleep_durations.get(3, 0),  
            'sleep_rem_duration': sleep_durations.get(2, 0),  
            'sleep_awake_duration': sleep_durations.get(1, 0), 
            'total_sleep_duration': sum(sleep_durations)
        }
        aggregated_data.append(day_summary)

    # Convert the list of dictionaries to a DataFrame
    sleep_summary_df = pd.DataFrame(aggregated_data)
    return sleep_summary_df