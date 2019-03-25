#import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=steward,health,boroname,spc_common,count(tree_id)' +\
        #'&$where=boroname=\'Bronx\'' +\
        '&$group=steward,health,boroname,spc_common').replace(' ', '%20')

df = pd.read_json(soql_url)

df['percentage'] = df['count_tree_id']/df['count_tree_id'].sum()

ind1 = df['boroname'].unique()
ind2 = df['spc_common'].unique()
#ind3 = df['steward'].unique()


app.layout = html.Div([
    html.Div([
        html.H1("Arborist App"),
        dcc.Markdown("""What proportion of trees are in good, fair, or poor health according to the ‘health’ variable?  """),
        
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in ind1],
                value='Manhattan'
            ),
            
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in ind2],
                value='northern red oak'
            ),
            
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    html.Div([
        dcc.Markdown("Are stewards (steward activity measured by the ‘steward’ variable) having an impact on the health of trees? "),
    dcc.Graph(id='ind-graph')
    
    
    ])
       

])


@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value')
     
     ])
def update_graph(xaxis_column_name, yaxis_column_name):
    dff = df[df['boroname'] == xaxis_column_name]
    dff = df[df['spc_common'] == yaxis_column_name]

    traces = []
    for i in dff.health.unique():
        df_h=dff[dff['health']==i]
        traces.append( go.Bar(
            x=df_h[df_h['spc_common'] == yaxis_column_name]['health'],
            y=df_h[df_h['boroname']==xaxis_column_name]['percentage'],
            text=df_h[df_h['spc_common'] == yaxis_column_name]['health'],
            name=i
           
            ))
        
            
                                 
                       

    return {
        #'data': [go.Bar(
            #x=dff[dff['spc_common'] == yaxis_column_name]['health'],
           # y=dff[dff['boroname']== xaxis_column_name]['percentage'],
            #text=dff[dff['spc_common'] == yaxis_column_name]['health'],
                   # )],
        'data':traces,
        'layout': go.Layout(
            
            xaxis={
                'title': yaxis_column_name
                
            },
            yaxis={
                'title': xaxis_column_name
                
            },
            
        )
    }


    
    


@app.callback(
    Output('ind-graph', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value')
     ])
    
def update_stwd_graph(xaxis_column_name, yaxis_column_name):
    dff = df[df['boroname'] == xaxis_column_name]
    dff = df[df['spc_common'] == yaxis_column_name]
    #dff = df[df['steward'] == stwdname]

    traces = []
    for i in dff.steward.unique():
        df_h=dff[dff['steward']==i]
        traces.append( go.Bar(
            x=df_h[df_h['boroname']==xaxis_column_name]['percentage'],
            y=df_h[df_h['spc_common']==yaxis_column_name]['percentage'],
            text=df_h['steward'],
            customdata=df_h['health'],
            
            name=i,
             #mode='lines+markers'
           
            ))
        
            
                                 
                       

    return {
        #'data': [go.Bar(
            #x=dff[dff['spc_common'] == yaxis_column_name]['health'],
           # y=dff[dff['boroname']== xaxis_column_name]['percentage'],
            #text=dff[dff['spc_common'] == yaxis_column_name]['health'],
                   # )],
        'data':traces,
        'layout': go.Layout(
            
            xaxis={
                'title': yaxis_column_name
                
            },
            yaxis={
                'title': xaxis_column_name
                
            },
            
        )
            
        
    
    }
    
    
if __name__ == '__main__':
    app.run_server(debug=True)
