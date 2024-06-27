from dash import Dash, html, dcc
from src import config
# from src.Dataset import Dataset
import dash_bootstrap_components as dbc
from src.widgets import dataset_selection_widget, help_popup_widget, history_widget, prompt_engineering_widget
from src.callbacks import dataset_callback, history_callback, prompt_engineering_callback, uncertainty_callback
from src.widgets.ohlc_chart_widget import create_prompt_history_chart

def run_ui():
    external_stylesheets = [dbc.themes.BOOTSTRAP]
    app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

    initial_chart_store = dcc.Store(id='initial-chart-store', data=True)  # Store to track if the initial chart is present
    full_history_store = dcc.Store(id='full-history-store', data=[])  # Store to keep track of the full history
    deleted_history_store = dcc.Store(id='deleted-history-store', data=[])  # Store to keep track of deleted entries

    # help_popup_widget = help_popup_widget.create_help_popup() # ToDo: Implement help_popup
    initial_prompt = 0.8
    initial_suggestions = [0.2, 0.4, 0.6]
    subsequent_suggestions_and_selections = [
        ([0.5, 0.7, 0.9], 0.6),
        ([0.65, 0.85, 0.95], 0.9)
    ]
    ohls_chart_widget = create_prompt_history_chart(initial_prompt, initial_suggestions, subsequent_suggestions_and_selections)

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

    app.run_server(debug=True, use_reloader=False)

def main():
    # if not Dataset.files_exist():
    #     print('File', config.AUGMENTED_DATASET_PATH, 'missing or file', config.ATTRIBUTE_DATA_PATH, 'missing or directory', config.IMAGES_DIR, 'missing')
    #     print('Creating dataset.')
    #     Dataset.download()

    # Dataset.load()

    # if len(Dataset.get()) != config.DATASET_SAMPLE_SIZE:
    #     print('Sample size changed in the configuration. Recalculating features.')
    #     Dataset.download()
    #     Dataset.load()

    print('Starting Dash')
    run_ui()

if __name__ == '__main__':
    main()
