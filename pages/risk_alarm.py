import pandas as pd
import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go

def alarm_rule(df):
    value = df['Value']
    if value > 0:
            return 1
    else:
        return 0
def generate_parent(df):
    if df['Label'] == '風險警示':
        return ''
    else:
        return '風險警示'
def data_preprocessing(column_of_risk, SAMASTER_SAR_PATH):
    df_samaster_sar = pd.read_csv(SAMASTER_SAR_PATH).drop_duplicates()
    df_samaster_sar_feature = df_samaster_sar[["ACC_RANDOM", "SNAP_DATE", "SAMST_CUST_STAT", "SAMST_OD_STAT", "SAMST_TXN_STOP_STAT","SAMST_COURT_STAT", "SAMST_WARN_STAT", "SAMST_OD_OV_STAT", "SAMST_WASH_DB_OV_FLAG", "SAMST_WASH_CR_OV_FLAG"]]
    df_samaster_sar_feature[column_of_risk] = df_samaster_sar_feature[column_of_risk].astype(int)
    df_samaster_sar_feature["ACC_RANDOM"] = df_samaster_sar_feature["ACC_RANDOM"].astype(str)
    df_samaster_sar_feature["SNAP_DATE"] = df_samaster_sar_feature["SNAP_DATE"].apply(lambda x: x.split(" ")[0])
    df_samaster_sar_feature['SNAP_DATE'] = pd.to_datetime(df_samaster_sar_feature['SNAP_DATE'],format='%Y-%m-%d')
    # sum up all the columns value except ACC_RANDOM, SNAP_DATE
    df_samaster_sar_feature["風險警示"] = len(column_of_risk)
    # Convert the DataFrame from wide to long format
    df_long = df_samaster_sar_feature.melt(id_vars=['ACC_RANDOM', 'SNAP_DATE'], var_name='Label', value_name='Value').sort_values(by=['ACC_RANDOM', 'SNAP_DATE'])
    df_long['Alarm'] = df_long.apply(alarm_rule, axis=1)
    df_long['Parent'] = df_long.apply(generate_parent, axis=1)
    return df_samaster_sar_feature, df_long

# Define the layout
def create_layout(df_long):
    layout = html.Div([
        html.H1("台幣活期帳戶檔警示平台"),
        
        dcc.Graph(id='treemap-chart'),
        
        html.Label("Filter by ACC_RANDOM:"),
        dcc.Dropdown(
            id='acc-random-dropdown',
            options=[
                {'label': f'ACC_RANDOM {acc}', 'value': acc} for acc in df_long['ACC_RANDOM'].unique()
            ],
            value=df_long['ACC_RANDOM'].iloc[0],
            style={'color': 'Black', 'width': '250px'}
        ),
        # DatePickerSingle for selecting a specific date
        dcc.DatePickerSingle(
            id='date-picker-single',
            date=unique_dates[0],  # Set the initial date
            display_format='YYYY-MM-DD',
            persistence=True,
            persistence_type='local',
        )
        
    ])
    return layout


def update_treemap_chart(selected_acc_random, selected_date):
    # Filter the DataFrame by selected ACC_RANDOM value
    selected_date = str(selected_date)
    df_long['SNAP_DATE'] = df_long['SNAP_DATE'].astype(str)
    filtered_df = df_long[(df_long['ACC_RANDOM'] == str(selected_acc_random)) & (df_long['SNAP_DATE'] == selected_date)]
    # Define colors based on values
    colors = ['white' if label == '風險警示' else 'LightPink' if value > 0 else 'LightGray' for label, value in zip(filtered_df['Label'], filtered_df['Value'])]

    # Create a Treemap chart using Plotly
    fig = go.Figure(go.Treemap(
        labels=filtered_df['Label'],
        parents=filtered_df['Parent'],
        text=filtered_df['Value'],
        # values=df['Value'],
        # textinfo='label+text',  # Display both label and value at the center
        textinfo='label',  # Display both label and value at the center
        textfont=dict(size=48),   # Adjust the font size
        # textposition='middle center',  # Center the text
        marker_colors=colors    
        ))
    
    fig.update_layout(
        margin=dict(t=0, l=0, r=0, b=0),
    )
    
    return fig

column_of_risk = ["SAMST_CUST_STAT", "SAMST_OD_STAT", "SAMST_TXN_STOP_STAT","SAMST_COURT_STAT", "SAMST_WARN_STAT", "SAMST_OD_OV_STAT", "SAMST_WASH_DB_OV_FLAG", "SAMST_WASH_CR_OV_FLAG"]
SAMASTER_SAR_PATH = "./Data/SAMASTER_SAR.csv"
df_samaster_sar_feature, df_long = data_preprocessing(column_of_risk, SAMASTER_SAR_PATH)
# Get unique date values
unique_dates = df_samaster_sar_feature['SNAP_DATE'].unique()
layout = create_layout(df_long)
# Initialize the Dash app
dash.register_page(__name__, name='風險警示平台', description='風險警示平台')

# Define callback to update the Treemap chart
@callback(
    Output('treemap-chart', 'figure'),
    [Input('acc-random-dropdown', 'value'),
     Input('date-picker-single', 'date')]
)
def update(selected_acc_random, selected_date):
    return update_treemap_chart(selected_acc_random, selected_date)