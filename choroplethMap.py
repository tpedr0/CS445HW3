# imports necessary libraries
import dash
import pandas as pd
import plotly.express as px
import json
from dash import dcc, html
from dash.dependencies import Input, Output, ALL

# loads our transformed data
df = pd.read_csv('filteredTaxData2021.csv')

# makes sure 'item' becomes a column with state codes as rows
df = df.melt(id_vars='item', var_name='State', value_name='Value')

# drop the extra columns generated in our data clean up/filtering
df = df[~df['State'].isin(['number_of_zeroes', 'number_of_NaNs'])]

# loads our state population data gathered from the U.S. Census
pop_df = pd.read_csv('statePopulations2021.csv')

# transposes the population DataFrame to long format
pop_df = pop_df.melt(id_vars='item', var_name='State', value_name='Population')
pop_df = pop_df[pop_df['item'] == 'population'].drop(columns=['item'])


# perform a merge
df = df.merge(pop_df, on='State', how='left')

# calculates tax collected per capita
df['ValuePerCapita'] = df['Value'] / df['Population']

# initializes the dash app
app = dash.Dash(__name__)

# defines item for each map
map1_items = ['T10', 'T12', 'T13', 'T16']
map2_items = ['T19', 'T23', 'T24', 'T28']

# creates two lists of buttons, one for each map
buttons_map1 = html.Div(
    [html.Button(i, id={'type': 'map1-btn', 'index': i}, n_clicks=0, style={'margin': '10px'}) for i in map1_items],
    style={'textAlign': 'center'}
)
buttons_map2 = html.Div(
    [html.Button(i, id={'type': 'map2-btn', 'index': i}, n_clicks=0, style={'margin': '10px'}) for i in map2_items],
    style={'textAlign': 'center'}
)

# defines layout of the application
app.layout = html.Div([
    html.Div([
        html.H1(id='title-map1', children='Map Title 1', style={'textAlign': 'center'}),
        buttons_map1,
        dcc.Graph(id='choropleth-map1'),
    ], style={'display': 'inline-block', 'width': '49%', 'verticalAlign': 'top'}),
    html.Div([
        html.H1(id='title-map2', children='Map Title 2', style={'textAlign': 'center'}),
        buttons_map2,
        dcc.Graph(id='choropleth-map2'),
    ], style={'display': 'inline-block', 'width': '49%', 'verticalAlign': 'top'}),
])

# maps the item codes to descriptions (used for map titles)
item_descriptions = {
    'T10': 'Alcoholic Beverages Sales Tax (T10)',
    'T12': 'Insurance Premiums Sales Tax (T12)',
    'T13': 'Motor Fuels Sales Tax (T13)',
    'T16': 'Tobacco Products Sales Tax (T16)',
    'T19': 'Other Selective Sales and Gross Receipts Taxes (T19)',
    'T23': 'Hunting and Fishing License (T23)',
    'T24': 'Motor Vehicles License (T24)',
    'T28': 'Occupation and Businesses License, NEC (T28)',
}


# callback that selects the first map based on selection
@app.callback(
    [Output('choropleth-map1', 'figure'), Output('title-map1', 'children')],
    [Input({'type': 'map1-btn', 'index': ALL}, 'n_clicks')]
)
def update_map1(*args):
    # determines what button was clicked last
    ctx = dash.callback_context
    item_clicked = 'T10'  # default item when the page loads
    if ctx.triggered:
        button_id = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])
        item_clicked = button_id['index']

    # filters data based on selected item and calculates the max value for coloring
    filtered_df = df[df['item'] == item_clicked]
    max_value = filtered_df[filtered_df['State'] != 'US']['ValuePerCapita'].max()
    scale_max = max_value * 1.2

    # creates choropleth map
    title = item_descriptions.get(item_clicked, 'Unknown Tax Item')
    fig = px.choropleth(
        filtered_df,
        locations='State',
        color='ValuePerCapita',
        locationmode='USA-states',
        scope="usa",
        color_continuous_scale="darkmint",
        range_color=[0, scale_max],
        labels={'ValuePerCapita': 'Tax Collected per Capita (USD) '}
    )
    fig.update_layout(
        title_text=title,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_colorbar={
            'title': f"<b>{item_clicked}</b>",
            }
    )
    return fig, title


# callback that selects the first map based on selection
@app.callback(
    [Output('choropleth-map2', 'figure'), Output('title-map2', 'children')],
    [Input({'type': 'map2-btn', 'index': ALL}, 'n_clicks')]
)
def update_map2(*args):
    # determines what button was clicked last
    ctx = dash.callback_context
    item_clicked = 'T19'  # default item when the page loads
    if ctx.triggered:
        button_id = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])
        item_clicked = button_id['index']

    # filters data based on selected item and calculates the max value for coloring
    filtered_df = df[df['item'] == item_clicked]
    max_value = filtered_df[filtered_df['State'] != 'US']['ValuePerCapita'].max()
    scale_max = max_value * 1.2

    # creates choropleth map
    title = item_descriptions.get(item_clicked, 'Unknown Tax Item')
    fig = px.choropleth(
        filtered_df,
        locations='State',
        color='ValuePerCapita',
        locationmode='USA-states',
        scope="usa",
        color_continuous_scale="darkmint",
        range_color=[0, scale_max],
        labels={'ValuePerCapita': 'Tax Collected per Capita (USD) '}
    )
    fig.update_layout(
        title_text=title,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_colorbar={
            'title': f"<b>{item_clicked}</b>",
            }
    )
    return fig, title


# runs the app
if __name__ == '__main__':
    app.run_server(debug=True)
