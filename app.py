from turtle import color
from dash import Dash, html, dcc, Input, Output
import altair as alt
from numpy import character
import pandas as pd
from vega_datasets import data


# Read in global data
character_matrix = pd.read_csv('data/characters_stats.csv')
dropdown = ["Intelligence", "Strength",	"Speed", "Durability", "Power", "Combat"]

# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div([
    html.Iframe(
        id='scatter',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    dcc.Dropdown(
        id='xcol-widget',
        value='Intelligence',  # REQUIRED to show the plot on the first page load
        options=[{'label': col, 'value': col} for col in dropdown],
        placeholder='Select x axis...'),
    dcc.Dropdown(
        id='ycol-widget',
        value='Strength', 
        options=[{'label': col, 'value': col} for col in dropdown],
        placeholder='Select y axis...')])

# Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xcol-widget', 'value'),
    Input('ycol-widget', 'value'))
def plot_altair(xcol, ycol):
    if xcol and ycol:
        chart = alt.Chart(character_matrix).mark_point().encode(
            x=xcol,
            y=ycol,
            color='Alignment',
            tooltip=['Name', 'Total']).properties(
                title="Scatter plot of Marvel Heroes matrix"
                ).interactive()
        return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)