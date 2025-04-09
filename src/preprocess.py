'''
    Contains some functions to preprocess data (not used in current pie/bar chart).
'''
import pandas as pd

def convert_dates(dataframe: pd.DataFrame):
    '''
        Converts the dates in the dataframe to datetime objects.
    '''
    dataframe['Date_Plantation'] = pd.to_datetime(dataframe['Date_Plantation'])
    return dataframe

def filter_years(dataframe: pd.DataFrame, start, end):
    '''
        Filters the elements of the dataframe by date.
    '''
    dataframe = dataframe[(dataframe['Date_Plantation'].dt.year >= start) & 
                          (dataframe['Date_Plantation'].dt.year <= end)]
    return dataframe

def summarize_yearly_counts(dataframe: pd.DataFrame):
    '''
        Groups the data by neighborhood and year, summing counts.
    '''
    return dataframe.groupby(['Arrond_Nom', dataframe['Date_Plantation'].dt.year]).size().reset_index(name='Counts')

def restructure_df(yearly_df: pd.DataFrame):
    '''
        Restructures the dataframe for heatmap-like display.
    '''
    return yearly_df.pivot(index='Arrond_Nom', columns='Date_Plantation', values='Counts').fillna(0)