# Smart-Wake Study
A Smart Alarm’s Effect on Morning Cardiac Activity

## About The Project 
Smartwatches offer users features like heart rate monitoring and sleep analysis, utilizing heart rate measurements to classify sleep stages. This study enhances the ecological validity of findings by observing sleep patterns over a month, employing on-body sensors for real-life sleep data. Unlike previous research, the focus is on quantitative, accurate, and ecologically valid data collection, combining it with smart-wake systems to assess post-awakening heart rate effects while maintaining strict adherence to ethical and legal standards

### Built With
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB)](https://www.python.org/downloads/)

### Project Structure
This project is structured in jupyter notebooks in the following order: 
1. EDA.ipynb
2. preprocessing.ipynb
3. analysis.ipynb
4. model_selection.ipynb

The output of each notebook serves as input for the next notebook. All functions used can be found in functions.py.

## EDA.ipynb
This notebooks contains all code applied to explore the raw collected data. This includes initial structuring of the data, that is needed for initial data exploration. The notebook contains: 
- heart rate data exploration
- sleep data exploration
- behavioral data exploration

## preprocessing.ipynb
This file contains all preprocessing needed for further analysis. From two types of smartwatches, data was extracted, leading to the processing of two different formats. This code results in an aggregated dataframe containing Xiaomi heart and sleep data, as well as Apple heart and sleep data. 

## analysis.ipynb 
This notebook contains all code needed for in depth analysis on heart and sleep data separately, as well as combined analysis. Data is analyzed for each participant in the dataset separately. In addition, comparisons can be analyzed between the participants.

## model_selection.ipynb
To test the effect of the smart-wake system on post-awakening heart rate OLS is applied. In this notebook, you can find the check for OLS assumptions as well as the model itself and model results. 

## functions.py 
Contains all defined functions needed to run the code in all notebooks seamlessly. Functions are imported in each of the notebook, when necessary 

## Data Description
Data is collected from Xiaomi smartwatches and an Apple watch, in the form of csv files and an xml file. Preprocessing for these exact formats is included in EDA.jpynb and preprocessing.jpynb. These files contain different heart rate and sleep related features. The behavioral tracking data is also included in the form of an excel file, requiring minimal preprocessing. 

An overview of the complete preprocessed data (aggregated_df.csv) resulting from the preprocessing notebook can be found below:
| Column Name                 | Type    | Description                                                         |
|-----------------------------|---------|---------------------------------------------------------------------|
| Person ID                   | int64   | Unique key identifier for subject                                   |
| Drinks                      | int64   | Whether the subject consumed alcohol the day before                 |
| Fastfood                    | int64   | Whether the subject consumed fast food the day before               |
| Sports                      | int64   | Whether the subject has exercised the day before                    |
| Food 2h before sleep        | int64   | Whether the subject has had food 2h before bedtime                  |
| Medication                  | int64   | Whether the subject took medication the day before                  |
| Date created                | object  | The date of logging data                                            |
| Woke up by (smart) alarm    | int64   | Whether the subject woke up by smart alarm                          |
| Woke up by external factors | int64   | Whether the subject woke up by external factors                     |
| Slept again after alarm     | int64   | Whether the subject slept again after their alarm                   |
| Smart alarm                 | int64   | Whether the subject used their smart alarm                          |
| time_of_awakening           | object  | The time the subject woke up                                        |
| state_before_awakening      | float64 | Sleep state before the subject woke up                              |
| Number of Measurements      | object  | The number of heart rate measurements in the corresponding interval |
| Average Heart Rate          | object  | The average heart rate in the corresponding interval                |
| Average Lowest Three obs    | object  | The average of the lowest three heart rate observations             |
| Average First Ten min       | object  | The average heart rate in the first ten minutes after waking        |
| Average First Thirty min    | object  | The average heart rate in the first thirty minutes after waking     |












