""" This module contains our UI and front end code that users can interact with in order

to create and visualize routes to visit up to 6 MLB stadiums on a path.

"""

from datetime import date

from dash import Dash, html, dcc, callback, Output, Input, dash_table, no_update
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import dash_loading_spinners as dls
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

from makeRoute.exhaustiveSearch import (
    reduce_routes,
    reduce_schedule,
    sort_order,
    find_all_routes,
)

df = pd.read_csv("data/final_mlb_schedule.csv")
cost_dfx = pd.read_csv("data/cost_df.csv")

schedule = df.copy()
schedule["date"] = pd.to_datetime(schedule["date"])
# print(schedule["home team"].unique().tolist())


fig = go.Figure(
    go.Scattermapbox(
        mode="markers+lines", lon=[], lat=[], hovertext=[], marker={"size": 10}
    )
)

fig.update_layout(
    margin={"l": 0, "t": 0, "b": 0, "r": 0},
    mapbox={
        "center": {"lat": 37.0902, "lon": -95.7129},
        "style": "open-street-map",
        "zoom": 3,
    },
)

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

CONTENT_STYLE = {
    "margin-left": "22rem",
    "margin-right": "22rem",
    "padding": "2rem 1rem",
}


instructions_label = html.H5(
    "Choose up to 6 MLB teams you would like to visit this season within \
the time frame you want. \
We will create the optimal route that is optimized by time, distance or cost."
)
date_picker = dcc.DatePickerRange(
    # date range
    id="date-selection",
    min_date_allowed=date(2024, 3, 20),
    max_date_allowed=date(2024, 9, 29),
    initial_visible_month=date(2024, 3, 20),
    # end_date=date(2024, 9, 29)
    style={"margin-top": "15px"},
)
dropdown = dcc.Dropdown(
    # Shows all teams in a drop down list to choose from
    np.sort(df["home team"].unique()).tolist(),
    multi=True,
    id="dropdown-selection",
    placeholder="Select teams you wish to visit",
    style={"margin-top": "15px"},
)
metrics_label = html.H5("Optimize for: ", style={"margin-top": "15px"})
radio_items = dcc.RadioItems(
    options=[
        {"label": "Time", "value": "time"},
        {"label": "Distance", "value": "distance"},
        {"label": "Cost", "value": "cost"},
    ],
    value="time",
    id="prioritize",
    # inline=True
)
total_table = dash_table.DataTable(
    id="total_table",
    style_cell={"padding": "5px"},
    style_header={"backgroundColor": "white", "fontWeight": "bold"},
)

selection_sidebar = html.Div(
    [
        instructions_label,
        date_picker,
        dropdown,
        metrics_label,
        radio_items,
        total_table,
    ],
    style=SIDEBAR_STYLE,
)

schedule_table = dash_table.DataTable(
    id="table",
    style_cell={"padding": "5px", "margin-top": "15px"},
    style_header={"fontWeight": "bold"},
    # style_header={"backgroundColor": "white", "fontWeight": "bold",'color':'w'},
)
path = html.Div(id="image_route", children=[], style={"margin-top": "15px"})


content = html.Div(
    [
        dls.BallTriangle(dcc.Graph(figure=fig, id="graph-content")),
        schedule_table,
        path,
        dcc.Store(
            id="remaining_team_list",
            storage_type="memory",
            data=np.sort(df["home team"].unique()).tolist(),
        ),
    ],
    style=CONTENT_STYLE,
)
# , style={"margin-left": "1000px"}),
# style={'textAlign': 'center','margin':'auto'})
app.layout = html.Div(
    [
        dbc.Col(selection_sidebar, width=2),
        dbc.Col(
            [
                dbc.Row(
                    html.H1(
                        children="Baseball Traveling Fans(man)",
                        style={
                            "textAlign": "center",
                            "margin": "auto",
                            "margin-left": "270px",
                            "margin-top": "20px",
                        },
                    )
                ),
                # "padding": "2rem 1rem",
                #  'margin':'auto'}),
                dbc.Row(content),
            ],
            width=9,
        ),
    ]
)


@callback(
    [Output("dropdown-selection", "options"), Output("remaining_team_list", "data")],
    Input("dropdown-selection", "value"),
    Input("remaining_team_list", "data"),
    prevent_initial_call=True,
)
def update_dropdown(teams_selected, remaining_teams):
    """
    Updates the dropdown selections to remove teams already selected as well as not allow

    anymore selections once the user selects 6 teams.

    """

    # Limit the number of teams selected to 6
    if teams_selected is not None and len(teams_selected) > 5:
        return teams_selected, remaining_teams

    return remaining_teams, remaining_teams


@callback(
    Output("graph-content", "figure"),
    Input("dropdown-selection", "value"),
    Input("date-selection", "start_date"),
    Input("date-selection", "end_date"),
    Input("prioritize", "value"),
)
# pylint: disable=too-many-locals
def update_graph(teams, start_date, end_date, sort_method):
    """
    Updates the map and plots the new route calculated based on the parameters.

    """
    dff = df.copy()
    dff = dff.groupby("home team").first().reset_index()

    sched = df.copy()

    if teams is None or len(teams) < 2:
        sched = sched[sched["home team"].isin([])]
    else:
        teamlist = teams
        short_sched = reduce_schedule(schedule, teamlist, start_date, end_date)
        routes = find_all_routes(teamlist)
        route_df = reduce_routes(routes, short_sched, cost_dfx)
        sorted_route = sort_order(route_df, sort_method)
        sched = sorted_route["games"][0]

    team_lons = sched["Longitude"].tolist()
    team_lats = sched["Latitude"].tolist()
    team_home = sched["home team"].tolist()
    team_away = sched["away team"].tolist()
    order = list(range(len(sched)))
    order_final = []
    for x in order:
        order_final.append(str(x + 1))

    sched["date"] = pd.to_datetime(sched["date"])
    sched["date"] = sched["date"].dt.strftime("%m-%d-%Y")
    dates = sched["date"].tolist()
    time = sched["time"].tolist()
    hover_data_zipped = list(zip(team_home, team_away, dates, time))

    hover_data_format = []
    for point in hover_data_zipped:
        hover_data_format.append(
            f"{point[1]} at {point[0]} on {point[2]} at {point[3]}"
        )

    new_fig = go.Figure(
        go.Scattermapbox(
            mode="markers+lines+text",
            lon=team_lons,
            lat=team_lats,
            hovertext=hover_data_format,
            hoverinfo="text",
            text=order_final,
            textposition="top center",
            # textposition='TopCenter',
            marker={"size": 10},
        )
    )

    new_fig.update_layout(
        margin={"l": 0, "t": 0, "b": 0, "r": 0},
        mapbox={
            "center": {"lat": 37.0902, "lon": -95.7129},
            "style": "open-street-map",
            "zoom": 3,
        },
        font={
            "family": "Courier New, monospace",
            "size": 25,  # Set the font size here
            "color": "blue",
        },
    )

    return new_fig


@callback(
    Output("image_route", "children"),
    Input("table", "data"),
)
def update_image_path(table_data):
    """
    Updates the route logos below the main table.

    """

    if table_data is None or len(table_data) == 0:
        raise PreventUpdate

    new_images = []
    new_images.append(html.H5("Route: ", style={"margin-top": "15px"}))

    for team_dict_ind,team_dict in enumerate(table_data):
        if team_dict_ind != 0:
            arrow = html.Img(
                src="assets/arrow_2.png", alt='arrow', style={"width": "50px"}
            )

            new_images.append(arrow)

        team = team_dict["Home Team"]
        team = team.replace(" ", "")

        img = html.Img(src=f"assets/{team}.png", alt=team, style={"width": "100px"})
        new_images.append(img)

    return new_images


@callback(
    Output("table", "data"),
    Input("dropdown-selection", "value"),
    Input("date-selection", "start_date"),
    Input("date-selection", "end_date"),
    Input("prioritize", "value"),
)
def update_game_schedule_table(teams, start_date, end_date, sort_method):
    """
    Updates the game schedule table based on the parameters and route

    calculation.

    """
    if teams is None or len(teams) < 2:
        return no_update
    teamlist = teams
    short_sched = reduce_schedule(schedule, teamlist, start_date, end_date)
    routes = find_all_routes(teamlist)
    route_df = reduce_routes(routes, short_sched, cost_dfx)
    sorted_route = sort_order(route_df, sort_method)
    sched = sorted_route["games"][0]
    sched = sched[["date", "time", "home team", "away team"]]
    sched["date"] = sched["date"].dt.strftime("%m-%d-%Y")
    sched.columns = ["Date", "Time", "Home Team", "Away Team"]
    return sched.to_dict("records")


@callback(
    Output("total_table", "data"),
    Input("dropdown-selection", "value"),
    Input("date-selection", "start_date"),
    Input("date-selection", "end_date"),
    Input("prioritize", "value"),
)
# pylint: disable=consider-using-f-string
def update_sidebar_metrics_table(teams, start_date, end_date, sort_method):
    """
    Updates the sidebar metrics table based on the parameters and route

    calculation.

    """
    if teams is None or len(teams) < 2:
        return no_update
    teamlist = teams
    short_sched = reduce_schedule(schedule, teamlist, start_date, end_date)
    routes = find_all_routes(teamlist)

    route_df = reduce_routes(routes, short_sched, cost_dfx)
    sorted_route = sort_order(route_df, sort_method)
    metrics = ["Time", "Distance", "Travel Cost"]
    metric_val = [
        str(sorted_route["time"][0]) + " days",
        str(sorted_route["distance"][0]) + " miles",
        "${0:.2f}".format(sorted_route["cost"][0]),
    ]
    totals = pd.DataFrame({"Metric": metrics, "Total": metric_val})

    return totals.to_dict("records")


if __name__ == "__main__":
    # temp change to debug
    app.run(debug=False)
