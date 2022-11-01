# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': 'All Sites', 'value': 'ALL'},
                                                      {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                      {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                      {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                      {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                                      ],
                                             value='ALL',
                                             placeholder="Select a Launch Site",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       1000: '1000',
                                                       2000: '2000',
                                                       3000: '3000',
                                                       4000: '4000',
                                                       5000: '5000',
                                                       6000: '6000',
                                                       7000: '7000',
                                                       8000: '8000',
                                                       9000: '9000',
                                                       10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Display pie chart of successful launches for all sites
        data = spacex_df.groupby('Launch Site')['class'].sum().reset_index()

        fig = px.pie(data, values='class', names='Launch Site', title='Successful Launches')
        return fig
    else:
        # Determine number of successful (class 1) and failed (class 0) launches per site
        success = len(spacex_df[(spacex_df['Launch Site']==entered_site) & (spacex_df['class'] == 1)])
        failure = len(spacex_df[(spacex_df['Launch Site']==entered_site) & (spacex_df['class'] == 0)])
        data = pd.DataFrame({'class': ['Success', 'Failure']})
        df1 = pd.DataFrame({'Launch Status': [success, failure]})
        data['Launch Status']= df1['Launch Status']

        fig = px.pie(data, values='Launch Status', names='class',
                    title=("Launch status for site "+entered_site))
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def update_scatter_chart(entered_site, value):
    # Difine Patload RangeSLider limits
    low, high = value

    if entered_site == 'ALL':
        # Display Payload Mass vs Launch Success for all launche sites as 'scatter plot'
        data = spacex_df[['Payload Mass (kg)', 'class', 'Booster Version Category']]
        data = data[(data['Payload Mass (kg)'] >= low) & (data['Payload Mass (kg)'] <= high)]

        fig = px.scatter(data, x='Payload Mass (kg)', y='class',
                         title=('Correlation between Payload Mass (kg) and Launch Success - All sites'),
                         color=data['Booster Version Category']
                        )
        return fig
    else:
        # Display Payload Mass vs Launch Success per launch site as 'scatter plot'
        data = spacex_df[(spacex_df['Launch Site'] == entered_site)]
        data = data[['Payload Mass (kg)', 'class', 'Booster Version Category']]
        data = data[(data['Payload Mass (kg)'] >= low) & (data['Payload Mass (kg)'] <= high)]

        fig = px.scatter(data, x='Payload Mass (kg)', y='class',
                         title=('Correlation between Payload Mass (kg) and Launch Success - Site ' + entered_site),
                         color=data['Booster Version Category']
                         )
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
