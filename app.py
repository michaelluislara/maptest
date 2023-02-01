# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import geopandas as gpd
import flask

server = flask.Flask(__name__)
app = Dash(__name__,server=server)
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

geo_df = gpd.read_file('CEN_CENSUS_DIVISIONS_SVW.geojson').set_index('CENSUS_DIVISION_NAME')
bc = pd.read_csv('bc.csv')
bc = bc[bc['CHARACTERISTIC_NAME'] == "Unemployment rate"]
geo_df['CENSUS_DIVISION_ID'] = pd.to_numeric(geo_df['CENSUS_DIVISION_ID'])
geo_df = geo_df.merge(bc, how='left', right_on='ALT_GEO_CODE', left_on='CENSUS_DIVISION_ID')


fig = px.choropleth_mapbox(geo_df,
                           geojson=geo_df.geometry,
                           locations=geo_df.index,
                           center={"lat": 54.108560, "lon": -125.024922},
                           color='C10_RATE_TOTAL',
                           mapbox_style='stamen-toner',
                           zoom=5,
                           opacity=0.3)
#54.108560, -125.024922


app.layout = html.Div(children=[
    html.H1(children='Map Example'),

    html.Div(children='''
        This is intended to show how we can add maps to containers.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig,
        style={'width': '95vw', 'height': '90vh'}
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)