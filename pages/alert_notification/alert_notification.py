import dash
import json
import os
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

# Initialize the list of emails
email_list = []

# Check if the JSON file exists and load its content
json_file = "./pages/alert_notification/emails.json"
if os.path.exists(json_file):
    with open(json_file, "r") as file:
        email_list = json.load(file)

def generate_email_divs(emails):
    if emails is None:
        return []
    
    email_divs = []
    for i, email in enumerate(emails):
        email_div = html.Div([
            email,
            # html.Button(f"Delete", id={"type": "email-delete-button", "index": i}, n_clicks=0),
            dbc.Button(f"Delete", id={"type": "email-delete-button", "index": i}, n_clicks=0, color="warning", outline=True),
            html.Br(),
        ])
        email_divs.append(email_div)
    return email_divs

def create_layout(email_list):
    layout = html.Div([
        html.H1("Fraud Detection AI Model Alert Notification"),
        html.P("經 AI 模型識別異常交易行為帳戶(申報 SAR 帳戶)後，即時並發送 email 給相關查調人員，加速警示作業，提高業務 運作的效率，並增強成功攔阻詐騙效率，保護客戶安全性。\n請輸入 email 以接收警示通知:", 
               style={'white-space': 'pre-line'}),
        # html.Label("Enter Email:"),
        dcc.Input(id="email-input", type="text", placeholder="Enter Email"),
        # html.Button("Add Email", id="submit-button", n_clicks=0),
        dbc.Button("Add Email", color="info", id="submit-button", n_clicks=0),
        html.Br(),
        html.Br(),
        html.H2("示警 Email 清單", style={'color': 'lightblue'}),
        html.Div(id="email-list", children=generate_email_divs(email_list)),
    ])
    return layout

layout = create_layout(email_list)
# Initialize the Dash app
dash.register_page(__name__,  path='/alert_notification', name='alert notification', description='Email list of alert notification')

@callback(
    Output("email-list", "children"),
    Output("email-input", "value"),
    [Input("submit-button", "n_clicks"),
     Input({"type": "email-delete-button", "index": dash.dependencies.ALL}, "n_clicks")],
    [State("email-input", "value"),
     State("email-list", "children")]
)
def update_email_list(submit_n_clicks, delete_clicks, email_value, email_divs):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if "submit-button" in triggered_id and email_value:
        email_list.append(email_value)
        with open(json_file, "w") as file:
            json.dump(email_list, file)
        return generate_email_divs(email_list), ""
    elif "email-delete-button" in triggered_id:
        index = json.loads(triggered_id)["index"]
        del email_list[index]
        with open(json_file, "w") as file:
            json.dump(email_list, file)
        return generate_email_divs(email_list), email_value
    else:
        return email_divs, email_value



# if __name__ == '__main__':
#     app.run_server(debug=True)
