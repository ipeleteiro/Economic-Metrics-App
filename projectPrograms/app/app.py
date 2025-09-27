import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# initialising a multipage app with the stylesheet theme SPACELAB
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])

menu = dbc.Nav(
            # creating a menu to access every page
            [
                dbc.NavLink(                                      # navlink with the name and path asigned in each file
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",    # highlights active page in menu
                )
                for page in dash.page_registry.values()           # this is done for every page in the registry
            ],
            vertical=False,
            pills=True,
            className="bg-light",
)



app.layout = dbc.Container([
    # title of the page
    dbc.Row([
        dbc.Col(html.Div("Colour Coded Maps",
                         style={'fontSize':50, 'textAlign':'center'}))
    ]),

    html.Hr(),  # line break
    dbc.Row([
        menu
    ]),
    html.Hr(),

    dbc.Row([
        dash.page_container
    ])
], fluid=True)


if __name__ == "__main__":
    app.run(debug=True)