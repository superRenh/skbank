import dash
from dash import html

dash.register_page(__name__, path='/', name='Home', description='Home page')

layout = html.Div([
    html.H1('Home page'),
    html.Div('This is our Home page content.'),
])