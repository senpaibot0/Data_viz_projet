'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd


def convert_dates(dataframe: pd.DataFrame):
    '''
        Converts the dates in the dataframe to datetime objects.

        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with datetime-formatted dates.
    '''
    # TODO : Convert dates
    dataframe['Date_Plantation'] = pd.to_datetime(dataframe['Date_Plantation'])
    return dataframe


def filter_years(dataframe: pd.DataFrame, start, end):
    '''
        Filters the elements of the dataframe by date, making sure
        they fall in the desired range.

        Args:
            dataframe: The dataframe to process
            start: The starting year (inclusive)
            end: The ending year (inclusive)
        Returns:
            The dataframe filtered by date.
    '''
    dataframe = dataframe[(dataframe['Date_Plantation'].dt.year >= start) & (
        dataframe['Date_Plantation'].dt.year <= end)]
    # TODO : Filter by dates
    return dataframe


def summarize_yearly_counts(dataframe: pd.DataFrame):
    '''
        Groups the data by neighborhood and year,
        summing the number of trees planted in each neighborhood
        each year.

        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with column 'Counts'
            containing the counts of planted
            trees for each neighborhood each year.
    '''
    # TODO : Summarize df
    return dataframe.groupby(['Arrond_Nom', dataframe['Date_Plantation'].dt.year]).size().reset_index(name='Counts')


def restructure_df(yearly_df: pd.DataFrame):
    '''
        Restructures the dataframe into a format easier
        to be displayed as a heatmap.

        The resulting dataframe should have as index
        the names of the neighborhoods, while the columns
        should be each considered year. The values
        in each cell represent the number of trees
        planted by the given neighborhood the given year.

        Any empty cells are filled with zeros.

        Args:
            yearly_df: The dataframe to process
        Returns:
            The restructured dataframe
    '''
    # TODO : Restructure df and fill empty cells with 0
    return yearly_df.pivot(index='Arrond_Nom', columns='Date_Plantation', values='Counts').fillna(0)


def get_daily_info(dataframe: pd.DataFrame, arrond, year):
    '''
        From the given dataframe, gets
        the daily amount of planted trees
        in the given neighborhood and year.

        Args:
            dataframe: The dataframe to process
            arrond: The desired neighborhood
            year: The desired year
        Returns:
            The daily tree count data for that
            neighborhood and year.
    '''
    # TODO : Get daily tree count data and return
    

    filtered_data = dataframe[(dataframe['Arrond'] == arrond) & (dataframe['Date_Plantation'].dt.year == year)]

    daily_tree_count = filtered_data.groupby(filtered_data['Date_Plantation'].dt.date).size().reset_index(name='Trees')

    return daily_tree_count