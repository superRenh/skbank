import os
import dash
import glob
import dash_table
from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Define AI model prediction result
TW_data = [
{"Accuracy": "95.63%", "Recall": "71.03%", "Precision": "60.06%"}
]
FR_data = [
{"Accuracy": "99.88%", "Recall": "94.38%", "Precision": "100.00%"}
]
# Define the columns for the table
columns = [{"name": col, "id": col} for col in ["Accuracy", "Recall", "Precision"]]

# Define risk level 
risk_level = {"high": 0.3, "middle": 0.1}

# Define the layout
def create_layout(result_filename_filepath):
    layout = html.Div([
        html.H1("AI 模型成效"),
        html.P("訓練2個異常交易行為識別AI模型，分別為偵測台幣帳戶異常與偵測外幣帳戶異常。透過 AI 模型，我們能夠即時地判斷交易行為是否為異常交易，並且能夠提供帳戶的風險等級。"),
        html.H3("台幣帳戶異常偵測 AI 模型成效", style={'color': 'lightblue'}),
        dash_table.DataTable(
        id='TW-model-result-table',
        columns=columns,
        data=TW_data,
        style_cell={'textAlign': 'center', 'fontSize': 18},
        style_header={'backgroundColor': 'rgb(100, 150, 150)', 'color': 'white', 'fontSize': 18},
        style_table={'width': '50%'}
        ),
        html.Br(),
        html.H3("外幣帳戶異常偵測 AI 模型成效", style={'color': 'lightblue'}),
        dash_table.DataTable(
        id='FR-model-result-table',
        columns=columns,
        data=FR_data,
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
            value=list(result_filename_filepath.keys())[-1],
            style={'color': 'Black', 'width': '250px'}
        ),
        dcc.Graph(id='sunburst-chart', style={'margin-bottom': '0px'}),
        dcc.Graph(id='risk-level-high-table', style={'margin-top': '0px', 'margin-bottom': '0px'}),
        dcc.Graph(id='risk-level-middle-table', style={'margin-top': '0px', 'margin-bottom': '0px'}),
        dcc.Graph(id='risk-level-low-table', style={'margin-top': '0px'})
    ])
    return layout

def update_sunburst_chart(selected_predict_date):
    _, _, _, risk_level_proportion, risk_level_count=model_prediction_risk_level(selected_predict_date, risk_level)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=['風險等級'],
        x=[risk_level_count[0]],
        name='high risk',
        orientation='h',
        marker=dict(
            color='rgba(246, 78, 139, 0.6)',
            line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
        ),
        text=[f'high risk {risk_level_proportion[0]}%'],  # Add text label here
        textposition='inside',  # Adjust the position of the text label ('inside' or 'outside')
        textfont=dict(size=20),  # Adjust the font size of the text label
        textangle=0,
    ))
    fig.add_trace(go.Bar(
        y=['風險等級'],
        x=[risk_level_count[1]],
        name='middle risk',
        orientation='h',
        marker=dict(
            color='rgba(255, 255, 80, 0.6)',
            line=dict(color='rgba(255, 255, 80, 1.0)', width=3)
        ),
        text=[f'middle risk {risk_level_proportion[1]}%'],  # Add text label here
        textposition='inside',  # Adjust the position of the text label ('inside' or 'outside')
        textfont=dict(size=20),  # Adjust the font size of the text label
        textangle=0,
    ))
    fig.add_trace(go.Bar(
        y=['風險等級'],
        x=[risk_level_count[2]],
        name='low risk',
        orientation='h',
        marker=dict(
            color='rgba(0, 128, 0, 0.6)',
            line=dict(color='rgba(0, 128, 0, 1.0)', width=3)
        ),
        text=[f'low risk {risk_level_proportion[2]}%'],  # Add text label here
        textposition='inside',  # Adjust the position of the text label ('inside' or 'outside')
        textfont=dict(size=20),  # Adjust the font size of the text label
        textangle=0,
    ))
    fig.update_layout(barmode='stack')
    fig.update_layout(title=f"AI模型預測日期: {selected_predict_date}<br>high risk:{risk_level_count[0]}, middle risk:{risk_level_count[1]}, low risk:{risk_level_count[2]}")
    
    return fig

def update_risk_level_table(selected_predict_date):
    df_high, df_middle, df_low, _, _ = model_prediction_risk_level(selected_predict_date, risk_level)

    # Create data for the three tables
    high_table = go.Figure(data=[go.Table(
        header=dict(values=list(df_high.columns), fill_color='rgba(246, 78, 139, 0.8)', align='left'),
        cells=dict(values=[df_high.ACC_RANDOM, df_high.Probability], fill_color='rgba(211,211,211,0.5)', align='left')
    )],layout=go.Layout(margin=dict(t=50, b=0)))

    middle_table = go.Figure(data=[go.Table(
        header=dict(values=list(df_middle.columns), fill_color='rgba(255, 255, 80, 0.8)', align='left'),
        cells=dict(values=[df_middle.ACC_RANDOM, df_middle.Probability], fill_color='rgba(211,211,211,0.5)', align='left')
    )], layout=go.Layout(margin=dict(t=50, b=0)))

    low_table = go.Figure(data=[go.Table(
        header=dict(values=list(df_low.columns), fill_color='rgba(0, 128, 0, 0.8)', align='left'),
        cells=dict(values=[df_low.ACC_RANDOM, df_low.Probability], fill_color='rgba(211,211,211,0.5)', align='left')
    )], layout=go.Layout(margin=dict(t=50, b=0)))

    # Update the layout and return the figures
    high_table.update_layout(title=f"高度風險帳戶列表")
    middle_table.update_layout(title=f"中度風險帳戶列表")
    low_table.update_layout(title=f"低度風險帳戶列表")

    return high_table, middle_table, low_table

def model_prediction_risk_level(selected_predict_date, risk_level):
    df = pd.read_csv(result_filename_filepath[selected_predict_date])
    df['risk_level'] = df['Probability'].apply(lambda x: 'high' if x >= risk_level['high'] else 'middle' if x >= risk_level['middle'] else 'low')
    df_high = df[df['risk_level'] == 'high'].drop(columns=['risk_level'])
    df_middle = df[df['risk_level'] == 'middle'].drop(columns=['risk_level'])
    df_low = df[df['risk_level'] == 'low'].drop(columns=['risk_level'])
    risk_level_proportion = [round(len(df_high)/len(df),2)*100, 
                             round(len(df_middle)/len(df),2)*100, 
                             round(len(df_low)/len(df),2)*100]
    risk_level_count = [len(df_high), len(df_middle), len(df_low)]
    return df_high, df_middle, df_low, risk_level_proportion, risk_level_count

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
def update(selected_predict_date):
    return update_sunburst_chart(selected_predict_date)

@callback(
    Output('risk-level-high-table', 'figure'),
    Output('risk-level-middle-table', 'figure'),
    Output('risk-level-low-table', 'figure'),
    Input('model-result-dropdown' , 'value')
)
def update(selected_predict_date):
    return update_risk_level_table(selected_predict_date)