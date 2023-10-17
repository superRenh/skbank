import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, ClientsideFunction, State

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SOLAR])

server = app.server

# Define the CSS style for the entire page
page_style = {
    'margin': '20px'  # Adjust margin as needed (e.g., '20px' top/right/bottom/left)
}

# Create a list of options for the dropdown menu
dropdown_options = [
    {'label': f"{page['name']} - {page['description']}", 'value': page['relative_path']}
    for page in dash.page_registry.values() if page['name'] != 'Home' and page['name'] != 'Fraud Detection AI Model' and page['name'] != 'alert notification'
]

app.layout = html.Div([
    html.H1(['新光銀行異常交易行為偵測平台', dbc.Badge("Digital Finance Sentinel", className="ms-1")]),
    html.Div(
        [
            dbc.Button("Home Page", href="/", color="primary"),
            dbc.Button("Fraud Detection AI Model", href="/ai_model", color="warning"),
            dbc.Button("Alert Notification", href="/alert_notification", color="danger")
        ]   
        ),
        
    # Create a dropdown menu for page selection
    dcc.Dropdown(
        id='page-dropdown',
        options=dropdown_options,
        value=None,  # Set an initial value of None
        clearable=False,  # Prevent clearing the dropdown selection
        style={'color': 'Black'}
    ),
    html.Br(),
    # Create a div to display the selected page
    html.Div(id='selected-page-content'),
    dash.page_container
],style=page_style)

# Define a callback to display the selected page
@app.callback(
    dash.Output('selected-page-content', 'children'),
    [dash.Input('page-dropdown', 'value')]
)
def display_selected_page(selected_page):
    if selected_page:
        return dcc.Location(pathname=selected_page, id='page-location')


if __name__ == '__main__':
    app.run(debug=True)