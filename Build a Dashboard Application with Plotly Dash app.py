# Import required libraries
import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create 'Success' / 'Failure' flag for pie charts
my_list = []  
for each in spacex_df['class']:
    if each == 1:
        my_list.append('Success')
    else:
        my_list.append('Failed')
        
spacex_df['class_name'] = my_list

# specify mark values for range slider
mark_values = {0:'0', 1000:'1000', 2000:'2000', 3000:'3000', 4000:'4000', 5000:'5000',
                6000:'6000', 7000:'7000', 8000:'8000', 9000:'9000', 10000:'10000'}

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                                {'label': 'All Sites', 'value': 'ALL'},{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}, {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            ],
                                    value='ALL',
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(children=[],id='success-pie-chart'),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks=mark_values,
                                    value=[min_payload, max_payload]
                                    ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(children=[], id='success-payload-scatter-chart'),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'children'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):

    if entered_site == 'ALL':
        df = spacex_df
        pie_fig = px.pie(df, names='Launch Site', values='class', title='Proportion of Total Successful launches by Launch Site')
    else:
        df = spacex_df[spacex_df['Launch Site'] == entered_site]
        df['count'] = 1
        pie_fig = px.pie(df, names='class_name', values='count', title='Proportion of Successful & Failed launches for: {}'.format(entered_site))

    return dcc.Graph(figure=pie_fig)  

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'children'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')
)
def get_scatter_chart(site_selection, payload_selection):

    df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_selection[0]) & (spacex_df['Payload Mass (kg)'] <= payload_selection[1])]

    if site_selection == 'ALL':
        scatter_fig = px.scatter(data_frame=df, x='Payload Mass (kg)', y='class', title='Correlation between Payload and Success for All Sites',
                                color='Booster Version Category')
    else:
        df = df[df['Launch Site'] == site_selection]
        scatter_fig = px.scatter(data_frame=df, x='Payload Mass (kg)', y='class', title=f'Correlation between Payload and Success for: {site_selection}',
                                color='Booster Version Category')
    return dcc.Graph(figure=scatter_fig)

# Run the app
if __name__ == '__main__':
    app.run_server()

"""

    Which site has the largest successful launches?
        - VAFB SLC-4E: 9600kg
    Which site has the highest launch success rate?
        - KSC LC-39A: 77%
    Which payload range(s) has the highest launch success rate?
        - 3000-4000kg: 5 successful launches
    Which payload range(s) has the lowest launch success rate?
        - 
    Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest


"""


