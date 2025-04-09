from template import create_custom_theme, set_default_theme
from preprocess import convert_dates, filter_years, summarize_yearly_counts, restructure_df, get_daily_info
import pandas as pd
from heatmap import get_figure
data = pd.read_csv('../TP3/src/assets/data/arbres.csv')#assets/data/arbres.csv

data = convert_dates(data)

data = restructure_df(summarize_yearly_counts(filter_years(data, 2010, 2020)))


fig = get_figure(data)
