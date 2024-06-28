from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from src.widgets import dataset_selection_widget, help_popup_widget, history_widget, prompt_engineering_widget
import dash_bootstrap_components as dbc
from src.callbacks import dataset_callback, history_callback, prompt_engineering_callback, uncertainty_callback

def run_ui():
    external_stylesheets = [dbc.themes.BOOTSTRAP]
    app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

    initial_chart_store = dcc.Store(id='initial-chart-store', data=True)
    full_history_store = dcc.Store(id='full-history-store', data=[])
    deleted_history_store = dcc.Store(id='deleted-history-store', data=[])

    tabs = dcc.Tabs([
        dcc.Tab(label='Dataset Selection', children=[
            dataset_selection_widget.create_dataset_selection()
        ]),
        dcc.Tab(label='Prompt Engineering', children=[
            prompt_engineering_widget.create_input(),
        ]),
        dcc.Tab(label='Visualization History', children=[
            history_widget.create_history_widget()
        ]),
        dcc.Tab(label='(Un)certainty Chart', children=[
            html.Div([
                html.Div(id='ohls-chart', style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '400px', 'margin': '30px'}),
                html.Div([
                    dbc.Button('Clear History', id='clear-uncertainty-history-button', className='history-button', color='danger')
                ], style={'display': 'flex', 'justify-content': 'center'})
            ])
        ]),
    ], style={'marginBottom': '20px'})

    app.layout = dbc.Container([
        tabs,
        initial_chart_store,
        full_history_store,
        deleted_history_store,
        html.Div(id='error-popup-container'),
    ], fluid=True, id='container')

    return app

def main():
    print('Starting Dash')
    app = run_ui()
    app.run_server(debug=True, use_reloader=False)

if __name__ == '__main__':
    main()
