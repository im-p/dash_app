import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
from fbprophet import Prophet
import warnings
warnings.filterwarnings("ignore")

#vpk_mittaus = pd.read_csv("vpk_mittauspaikat.csv")
#virtaama_mittaus = pd.read_csv("virtaama_mittauspaikat.csv")
vpk = pd.read_csv("https://raw.githubusercontent.com/im-p/dash_app/master/vpk_mittaukset.csv")
virtaama = pd.read_csv("https://raw.githubusercontent.com/im-p/dash_app/master/virtaama_mittaukset.csv")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=external_stylesheets)
app.title = "Hydroligiset havainnot"

server = app.server

#-------------------------------plots layout--------------------------------------------------#
plot_layout = dict(
    autosize = False,
    showlegend = True,
    legend = dict(orientation = "h"),
    height = 500,
    plot_bgcolor="#191A1A",
    paper_bgcolor="#020202",
    margin = dict(
        t = 30,
        b = 30,
        l = 30,
        r = 30,
    ),
    yaxis2 = dict(
        overlaying = "y",
        side = "right"
    )
)

#-------------------------------keys for radiobuttons, options for dropdown--------------------------------------------------#
all_options = {
    "vedenpinnankorkeus": vpk.Nimi.unique().tolist(),
    "virtaama": virtaama.Nimi.unique().tolist(),
    "All": vpk.Nimi.unique().tolist() + virtaama.Nimi.unique().tolist()
}

#-------------------------------map--------------------------------------------------#
"""
def map_trace(dataframe, value):
    df = dataframe
    trace = dict(
        type = "scattermapbox",
        lon = df.lon.unique(),
        lat = df.lat.unique(),
        text = df.Nimi,
        name = value,
        hoverinfo = "text",
        mode = "markers",
    )
    return trace

def mapbox(value):
    
    traces = []

    if value == "vedenpinnankorkeus":
        traces.append(map_trace(vpk_mittaus, value))
            
    if value == "virtaama":
        traces.append(map_trace(virtaama_mittaus, value))
        
    if value == "All":
        traces.append(map_trace(vpk_mittaus, value))
        traces.append(map_trace(virtaama_mittaus, value))
        
    layout = dict(
        legend = dict(orientation = "h"),
        title = value + " havaintopaikat",
        autosize = False,
        showlegend = True,
        width = 780,
        height = 500,
        plot_bgcolor="#191A1A",
        paper_bgcolor="#020202",
        margin = dict(
            t = 50,
            b = 30,
            l = 30,
            r = 30,
        ),
        mapbox = dict(
            accesstoken = "pk.eyJ1IjoiaWlnb3IiLCJhIjoiY2p1dHJlZmZmMGE1dzN6cGlvZXI5aXNtbiJ9.GR6TYsf5at0qVN03vF4HQQ",
            center = dict(
                lat = 64.8,
                lon = 25.72088
            ),
        style = "dark",
        zoom = 3.7,
        )
    )
    
    figure = dict(data = traces, layout = layout)
    
    return figure
""" 
#-------------------------------observation plot--------------------------------------------------#
    
def plot_trace_y2(dataframe, city):
    df = dataframe
    trace = dict(
        type = "line",
        x = df.loc[df["Nimi"] == city, "Aika"],
        y = df.loc[df["Nimi"] == city, "Arvo"],
        name = city,
        mode = "lines",
        yaxis = "y2"
    )
    return trace

def plot_trace(dataframe, city):
    df = dataframe
    trace = dict(
        type = "line",
        x = df.loc[df["Nimi"] == city, "Aika"],
        y = df.loc[df["Nimi"] == city, "Arvo"],
        name = city,
        mode = "lines",
    )
    return trace
    
def plot(Radio_selection, Dropdown_selection):
    
    dff = vpk
    df_virtaama = virtaama
    traces = []
    
    for city in Dropdown_selection:
        if Radio_selection == "vedenpinnankorkeus":
            if dff.loc[dff["Nimi"] == city, "Arvo"].mean() > 7000:
                traces.append(plot_trace_y2(vpk, city))
            else:
                traces.append(plot_trace(vpk, city))

        if Radio_selection == "virtaama":
            if df_virtaama.loc[df_virtaama["Nimi"] == city, "Arvo"].mean() > 7000:
                traces.append(plot_trace_y2(virtaama, city))
            else:
                traces.append(plot_trace(virtaama, city))

        if Radio_selection == "All":
            concat = pd.concat([vpk, virtaama])
            if concat.loc[concat["Nimi"] == city, "Arvo"].mean() > 7000:
                traces.append(plot_trace_y2(concat, city))
            else:
                traces.append(plot_trace(concat, city))
        
    
    figure2 = dict(data = traces, layout = plot_layout)
    return figure2


#-------------------------------forecasting--------------------------------------------------#

def forecast_plot(dataframe, city):
    forecast = dataframe
    trace = dict(
        type = "line",
        x = forecast.ds[-31:],
        y = forecast.yhat[-31:],
        name = city + " prediction",
    )
    return trace

def forecast_plot_y2(dataframe, city):
    forecast = dataframe
    trace = dict(
        type = "line",
        x = forecast.ds[-31:],
        y = forecast.yhat[-31:],
        name = city + " prediction",
        yaxis = "y2",
    )
    return trace

def prediction(dataframe, dataframe2, city):
    df = dataframe
    df1 = pd.DataFrame(df.loc[dataframe2["Nimi"] == city, ["ds", "y"]])
    m = Prophet(yearly_seasonality=True, daily_seasonality=True)
    m.fit(df1)
    future = m.make_future_dataframe(30)
    forecast = m.predict(future)
    return forecast

def prediction_plot(Radio_selection, Dropdown_selection):
    
    traces = []
    dff = vpk.copy()
    dff.drop(["Paikka_Id", "KuntaNimi", "Nimi"],1,inplace=True)
    dff.columns = ["ds", "y"]
    dfff = vpk.copy()
    
    df_virtaama = virtaama.copy()
    df_virtaama.drop(["Paikka_Id", "KuntaNimi", "Nimi"],1,inplace=True)
    df_virtaama.columns = ["ds", "y"]
    dff_virtaama = virtaama.copy()
    
    
    for city in Dropdown_selection:
        if Radio_selection == "vedenpinnankorkeus":
            if prediction(dff, dfff, city).yhat.mean() > 7000:
                traces.append(plot_trace_y2(vpk, city))
                traces.append(forecast_plot_y2(prediction(dff, dfff, city), city))
            else:
                traces.append(plot_trace(vpk, city))
                traces.append(forecast_plot(prediction(dff, dfff, city), city))
                
        if Radio_selection == "virtaama":
            if prediction(df_virtaama, dff_virtaama, city).yhat.mean() > 100:
                traces.append(plot_trace_y2(virtaama, city))
                traces.append(forecast_plot_y2(prediction(df_virtaama, dff_virtaama, city), city))
            else:
                traces.append(plot_trace(virtaama, city))
                traces.append(forecast_plot(prediction(df_virtaama, dff_virtaama, city), city))        
            
    figure3 = dict(data = traces, layout = plot_layout)
    return figure3

#-------------------------------update data--------------------------------------------------#



#-------------------------------layout--------------------------------------------------#
app.layout = html.Div([
        #--container--
        html.Div([
            
            #--"header"--
            html.Div([
                html.H1("Hydrologiset Havainnot", style = {'text-align': 'center'}),
            ], className = "row"), #--header loppu--
            
            #-------------------------------dcc items--------------------------------------------------#
            
            #--dropdown/radio--
            html.Div([
                
                html.Div([
                dcc.RadioItems(id = "Radio",
                        options = [{"label": i, "value": i} for i in all_options.keys()],
                        labelStyle={'display': 'inline-block'},
                        value = "vedenpinnankorkeus"),
                    ], className = "six columns"),
                
                html.Div([
                    dcc.Dropdown(id = "Dropdown", multi = True, value = "")], className = "six columns")
                    
            ], className = "row", style = {"margin-top": "20"}), #--dropdown/radio loppu--
            
            html.Hr(),
            
             #----------------------------------map/plot-----------------------------------------------#
            
            html.Div([
                #--map--
                html.Div([
                    dcc.Graph(id = "my-map", config = {"scrollZoom": True})
                ], className = "seven columns"),
                
                #--plot--
                html.Div([
                    dcc.Graph(id='plot')
                ], className = "five columns"),
            
            ], className = "row", style = {'margin-top': '20'}),
        
         #----------------------------------prediction/table-----------------------------------------------#
             html.Div([
                    html.H2("Ennusteet", style = {"textAlign": "center"})
                ], className = "row"),
            
            html.Div([
                #--prediction--
                html.Div([
                    dcc.Graph(id = "prediction-plot", style = {"background": "black"})
                ], className = "twelve columns"),
                
            ], className = "row", style = {'background': 'black'}),
            
            html.Hr(),
        #--------------------------------footer-------------------------------------------------# 
        
        #--footer--
        html.Div([
            html.P("Hydroligiset havainnot / Lähde: SYKE, ELY-keskukset",
                  className = "ten columns", style = {"margin-left":"15"}),
            
        #--kuva--
            html.Img(
                src = "https://www.jamk.fi/globalassets/tietoa-jamkista--about-jamk/materiaalit-esitteet-asiakaslehdet-ja-logot/jamkin-logot/jamk_fi--tunnus/jamkfi_tunnus_sininen_suomi.png",
                className = "two columns",
                style = {"width": "10%", "height": "10%"}
            ),
            
        ], className = "row", style = {'margin-top': '20'}) #--footer loppu--
            
        #---------------------------------------------------------------------------------#
            
    ], className = "twelve columns"), #--container loppu--
    dcc.Interval(
        id = "interval",
        interval = 86400000,
        n_intervals = 0
    )
], className = "ten columns offset-by-one", style={'height': 'auto', "background":"black", 'boxShadow': '0px 0px 5px 5px white'}) #--layout end--#


#--------------------------------dropdown options-------------------------------------------------# 
@app.callback(
    Output("Dropdown", "options"),
    [Input("Radio", "value")])

def update_dropdown(selected):
    return [{"label": i, "value": i} for i in all_options[selected]] 
#------------------------------map---------------------------------------------------# 
"""
@app.callback(
    Output("my-map", "figure"),
    [Input("Radio", "value")])
"""
def update_map(value):
    return mapbox(value)
#----------------------------------plot-----------------------------------------------#
@app.callback(
    Output("plot", "figure"),
    [Input("Radio", "value"),
    Input("Dropdown", "value")])

def update_plot(Radio_selection, Dropdown_selection):
    return plot(Radio_selection, Dropdown_selection)
#-------------------------------prediction--------------------------------------------------#
@app.callback(
    Output("prediction-plot", "figure"),
    [Input("Radio", "value"),
    Input("Dropdown", "value")])

def update_prediction_plot(Radio_selection, Dropdown_selection):
    return prediction_plot(Radio_selection, Dropdown_selection)

if __name__ == "__main__":
    app.run_server()