# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import geopandas as gpd
import flask

server = flask.Flask(__name__)
app = Dash(__name__,server=server)
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

optionslist = ['C1_COUNT_TOTAL', 'C2_COUNT_MEN+',
    'C3_COUNT_WOMEN+',  'C10_RATE_TOTAL',
 'C11_RATE_MEN+', 'C12_RATE_WOMEN+']

geo_df = gpd.read_file('CEN_CENSUS_DIVISIONS_SVW.geojson').set_index('CENSUS_DIVISION_NAME')
bc = pd.read_csv('bc.csv')
bc = bc[bc['CHARACTERISTIC_NAME'] == "Unemployment rate"]
geo_df['CENSUS_DIVISION_ID'] = pd.to_numeric(geo_df['CENSUS_DIVISION_ID'])
geo_df = geo_df.merge(bc, how='left', right_on='ALT_GEO_CODE', left_on='CENSUS_DIVISION_ID')
# geo_df = geo_df.rename({'C10_RATE_TOTAL':'Unemployment Rate'}, axis=1)


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}



# fig = px.choropleth_mapbox(geo_df,
#                            geojson=geo_df.geometry,
#                            locations=geo_df.index,
#                            center={"lat": 54.108560, "lon": -125.024922},
#                            color='C10_RATE_TOTAL',
#                            mapbox_style='stamen-toner',
#                            zoom=5,
#                            opacity=0.3)
#54.108560, -125.024922

# fig.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
# )

fig2 = px.scatter(geo_df, x="FEATURE_AREA_SQM", y="C10_RATE_TOTAL",
                 size="FEATURE_AREA_SQM", color="CENSUS_YEAR_y", hover_name="CENSUS_DIVISION_ID",
                 log_x=True, size_max=60)


app.layout = html.Div(children=[
    html.H1(children='Map Example'),

    html.Div(children='''
        This is intended to show how we can add maps to containers.
    '''),

    html.Div(children=[
        html.Label('Dropdown'),
        dcc.Dropdown(optionslist, 'C10_RATE_TOTAL',id='rateselector'),
    ], style={'padding': 10, 'flex': 1, 'width':'15vw'}),
html.Div(children=[
    dcc.Graph(
        id='map',
        # figure=fig,
        style={'width': '45vw', 'height': '90vh'}
    ),

    dcc.Graph(
        id='bubble graph',
        # figure=fig2,
        style={'width': '45vw', 'height': '90vh'}
    )],style={'display': 'block'}
)
])

@app.callback(
    Output('map', 'figure'),
    Input('rateselector', 'value')
)
def update_map(rateselector):
    fig = px.choropleth_mapbox(geo_df,
                           geojson=geo_df.geometry,
                           locations=geo_df.index,
                           center={"lat": 54.108560, "lon": -125.024922},
                           color=rateselector,
                           mapbox_style='stamen-toner',
                           zoom=5,
                           opacity=0.3)
    return fig

@app.callback(
    Output('bubble graph', 'figure'),
    Input('rateselector', 'value')
)
def update_map(rateselector):
    fig2 = px.scatter(geo_df, x="FEATURE_AREA_SQM", y=rateselector,
                 size="FEATURE_AREA_SQM", color="CENSUS_YEAR_y", hover_name="CENSUS_DIVISION_ID",
                 log_x=True, size_max=60)
    return fig2

if __name__ == '__main__':
    app.run_server(debug=True)