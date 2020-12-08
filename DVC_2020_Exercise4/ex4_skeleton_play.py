import numpy as np
import pandas as pd
import geopandas as gpd
from datetime import datetime,timedelta

import bokeh.palettes as bp
from bokeh.plotting import figure,curdoc
from bokeh.transform import linear_cmap
from bokeh.layouts import column, row
from bokeh.models import (CDSView, 
						HoverTool,ColorBar,
						GeoJSONDataSource, 
						Patches,
						RadioButtonGroup,
						DateSlider,
						Button)


# ====================================================================
# Goal: Visualize demographics and daily new cases statistics in Switzerland

# The visualization output contains 2 parts: 

# Part 1: add a map view and the color encodes the Density and BedsPerCapita, 
# with a RadioButtonGroup which controls which aspect to show. 


# Part 2: add a circle in each canton on the map, size of circle represents the current daily new cases per capita,
# add a timeline slider, add callback function controlling the slider and changing the size of the circle on the map when dragging the time slider.
# Additionally, a "Play" button can animate the slider as well as circles on the map.  

# Reference link
# https://towardsdatascience.com/walkthrough-mapping-basics-with-bokeh-and-geopandas-in-python-43f40aa5b7e9

# ====================================================================



### Task 1: Data Preprocessing

## T1.1 Read and filter data 
# Four data sources:
# Demographics.csv: the statistics data about population density and hospital beds per capita in each canton
# covid_19_cases_switzerland_standard_format.csv: the location(longitude, latitude) of the capital city in each canton
# covid19_cases_switzerland_openzh-phase2.csv: same as in ex2, daily new cases in each canton
# gadm36_CHE_1.shp: the shape file contains geometry data of swiss cantons, and is provided in the "data" folder. 
# Please do not submit any data file with your solution, and you can asssume your solution is at the same directory as data 


demo_url = 'https://github.com/daenuprobst/covid19-cases-switzerland/blob/master/demographics.csv'
local_url = 'https://github.com/daenuprobst/covid19-cases-switzerland/blob/master/covid_19_cases_switzerland_standard_format.csv'
case_url = 'https://github.com/daenuprobst/covid19-cases-switzerland/blob/master/covid19_cases_switzerland_openzh-phase2.csv'
shape_dir = 'data/gadm36_CHE_1.shp'


# Read from demo_url into a dataframe using pandas
demo_raw = ...


# Read from local_url into a dataframe using pandas
local_raw = ...
# Extract unique 'abbreviation_canton','lat','long' combinations from local_raw
canton_point = ... 


# Read from case_url into a dataframe using pandas
case_raw = ... 
# Create a date list from case_raw and convert to datatime form
dates = ...


# Read shape file from shape_dir unsing geopandas
shape_raw = ...
# Extract canton name abbreviations from the attribute 'HASC_1', e.g. CH.AG --> AG, CH.ZH --> ZH
# And save into a new column named 'Canton' 
shape_raw['Canton'] = ...
canton_poly = shape_raw[['geometry','Canton']]





## T1.2 Merge data and build a GeoJSONDataSource

# Merge canton_poly with demo_raw on attribute name 'Canton' into dataframe merged,
# then merge the result with canton_point on 'Canton' and 'abbreviation_canton' respectively


# Potential issue: 
# https://stackoverflow.com/questions/57045479/is-there-a-way-to-fix-maximum-recursion-level-in-python-3
merged = ...





# For each date, extract a list of daily new cases per capita from all cantons(e.g. 'AG_diff_pc', 'AI_diff_pc', etc.), and add as a new column in merged
# For instance, in the column['2020-10-31'], there are: [0.0005411327220155498, nan, nan, 0.000496300306803826, ...]
for i,d in enumerate(dates_raw):
	...

	merged[d] = ...

# Calculate circle sizes that are proportional to dnc per capita
# Set the latest dnc as default 
merged['size'] = merged.iloc[:,-1]*1e5/5+10
merged['dnc'] = merged.iloc[:,-1]

# Build a GeoJSONDataSource from merged
geosource = GeoJSONDataSource(...)




# Task 2: Data Visualization

# T2.1 Create linear color mappers for 2 attributes in demo_raw: population density, hospital beds per capita 
# Map their maximum values to the high, and mimimum to the low
labels = ['Density','BedsPerCapita']

mappers = {} 
mappers['Density'] = ...
mappers['BedsPerCapita'] = ...


# T2.2 Draw a Switzerland Map on canton level

# Define a figure 
p1 = figure(title = 'Demographics in Switzerland', 
					 plot_height = 600 ,
					 plot_width = 950, 
					 toolbar_location = 'above',
					 tools = "pan, wheel_zoom, box_zoom, reset")

p1.xgrid.grid_line_color = None
p1.ygrid.grid_line_color = None

# Plot the map using patches, set the fill_color as mappers['Density']
cantons = p1.patches(...)


# Create a colorbar with mapper['Density'] and add it to above figure
color_bar = ColorBar(...)
p1.add_layout(color_bar, 'right')


# Add a hovertool to display canton, density, bedspercapita and dnc 
hover = HoverTool(tooltips=[...] ,renderers=[cantons])

p1.add_tools(hover)



# T2.3 Add circles at the locations of capital cities for each canton, and the sizes are proportional to daily new cases per capita
sites = p1.circle(...)


# T2.4 Create a radio button group with labels 'Density', and 'BedsPerCapita'
buttons = RadioButtonGroup(...)

# Define a function to update color mapper used in both patches and colorbar 
def update_bar(new):
	for i,d in enumerate(labels):
		if i == new:
			...


buttons.on_click(...)


# T2.5 Add a dateslider to control which per capita daily new cases information to display

# Define a dateslider using maximum and mimimum dates, set value to be the latest date
timeslider = DateSlider(...)

# Complete the callback function 
# Hints: 
# 	convert the timestamp value from the slider to datetime and format it in the form of '%Y-%m-%d'
#	update columns 'size', 'dnc' with the column named '%Y-%m-%d' in merged
#	update geosource with new merged

def callback(attr,old,new):
	# Convert timestamp to datetime
	# https://stackoverflow.com/questions/9744775/how-to-convert-integer-timestamp-to-python-datetime
	date = ...
	i = date.strftime('%Y-%m-%d')

	merged.size = ...
	merged.dnc = ...
	geosource.geojson = ...


# Circles change on mouse move
timeslider.on_change(...)


# T2.6 Add a play button to change slider value and update the map plot dynamically
# https://stackoverflow.com/questions/46420606/python-bokeh-add-a-play-button-to-a-slider
# https://stackoverflow.com/questions/441147/how-to-subtract-a-day-from-a-date

# Update the slider value with one day before current date
def animate_update_slider():
	# Extract date from slider's current value 
	date = ...
	# Subtract one day from date and do not exceed the allowed date range
	day = ...

	...

	timeslider.value = day

# Define the callback function of button
def animate():
	global callback_id
	if button.label == '► Play':
		button.label = '❚❚ Pause'
		callback_id = curdoc().add_periodic_callback(animate_update_slider, 500)
	else:
		button.label = '► Play'
		curdoc().remove_periodic_callback(callback_id)

button = Button(label='► Play', width=80, height=40)
button.on_click(animate)




curdoc().add_root(column(p1,buttons, row(timeslider,button)))



