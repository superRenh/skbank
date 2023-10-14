import dash
from dash import Dash, html, dcc, Input, Output, ClientsideFunction, State

app = Dash(__name__, use_pages=True)
server = app.server


# app.layout = html.Div([
#     html.H1('新光銀行金流異常偵測系統'),
#     html.Div([
#         html.Div(
#             dcc.Link(f"{page['name']} - {page['description']}", href=page["relative_path"])
#         ) for page in dash.page_registry.values()
#     ]),
#     dash.page_container
# ])

# Create a list of options for the dropdown menu
dropdown_options = [
    {'label': f"{page['name']} - {page['description']}", 'value': page['relative_path']}
    for page in dash.page_registry.values() if page['name'] != 'Home'
]

app.layout = html.Div([
    html.H1('新光銀行金流異常偵測系統'),
    html.Div(
            dcc.Link("Home page", href="/")
        ),
        
    # Create a dropdown menu for page selection
    dcc.Dropdown(
        id='page-dropdown',
        options=dropdown_options,
        value=None,  # Set an initial value of None
        clearable=False  # Prevent clearing the dropdown selection
    ),
    
    # Create a div to display the selected page
    html.Div(id='selected-page-content'),
    dash.page_container
])

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