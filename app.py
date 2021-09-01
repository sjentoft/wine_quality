import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# read in data
wine = pd.read_csv("wine_all.csv", delimiter = ",")
wine["wine color"] = wine["color_text"]

# set up App
app = dash.Dash(__name__)
server = app.server
app.title = "Wine quality and price"


# Layout
app.layout = html.Div(
    children=[
        
        # Title
        html.H1("Wine quality and price", 
                className="text-center",
                style = {'font-family': 'Arial', 
                         'color': "rgb(211,211,211)",
                         'background-color': "rgb(93, 113, 120)",
                         'border': '20px double rgb(93, 113, 120)',
                         'textAlign': 'center'
                       }),
        
        # Variable select dropdown
        html.Div(
            children=[
                # Select variable
                html.B("Select variable:"),
                dcc.Dropdown(id='x_var', clearable=False, 
                                 value='fixed acidity', 
                                 options=[
                                     {'label': c, 'value': c} for c in wine.columns[np.r_[1:12, 16]]
                                 ]
                            ),
                # Radio button
                html.Br(),
                html.B("Filter data:"),
                dcc.RadioItems(id = 'data_filter',
                           labelStyle = {"display": "block"},
                           value = 'Portugal',
                           options = [{'label': "All", 'value': "All"}, 
                                      {'label': "Portugal", 'value': "Portugal"},
                                      {'label': "Vinmonopol", 'value': "Vinmonopol"}]
                              ),
                # Colour by box
                html.Br(),
                html.B("Color by:"),
                dcc.RadioItems(id = 'color_by',
                           labelStyle = {"display": "block"},
                           value = 'wine color',
                           options = [ 
                                      {'label': "Data source", 'value': "source"},
                                      {'label': "Wine colour", 'value': "wine color"},
                                      {'label': "None", 'value': "drop"}]
                              ),
                
                # Trendline box
                html.Br(),
                dcc.Checklist(id = 'trend_check',
                    options=[ 
                    {'label': 'Include trendline', 'value': 'ols'}
                    ],
                    value=['ols']
                ) 
                
            ], style = {'width' : '15%', 
                        'display': 'inline-block',
                       'vertical-align': 'top',
                        'font-family': 'Helvetica Neue', 
                       }
        ),
        
        
            
        # Scatterplot
        html.Div(
            dcc.Graph(id="graph_scatter",
                     style={'width': '800'}), 
            style={'display': 'inline-block',
                  'width':'43%'}
        ),
        
        # Histogram
        html.Div(
            dcc.Graph(id="graph_hist",
                     style={'width': '800'}), 
            style={'display': 'inline-block',
                  'width':'42%'}
        )
               
    ], className="container-fluid"
)


# Define callback to update graph
@app.callback(
    Output('graph_scatter', 'figure'),
    [Input("x_var", "value"), 
     Input("trend_check", "value"), 
     Input("data_filter", "value"),
     Input("color_by", "value")]
)
def update_figure(x_var, trend_check, data_filter, color_by):
    
    # filter data
    filt = [data_filter]
    if filt == ["All"]:
        filt = ["Portugal", "Vinmonopol"]
    wine_set = wine[wine.source.isin(filt)]
    
    # plot figure with trendline
    farge = ["#00958A", "#940D07"]
    if color_by == "drop":
        color_by = None
        farge = ["#9063CD"]
    if trend_check != ['ols']:
        trend_check = None
    else:
        trend_check = trend_check[0]

    fig = px.scatter(
        wine_set, x=x_var, y="quality", 
        color = color_by,
        color_discrete_sequence=farge,
        opacity = 0.5,
        render_mode="webgl",
        trendline=trend_check)
    fig.update_layout(showlegend=False)
    
    return fig
    

@app.callback(
    Output('graph_hist', 'figure'),
    [Input("x_var", "value"),
     Input("data_filter", "value"),
     Input("color_by", "value")
    ]
)
def update_bar(x_var, data_filter, color_by):
    # filter data
    filt = [data_filter]
    if filt == ["All"]:
        filt = ["Portugal", "Vinmonopol"]
    wine_set = wine[wine.source.isin(filt)]
    farge = ["#00958A", "#940D07"]
    if color_by == "drop":
        color_by = None
        farge = ["#9063CD"]
    return px.histogram(wine_set, x=x_var,
                        color = color_by, 
                        barmode="overlay",
                        color_discrete_sequence=farge#,
                        #showlegend = False
                        )

# Run app and display result inline in the notebook
#app.run_server(mode='inline')
if __name__ == '__main__':
    app.run_server()
