from dash import Dash, html, dcc, Input, Output
import altair as alt
import pandas as pd

# Read in global data
character_matrix = pd.read_csv('characters_stats.csv')
dropdown = ["Intelligence", "Strength",	"Speed", "Durability", "Power", "Combat"]

# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server
app.layout = html.Div([
    html.Iframe(
        id='scatter',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    html.Div([
        "Dropdown for x axis:",
        dcc.Dropdown(
        id='xcol-widget',
        value='Intelligence',  # REQUIRED to show the plot on the first page load
        options=[{'label': col, 'value': col} for col in dropdown],
        placeholder='Select x axis...')
    ]),
    html.Div([
        "Dropdown for y axis:",
        dcc.Dropdown(
        id='ycol-widget',
        value='Strength',
        options=[{'label': col, 'value': col} for col in dropdown],
        placeholder='Select y axis...')
    ]),
    html.Div([
        "Slide to change the size of the points",
        dcc.Slider(id='slider', min=10, max=100, step=10, value=10)
    ])
    ])

# Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xcol-widget', 'value'),
    Input('ycol-widget', 'value'),
    Input('slider', 'value'))

def plot_altair(xcol, ycol, dot_size):
    
    if xcol and ycol:
        chart = alt.Chart(character_matrix).mark_point().encode(
            x=xcol,
            y=ycol,
            color='Alignment',
            tooltip=['Name', 'Total']).properties(
                title="Scatter plot of Marvel Heroes matrix"
                ).interactive(
            ).configure_point(
                size=dot_size
            )
        return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)