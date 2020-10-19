import pandas as pd
from math import pi
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool,FactorRange,CustomJS
# import bokeh.palettes as bp # uncomment it if you need special colors that are pre-defined
#original_url = 'https://github.com/daenuprobst/covid19-cases-switzerland/blob/master/demographics_switzerland_bag.csv'
original_url = 'https://raw.githubusercontent.com/daenuprobst/covid19-cases-switzerland/master/demographics_switzerland_bag.csv'

df = pd.read_csv(original_url)
print(df.head(10))