from dash import Dash, html, dcc, callback, Output, Input, dash_table, no_update
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import date
from makeRoute.makeRoute import route_creator, game_finder, schedule_builder

df = pd.read_csv('data/final_mlb_schedule.csv')

schedule = df.copy()
schedule['date'] = pd.to_datetime(schedule['date'])

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
    dcc.DatePickerRange(
        # date range
        id='date-selection',
        min_date_allowed=date(2024, 3, 20),
        max_date_allowed=date(2024, 9, 29),
        initial_visible_month=date(2024, 3, 20),
        # end_date=date(2024, 9, 29)
    ),
    dcc.Dropdown(
        # Shows all teams in a drop down list to choose from
        df['home team'].unique(),
        multi=True, 
        id='dropdown-selection',
        placeholder="Select teams you wish to visit"),

    dcc.Graph(figure=fig,id='graph-content'),
    dash_table.DataTable(id = 'table')
    ])



@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('date-selection', 'start_date'),
    Input('date-selection', 'end_date')
)
# Updates graph based on the selection from the drop down list
def update_graph(value, start_date, end_date):
    dff = df.copy()
    dff = dff.groupby('home team').first().reset_index()

    sched = df.copy()

    # if value is not None:
    #     # dff = dff[dff['home team'].isin(value)]
    # else :
    #     # dff = dff[dff['home team'].isin([]])]

    if value is None:

        sched = sched[sched['home team'].isin([])]
    elif len(value) < 3:
        sched = sched[sched['home team'].isin([])]
    else :
        teamlist = value  # ['Texas Rangers', 'Colorado Rockies', 'Baltimore Orioles', 'Detroit Tigers', 'Minnesota Twins', 'St. Louis Cardinals', 'Tampa Bay Rays']
        r1 = route_creator(schedule, teamlist, start_date, end_date, 1)
        g1 = game_finder(schedule, r1[0], start_date, end_date)
        sched = (schedule_builder(g1, r1[0]))

    team_lons = sched['Longitude'].tolist()
    team_lats = sched['Latitude'].tolist()
    team_home = sched['home team'].tolist()
    team_away = sched['away team'].tolist()
    dates = sched['date'].tolist()
    time = sched['time'].tolist()
    hover_data_zipped = list(zip(team_home,team_away,dates,time))

    hover_data_format = []
    for point in hover_data_zipped :
        hover_data_format.append(f'{point[1]} at {point[0]} on {point[2]} at {point[3]}')



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

@callback(
    Output('table', 'data'),
    Input('dropdown-selection', 'value'),
    Input('date-selection', 'start_date'),
    Input('date-selection', 'end_date')
)

def update_table(value, start_date, end_date):
    if value is None:
        return no_update
    elif len(value) < 3:
        return no_update
    teamlist = value  # ['Texas Rangers', 'Colorado Rockies', 'Baltimore Orioles', 'Detroit Tigers', 'Minnesota Twins', 'St. Louis Cardinals', 'Tampa Bay Rays']
    r1 = route_creator(schedule, teamlist, start_date, end_date, 1)
    g1 = game_finder(schedule, r1[0], start_date, end_date)
    sched = (schedule_builder(g1, r1[0]))
    sched = sched[['date', 'time', 'away team', 'home team']]
    return sched.to_dict("records")

if __name__ == '__main__':
    app.run(debug=True)
