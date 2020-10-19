import pandas as pd 
from math import pi
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool,FactorRange,CustomJS
# import bokeh.palettes as bp # uncomment it if you need special colors that are pre-defined

 
### Task 1: Data Preprocessing
 

## T1.1 Read online .csv file into a dataframe using pandas
# Reference links: 
# https://pandas.pydata.org/pandas-docs/stable/reference/frame.html
# https://stackoverflow.com/questions/55240330/how-to-read-csv-file-from-github-using-pandas 

original_url = 'https://github.com/daenuprobst/covid19-cases-switzerland/blob/master/demographics_switzerland_bag.csv'
raw_content_url = 'https://raw.githubusercontent.com/daenuprobst/covid19-cases-switzerland/master/demographics_switzerland_bag.csv'
df = pd.read_csv(raw_content_url)
#print(df.head(3))



## T1.2 Prepare data for a grouped vbar_stack plot
# Reference link, read first before starting: 
# https://docs.bokeh.org/en/latest/docs/user_guide/categorical.html#stacked-and-grouped


# Filter out rows containing 'CH' 
boolean_check_for_CH = df['canton']!='CH'
df =  df[boolean_check_for_CH]
#print(df.head(9))

# Extract unique value lists of canton, age_group and sex
canton = df.canton.unique()
#print(canton)
age_group = df.age_group.unique()
#print(age_group)
sex = df.sex.unique()
#print(sex)


# Create a list of categories in the form of [(canton1,age_group1), (canton2,age_group2), ...]
factors = []
for cant in canton:
    for age in age_group:
        factors.append((cant, age))

# Use genders as stack names
stacks = ['male','female']

# Calculate total population size as the value for each stack identified by canton,age_group and sex
#take data group by canton afe group and sex, then sum up the pop size
stack_val = df.groupby(['canton', 'age_group', 'sex']).sum().unstack()
#print(stack_val.pop_size.Männlich.head(5))

# Build a ColumnDataSource using above information
#x_axis needs cantons and its age_groups so we take factors
#y_values are the values of the male and female population
source = ColumnDataSource(dict(
    x = factors,
    male = stack_val.pop_size.Männlich,
    female = stack_val.pop_size.Weiblich
))


### Task 2: Data Visualization


## T2.1: Visualize the data using bokeh plot functions
p=figure(x_range=FactorRange(*factors), plot_height=500, plot_width=800, title='Canton Population Visualization')
p.yaxis.axis_label = "Population Size"
p.xaxis.axis_label = "Canton"
p.sizing_mode = "stretch_both"
p.xgrid.grid_line_color = None


p.vbar_stack(stacks, x='x', width=0.9, alpha=0.5, color=['green', 'grey'], source=source,legend_label=stacks)



## T2.2 Add the hovering tooltips to the plot using HoverTool
# To be specific, the hover tooltips should display “gender”, canton, age group”, and “population” when hovering.
# https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#hovertool
# read more if you want to create fancy hover text: https://stackoverflow.com/questions/58716812/conditional-tooltip-bokeh-stacked-chart

#when hover then show gender , canton, age group, population
hover = HoverTool(tooltips=[("gender", "$name"), ("canton, age group", "@x"), ("population", "@$name")])
p.add_tools(hover)
show(p)


## T2.3 Save the plot as "dvc_ex1.html" using output_file
output_file("dvc_ex1.html")