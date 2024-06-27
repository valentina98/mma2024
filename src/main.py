from dash import Dash, html, dcc
from src import config
# from src.Dataset import Dataset
import dash_bootstrap_components as dbc
from src.widgets import dataset_selection_widget, help_popup_widget, history_widget, ohlc_chart_widget, prompt_engineering_widget
from src.callbacks import dataset_callback, history_callback, prompt_engineering_callback, uncertainty_callback

def run_ui():
    external_stylesheets = [dbc.themes.BOOTSTRAP]
    app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

    initial_chart_store = dcc.Store(id='initial-chart-store', data=True)  # Store to track if the initial chart is present
    full_history_store = dcc.Store(id='full-history-store', data=[])  # Store to keep track of the full history
    deleted_history_store = dcc.Store(id='deleted-history-store', data=[])  # Store to keep track of deleted entries

    # help_popup_widget = help_popup_widget.create_help_popup() # ToDo: Implement help_popup
    ohls_chart_widget = ohlc_chart_widget.create_ohlc_chart(ohlc_chart_widget.chart_data)

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
            html.Div(id='ohls-chart', children=[ohls_chart_widget], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '100%'})
        ]),
    ], style={'marginBottom': '20px'})

    app.layout = dbc.Container([
        # help_popup_widget,
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
