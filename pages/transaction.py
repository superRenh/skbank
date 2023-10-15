import pandas as pd
import dash
from dash import dcc, html, Input, Output, callback, State, ALL
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc


# data preprocessing functions
def remove_comma_str(number_str):
    if ',' in number_str:
        number_str = number_str.replace(',', '')
    return number_str
def standard_txn_time(time_int):
    time_str = str(time_int).zfill(6)
    return f"{time_str[:2]}:{time_str[2:4]}:{time_str[4:]}"

def data_preprocessing(SATXNREC_SAR_PATH, SAMASTER_SAR_PATH):
    df_satxnrec_sar = pd.read_csv(SATXNREC_SAR_PATH).drop_duplicates()
    df_satxnrec_sar_plot = df_satxnrec_sar[["ACC_RANDOM", "SATXN_BUSI_DATE", "SATXN_TXN_TIME", "SATXN_TXN_AMT", "SATXN_DB_CR_STAT"]]
    df_satxnrec_sar_plot["ACC_RANDOM"] = df_satxnrec_sar_plot["ACC_RANDOM"].astype(str)
    df_satxnrec_sar_plot["ACC_RANDOM"] = df_satxnrec_sar_plot["ACC_RANDOM"].apply(remove_comma_str)
    df_satxnrec_sar_plot["SATXN_BUSI_DATE"] = df_satxnrec_sar_plot["SATXN_BUSI_DATE"].apply(lambda x: x.split(" ")[0])
    df_satxnrec_sar_plot["SATXN_TXN_TIME"] = df_satxnrec_sar_plot["SATXN_TXN_TIME"].apply(standard_txn_time)
    df_satxnrec_sar_plot["SATXN_TXN_DATETIME"] = df_satxnrec_sar_plot["SATXN_BUSI_DATE"] + " " + df_satxnrec_sar_plot["SATXN_TXN_TIME"]
    df_satxnrec_sar_plot["SATXN_TXN_AMT"] = df_satxnrec_sar_plot["SATXN_TXN_AMT"].apply(remove_comma_str)
    df_satxnrec_sar_plot["SATXN_TXN_AMT"] = df_satxnrec_sar_plot["SATXN_TXN_AMT"].astype(float)
    df_satxnrec_sar_plot["SATXN_TXN_AMT_DIR"] = df_satxnrec_sar_plot.apply(lambda x: float(x["SATXN_TXN_AMT"]) *(-1) if x["SATXN_DB_CR_STAT"]==1 else float(x["SATXN_TXN_AMT"]), axis=1)
    df_satxnrec_sar_plot = df_satxnrec_sar_plot[["ACC_RANDOM", "SATXN_TXN_DATETIME", "SATXN_TXN_AMT_DIR", "SATXN_TXN_AMT"]]

    df_samaster_sar = pd.read_csv(SAMASTER_SAR_PATH).drop_duplicates()
    df_samaster_sar_plot = df_samaster_sar[["ACC_RANDOM", "SNAP_DATE", "SAMST_BAL"]]
    df_samaster_sar_plot["SNAP_DATE"] = df_samaster_sar_plot["SNAP_DATE"].apply(lambda x: x.split(".")[0])
    df_samaster_sar_plot["ACC_RANDOM"] = df_samaster_sar_plot["ACC_RANDOM"].astype(str)
    df_samaster_sar_plot["SAMST_BAL"] = df_samaster_sar_plot["SAMST_BAL"].astype(float)

    # Create a DataFrame
    df = df_satxnrec_sar_plot
    df_histogram = df_samaster_sar_plot
    # Convert the date column to datetime
    df['SATXN_TXN_DATETIME'] = pd.to_datetime(df['SATXN_TXN_DATETIME'])
    df_histogram["SNAP_DATE"] = pd.to_datetime(df_histogram["SNAP_DATE"])
    return df, df_histogram

# Define the layout
def create_layout(df):
    layout = html.Div([
        # dcc.Link('Go to home page', href='/'),
        html.H1("交易資料與餘額資料儀表板"),
        html.P("透過了解客戶的交易行為和帳戶餘額的變動情況，有助於銀行同仁追踪和管理資金流動。"),
        html.Ul([html.Li("橫軸代表時間，縱軸表示金額"),
                html.Li("交易數據:\n使用不同顏色和大小的點來表示每次的交易金額。正值（位於X軸以上,貸方交易）代表金錢轉入，而負值（位於X軸以下,借方交易）代表金錢轉出。\n點的大小則代表交易的金額，較大的點表示較大筆的交易。", style={'white-space': 'pre-line'}),
                html.Li("帳戶餘額:\n用紅色的折線圖表示，它展示了隨著時間的進行，帳戶餘額是如何變化的。從圖中可以看到，每次交易後，無論是轉入還是轉出，都會影響到帳戶的餘額。", style={'white-space': 'pre-line'})]),
        html.Br(),
        dcc.Graph(id='time-series-plot'),
        
        html.Label("篩選帳號流水編號"),
        dcc.Dropdown(
            id='acc-random-dropdown',
            options=[
                {'label': f'帳號流水編號: {acc}', 'value': acc} for acc in df['ACC_RANDOM'].unique()
            ],
            value=df['ACC_RANDOM'].iloc[0],
            style={'color': 'Black', 'width': '250px'}
        )
    ])
    
    return layout

# Define the callback function
def update_time_series_plot(selected_acc_random, df, df_histogram):
    filtered_df = df[df['ACC_RANDOM'] == selected_acc_random]
    fig = px.scatter(
        filtered_df,
        x='SATXN_TXN_DATETIME',
        y='SATXN_TXN_AMT_DIR',
        color='SATXN_TXN_AMT_DIR',
        size='SATXN_TXN_AMT',
        labels={'SATXN_BUSI_DATETIME': 'Date and Time', 'SATXN_TXN_AMT_DIR': 'SATXN_TXN_AMT'}
    )

    # Filter the histogram data by selected ACC_RANDOM
    filtered_df_histogram = df_histogram[df_histogram['ACC_RANDOM'] == selected_acc_random]

    # Create the filled histogram as a filled scatter plot with transparency
    fig.add_trace(go.Scatter(
        x=filtered_df_histogram['SNAP_DATE'],
        y=filtered_df_histogram['SAMST_BAL'],
        fill='tozeroy',
        fillcolor='rgba(173, 216, 230, 0.5)',  # Set the fill color to light blue with opacity
        name='Histogram'
    ))

    # Add a red dashed line at y=0
    fig.add_shape(
        type='line',
        x0=filtered_df_histogram['SNAP_DATE'].min(),
        x1=filtered_df_histogram['SNAP_DATE'].max(),
        y0=0,
        y1=0,
        line=dict(color='black', dash='dash')
    )

    fig.update_layout(title=f"Transaction Data for ACC_RANDOM {selected_acc_random}")

    return fig

# Load data and preprocess it
SATXNREC_SAR_PATH = "./Data/SATXNREC_SAR.csv"
SAMASTER_SAR_PATH = "./Data/SAMASTER_SAR.csv"
df, df_histogram = data_preprocessing(SATXNREC_SAR_PATH, SAMASTER_SAR_PATH)
dash.register_page(__name__, name='Transaction Data Dashboard', description='This is a dashboard for transaction data.')
layout = create_layout(df)

@callback(
    Output('time-series-plot', 'figure'),
    Input('acc-random-dropdown', 'value')
    )
def update(selected_acc_random):
    return update_time_series_plot(selected_acc_random, df, df_histogram)