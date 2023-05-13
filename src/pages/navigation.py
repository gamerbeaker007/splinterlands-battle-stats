import logging

from aio import ThemeSwitchAIO
from dash import html, Output, Input, callback, dcc, State
import dash_bootstrap_components as dbc

from src import battle_store, collection_store
from src.configuration import config
from src.pages import main_page, page1, page2
from src.utils import store_util

PLOTLY_LOGO = 'https://d36mxiodymuqjm.cloudfront.net/website/icons/img_icon_splinterlands.svg'

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height='30px')),
                        dbc.Col(dbc.NavbarBrand('SPL Battle statistics', className='ms-2')),
                    ],
                    align='center',
                    className='g-0',
                ),
                href='/',
                style={'textDecoration': 'none'},
            ),
            dbc.Col(
                dbc.NavbarSimple(
                    children=[
                        dbc.NavItem(dbc.NavLink('Home', href='/')),
                        dbc.NavItem(dbc.NavLink('Page 1', href='/page1')),
                        dbc.NavItem(dbc.NavLink('Page 2', href='/page2')),
                    ],
                    brand_href='/',
                ),
            ),
            dbc.Col(
                ThemeSwitchAIO(aio_id="theme", themes=[dbc.themes.MINTY, dbc.themes.CYBORG]),
                width='auto'),
            dbc.Col(
                dbc.Button(
                    'Pull new data',
                    id='load-new-values',
                    color='primary',
                    className='ms-2', n_clicks=0
                ),
                width='auto',
            ),
            html.Div(id='hidden-div', style={'display': 'none'}),
            html.Div(id='hidden-div1', style={'display': 'none'}),

        ]),
)

layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content', children=[]),
])


@callback(Output('page-content', 'children'),
          [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return main_page.layout
    if pathname == '/page1':
        return page1.layout
    if pathname == '/page2':
        return page2.layout
    else:  # if redirected to unknown link
        return '404 Page Error! Please choose a link'


@callback(
    Output('hidden-div1', 'children'),
    Input('load-new-values', 'n_clicks'),
)
def update_output(n_clicks):
    logging.info(n_clicks)
    collection_store.update_collection()
    battle_store.process_battles()

    store_util.save_stores()


@callback(
    Output('hidden-div', 'children'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value'),
)
def generate_chart(toggle):
    config.theme = 'minty' if toggle else 'cyborg'