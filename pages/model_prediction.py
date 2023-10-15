import os
import dash
import glob
import dash_table
from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.graph_objects as go

# Define AI model prediction result
data = [
{"Accuracy": "95.91%", "Recall": "67.39%", "Precision": "63.44%"}
]
# Define the columns for the table
columns = [{"name": col, "id": col} for col in ["Accuracy", "Recall", "Precision"]]


# Define the layout
def create_layout(result_filename_filepath):
    layout = html.Div([
        html.H1("AI 模型成效"),
        html.P("訓練2個異常交易行為識別AI模型，分別為偵測台幣帳戶異常與偵測外幣帳戶異常。透過 AI 模型，我們能夠即時地判斷交易行為是否為異常交易，並且能夠提供帳戶的風險等級。"),
        html.H3("台幣帳戶異常偵測 AI 模型成效", style={'color': 'lightblue'}),
        dash_table.DataTable(
        id='sample-table',
        columns=columns,
        data=data,
        style_cell={'textAlign': 'center', 'fontSize': 18},
        style_header={'backgroundColor': 'rgb(100, 150, 150)', 'color': 'white', 'fontSize': 18},
        style_table={'width': '50%'}
        ),
        html.Br(),
        html.H3("外幣帳戶異常偵測 AI 模型成效", style={'color': 'lightblue'}),
        dash_table.DataTable(
        id='sample-table',
        columns=columns,
        data=data,
        style_cell={'textAlign': 'center', 'fontSize': 18},
        style_header={'backgroundColor': 'rgb(100, 150, 150)', 'color': 'white', 'fontSize': 18},
        style_table={'width': '50%'}
        ),
        html.Br(),
        html.H1("風險等級分佈"),
        html.P("風險等級分佈圖，能夠讓管理者快速了解所有帳戶的風險等級分佈，並且能夠透過圖表的互動功能，查看不同風險等級的異常帳戶數量。"),
        html.Div("篩選日期"),
        dcc.Dropdown(
            id='model-result-dropdown',
            options=[
                {'label': f'日期: {version}', 'value': version} for version in result_filename_filepath.keys()
            ],
            value=1,
            style={'color': 'Black', 'width': '250px'}
        ),
        dcc.Graph(id='sunburst-chart')
    ])
    return layout

def update_sunburst_chart(selected_acc_random):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=['風險等級'],
        x=[20],
        name='high risk',
        orientation='h',
        marker=dict(
            color='rgba(246, 78, 139, 0.6)',
            line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
        ),
        text=['high risk 50%'],  # Add text label here
        textposition='inside',  # Adjust the position of the text label ('inside' or 'outside')
        textfont=dict(size=20),  # Adjust the font size of the text label
        textangle=0,
    ))
    fig.add_trace(go.Bar(
        y=['風險等級'],
        x=[12],
        name='middle risk',
        orientation='h',
        marker=dict(
            color='rgba(255, 255, 80, 0.6)',
            line=dict(color='rgba(255, 255, 80, 1.0)', width=3)
        ),
        text=['middle risk 40%'],  # Add text label here
        textposition='inside',  # Adjust the position of the text label ('inside' or 'outside')
        textfont=dict(size=20),  # Adjust the font size of the text label
        textangle=0,
    ))
    fig.add_trace(go.Bar(
        y=['風險等級'],
        x=[5],
        name='low risk',
        orientation='h',
        marker=dict(
            color='rgba(0, 128, 0, 0.6)',
            line=dict(color='rgba(0, 128, 0, 1.0)', width=3)
        ),
        text=['low risk 10%'],  # Add text label here
        textposition='inside',  # Adjust the position of the text label ('inside' or 'outside')
        textfont=dict(size=20),  # Adjust the font size of the text label
        textangle=0,
    ))
    fig.update_layout(barmode='stack')
    return fig

# Define model result period
model_prediction_dir = "./model_prediction"
result_filename_filepath={os.path.basename(file).split('.')[0]: file for file in glob.glob(os.path.join(model_prediction_dir, "*.csv"))}

layout = create_layout(result_filename_filepath)
# Initialize the Dash app
dash.register_page(__name__,  path='/ai_model', name='Fraud Detection AI Model', description='Fraud Detection AI Model')

@callback(
    Output('sunburst-chart', 'figure'),
    Input('model-result-dropdown' , 'value')
)
def update(selected_acc_random):
    return update_sunburst_chart(selected_acc_random)

