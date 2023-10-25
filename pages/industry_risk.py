import pandas as pd
import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go

def data_preprocessing(CFMASTER_PATH, CFMASTER_SAR_PATH):
    df = pd.read_csv(CFMASTER_PATH).drop_duplicates()
    df_sar = pd.read_csv(CFMASTER_SAR_PATH).drop_duplicates()
    df_cfmst_bins_code = df["CFMST_BINS_CODE_JCIC"].astype(str)
    df_sar_cfms_bins_code = df_sar["CFMST_BINS_CODE_JCIC"].astype(str)
    df_cfmst_bins_code_count = df_cfmst_bins_code.value_counts()
    x_cfmst = df_cfmst_bins_code_count.index.tolist()
    y_cfmst = df_cfmst_bins_code_count.values.tolist()
    df_cfmst_bins_code_count_sar = df_sar_cfms_bins_code.value_counts()
    x_cfmst_sar = df_cfmst_bins_code_count_sar.index.tolist()
    y_cfmst_sar = df_cfmst_bins_code_count_sar.values.tolist()
    return x_cfmst, y_cfmst, x_cfmst_sar, y_cfmst_sar

# Define the layout
def create_layout(fig, fig_sar):
    layout = html.Div([
        html.H1("Industry distribution"),
        dcc.Graph(figure=fig),
        dcc.Graph(figure=fig_sar)
    ])
    return layout

# Define the callback function
def update_bar_plot(x, y, type, color='lightblue'):
    # Create a Plotly bar trace
    trace = go.Bar(
        x=x,
        y=y,
        marker=dict(color=color)  # Customize the bar color
    )
    fig = go.Figure(data=[trace])
    
    fig.update_layout(title=dict(text=f"行業別數量分佈圖({type})", font=dict(color=color)), xaxis_title="行業別", yaxis_title="數量")
    return fig

# Load data and preprocess it
x_cfmst, y_cfmst, x_cfmst_sar, y_cfmst_sar = data_preprocessing('./Data/CFMASTER.csv', './Data/CFMASTER_SAR.csv')
dash.register_page(__name__, name='Industry distribution', description='This is a dashboard for Industry distribution.')
fig = update_bar_plot(x_cfmst, y_cfmst, '非SAR帳戶')
fig_sar = update_bar_plot(x_cfmst_sar, y_cfmst_sar, 'SAR帳戶', 'lightpink')
layout = create_layout(fig, fig_sar)