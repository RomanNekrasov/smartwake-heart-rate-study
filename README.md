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

## Data Description
Data is collected from Xiaomi smartwatches and an Apple watch, in the form of csv files and an xml file. Preprocessing for these exact formats is included in EDA.jpynb and preprocessing.jpynb. These files contain different heart rate and sleep related features. The behavioral tracking data is also included in the form of an excel file, requiring minimal preprocessing. 


## Study Reproducibility
For reproducibility purposes, a consent form template and the information letter are available.
