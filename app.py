from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('data/final_mlb_schedule.csv')

# Original graph with no paths added
fig = go.Figure(go.Scattermapbox(
    mode = "markers+lines",
    lon = [],
    lat = [],
    hovertext=[],
    marker = {'size': 10}))

fig.update_layout(
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'center': {'lat': 37.0902, 'lon': -95.7129},
        'style': "open-street-map",
        'zoom': 3})

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Baseball Travel', style={'textAlign':'center'}),
    dcc.Dropdown(
        # Shows all teams in a drop down list to choose from
        df['home team'].unique(),
        multi=True, 
        id='dropdown-selection',
        placeholder="Select teams you wish to visit"),
    dcc.Graph(figure=fig,id='graph-content')])



@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
# Updates graph based on the selection from the drop down list
def update_graph(value):
    dff = df.copy()
    dff = dff.groupby('home team').first().reset_index()

    if value is not None :
        dff = dff[dff['home team'].isin(value)]
    else :
        dff = dff[dff['home team'].isin([])]

    
    team_lons = dff['Longitude'].tolist()
    team_lats = dff['Latitude'].tolist()
    team_home = dff['home team'].tolist()
    team_away = dff['away team'].tolist()
    dates = dff['date'].tolist()
    hover_data_zipped = list(zip(team_home,team_away,dates))

    hover_data_format = []
    for point in hover_data_zipped :
        hover_data_format.append(f'{point[1]} at {point[0]} on {point[2]}')



    fig = go.Figure(go.Scattermapbox(
        mode = "markers+lines",
        lon = team_lons,
        lat = team_lats,
        hovertext=hover_data_format,
        hoverinfo="text",
        marker = {'size': 10}))

    fig.update_layout(
        margin ={'l':0,'t':0,'b':0,'r':0},
        mapbox = {
            'center': {'lat': 37.0902, 'lon': -95.7129},
            'style': "open-street-map",
            'zoom': 3})
    return fig

if __name__ == '__main__':
    app.run(debug=True)
