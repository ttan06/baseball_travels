from dash import Dash, html, dcc, callback, Output, Input, dash_table, no_update
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from datetime import date
# from makeRoute.makeRoute import route_creator#, game_finder, schedule_builder
from makeRoute.exhaustiveSearch import reduce_routes, reduce_schedule, sort_order, find_all_routes

df = pd.read_csv('data/final_mlb_schedule.csv')
cost_dfx = pd.read_csv('data/cost_df.csv')

schedule = df.copy()
schedule['date'] = pd.to_datetime(schedule['date'])
print(schedule['home team'].unique().tolist())

# Original graph with no paths added
fig = go.Figure(go.Scattermapbox(
    mode="markers+lines",
    lon=[],
    lat=[],
    hovertext=[],
    marker={'size': 10}))

fig.update_layout(
    margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
    mapbox={
        'center': {'lat': 37.0902, 'lon': -95.7129},
        'style': "open-street-map",
        'zoom': 3})

app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
# sidebar = html.Div(
#     [
#         html.H2("Sidebar", className="display-4"),
#         html.Hr(),
#         html.P(
#             "A simple sidebar layout with navigation links", className="lead"
#         ),
#         dbc.Nav(
#             [
#                 dbc.NavLink("Home", href="/", active="exact"),
#                 dbc.NavLink("Page 1", href="/page-1", active="exact"),
#                 dbc.NavLink("Page 2", href="/page-2", active="exact"),
#             ],
#             vertical=True,
#             pills=True,
#         ),
#     ],
#     style=SIDEBAR_STYLE,
# )
CONTENT_STYLE = {
    "margin-left": "22rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

selection_sidebar = html.Div([
    dash_table.DataTable(id='total_table'),
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
        np.sort(df['home team'].unique()),
        multi=True,
        id='dropdown-selection',
        placeholder="Select teams you wish to visit"),
    dcc.RadioItems(
        options=[
            {'label': 'Time', 'value': 'time'},
            {'label': 'Distance', 'value': 'distance'},
            {'label': 'Cost', 'value': 'cost'},
        ],
        value='Time',
        id='prioritize',
        inline=True
    )
],
    style=SIDEBAR_STYLE, )

content = html.Div([dcc.Graph(figure=fig, id='graph-content'),
                    dash_table.DataTable(id='table')]
                   , style=CONTENT_STYLE)

app.layout = html.Div([html.H1(children='Baseball Travel', style={'textAlign': 'center'}),
                       selection_sidebar, content
                       ])


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('date-selection', 'start_date'),
    Input('date-selection', 'end_date'),
    Input('prioritize', 'value')
)
# Updates graph based on the selection from the drop down list
def update_graph(teams, start_date, end_date, sort_method):
    dff = df.copy()
    dff = dff.groupby('home team').first().reset_index()

    sched = df.copy()

    # if value is not None:
    #     # dff = dff[dff['home team'].isin(value)]
    # else :
    #     # dff = dff[dff['home team'].isin([]])]

    if teams is None:

        sched = sched[sched['home team'].isin([])]
    elif len(teams) < 2:
        sched = sched[sched['home team'].isin([])]
    else:
        teamlist = teams  # ['Texas Rangers', 'Colorado Rockies', 'Baltimore Orioles', 'Detroit Tigers', 'Minnesota Twins', 'St. Louis Cardinals', 'Tampa Bay Rays']
        # r1 = route_creator(schedule, teamlist, start_date, end_date, 1)
        short_sched = reduce_schedule(schedule, teamlist, start_date, end_date)
        routes = find_all_routes(teamlist)
        route_df = reduce_routes(routes, short_sched, cost_dfx)
        sorted_route = sort_order(route_df, sort_method)
        sched = sorted_route['games'][0]

    team_lons = sched['Longitude'].tolist()
    team_lats = sched['Latitude'].tolist()
    team_home = sched['home team'].tolist()
    team_away = sched['away team'].tolist()
    order = list(range(len(sched)))
    order_final = []
    for x in order:
        order_final.append(str(x + 1))

    sched['date'] = pd.to_datetime(sched['date'])
    sched['date'] = sched['date'].dt.strftime('%m-%d-%Y')
    dates = sched['date'].tolist()
    time = sched['time'].tolist()
    hover_data_zipped = list(zip(team_home, team_away, dates, time))

    hover_data_format = []
    for point in hover_data_zipped:
        hover_data_format.append(f'{point[1]} at {point[0]} on {point[2]} at {point[3]}')

    fig = go.Figure(go.Scattermapbox(
        mode="markers+lines+text",
        lon=team_lons,
        lat=team_lats,
        hovertext=hover_data_format,
        hoverinfo="text",
        text=order_final,
        textposition='top center',
        # textposition='TopCenter',
        marker={'size': 10}))

    fig.update_layout(
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
            'center': {'lat': 37.0902, 'lon': -95.7129},
            'style': "open-street-map",
            'zoom': 3},
        font=dict(
            family="Courier New, monospace",
            size=25,  # Set the font size here
            color="RebeccaPurple")
    )

    team_to_image_map = {
        'San Diego Padres': "", 'Chicago Cubs': "", 'Los Angeles Dodgers': "",
        'Texas Rangers': "", 'Colorado Rockies': "",
        'Baltimore Orioles': "https://upload.wikimedia.org/wikipedia/commons/e/e9/Baltimore_Orioles_Script.svg",
        'Detroit Tigers': "", 'Minnesota Twins': "", 'St. Louis Cardinals': "",
        'Tampa Bay Rays': "", 'Toronto Blue Jays': "", 'New York Mets': "",
        'Chicago White Sox': "", 'Cleveland Guardians': "", 'Kansas City Royals': "",
        'Oakland Athletics': "", 'San Francisco Giants': "", 'Los Angeles Angels': "",
        "Arizona D'Backs": "https://loodibee.com/wp-content/uploads/mlb-arizona-diamondbacks-logo.png",
        'Washington Nationals': "", 'Atlanta Braves': "", 'Boston Red Sox': "",
        'Pittsburgh Pirates': "", 'Philadelphia Phillies': "", 'Houston Astros': "",
        'New York Yankees': "", 'Miami Marlins': "", 'Cincinnati Reds': "", 'Milwaukee Brewers': "",
        'Seattle Mariners': "",
    }

    for x_ind, y_ind, team in sched[["Longitude", "Latitude", "home team"]].values:
        fig.add_layout_image(
            dict(
                source=team_to_image_map[team],
                # xref="x domain",
                # yref="y domain",
                # xanchor="right",
                # yanchor="top",
                x=1,
                y=1,
                # sizex=2,
                # sizey=2,
                # sizing="contain",
                # opacity=1.0,
                layer="above",
            )
            # layout=go.Layout(
            #                 xaxis =  {
            #                     'showgrid': False
            #                          },
            #                 yaxis = {
            #                    'showgrid': True
            #                         })
            # ),
        )

    return fig


@callback(
    Output('table', 'data'),
    Input('dropdown-selection', 'value'),
    Input('date-selection', 'start_date'),
    Input('date-selection', 'end_date'),
    Input('prioritize', 'value')
)
def update_table(teams, start_date, end_date, sort_method):
    if teams is None:
        return no_update
    elif len(teams) < 2:
        return no_update
    teamlist = teams  # ['Texas Rangers', 'Colorado Rockies', 'Baltimore Orioles', 'Detroit Tigers', 'Minnesota Twins', 'St. Louis Cardinals', 'Tampa Bay Rays']
    # r1 = route_creator(schedule, teamlist, start_date, end_date, 1)
    # g1 = game_finder(schedule, r1[0], start_date, end_date)
    short_sched = reduce_schedule(schedule, teamlist, start_date, end_date)
    routes = find_all_routes(teamlist)
    route_df = reduce_routes(routes, short_sched, cost_dfx)
    sorted_route = sort_order(route_df, sort_method)
    sched = sorted_route['games'][0]
    sched = sched[['date', 'time', 'away team', 'home team']]
    sched['date'] = sched['date'].dt.strftime('%m-%d-%Y')
    return sched.to_dict("records")


@callback(
    Output('total_table', 'data'),
    Input('dropdown-selection', 'value'),
    Input('date-selection', 'start_date'),
    Input('date-selection', 'end_date'),
    Input('prioritize', 'value')
)
def update_table(teams, start_date, end_date, sort_method):
    if teams is None:
        return no_update
    elif len(teams) < 2:
        return no_update
    teamlist = teams  # ['Texas Rangers', 'Colorado Rockies', 'Baltimore Orioles', 'Detroit Tigers', 'Minnesota Twins', 'St. Louis Cardinals', 'Tampa Bay Rays']
    # r1 = route_creator(schedule, teamlist, start_date, end_date, 1)
    # g1 = game_finder(schedule, r1[0], start_date, end_date)
    short_sched = reduce_schedule(schedule, teamlist, start_date, end_date)
    routes = find_all_routes(teamlist)
    route_df = reduce_routes(routes, short_sched, cost_dfx)
    sorted_route = sort_order(route_df, sort_method)
    metrics = ['Time', 'Distance', 'Travel Cost']
    metric_val = [str(sorted_route['time'][0]) + ' days', str(sorted_route['distance'][0]) + ' miles',
                  '${0:.2f}'.format(sorted_route['cost'][0])]
    totals = pd.DataFrame({'Metric': metrics, 'Total': metric_val})

    return totals.to_dict("records")


if __name__ == '__main__':
    app.run(debug=False)
