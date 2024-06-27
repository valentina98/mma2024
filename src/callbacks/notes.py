from dash import callback, Output, Input, State, no_update, ctx
from dash.dependencies import ALL
from utils import logger

@callback(
    Output('custom-ohlc-chart', 'children'),
    Input('save-button', 'n_clicks'),
    State('prompt-score', 'children'),
    State({'type': 'suggestion-score', 'index': ALL}, 'children'),
    prevent_initial_call=True
)
def save_clicked_update_custom_ohlc(save_n_clicks, prompt_score, suggestion_scores):
    
    if not ctx.triggered:
        return no_update
    
    logger.info(f"Handling manage the custom OHLC: {save_n_clicks}, prompt_score: {prompt_score}, suggestion_scores: {suggestion_scores}")
    # INFO:utils:Handling manage the custom OHLC: 1, prompt_score: {'props': {'children': '(0.638)', 'className': 'suggestion-score'}, 'type': 'Span', 'namespace': 'dash_html_components'}, suggestion_scores: ['(0.327)', '(0.007)', '(0.07)']

    # logger.info(f"prompt_score: {prompt_score.get(props)children}")
    # logger.info(f"suggestion_scores: {suggestion_scores}")
    
    # initial_prompt = 0.8
    # initial_suggestions = [0.2, 0.4, 0.6]
    # subsequent_suggestions_and_selections = [
    #     ([0.5, 0.7, 0.9], 0.6),
    #     ([0.1, 0.3, 0.95], 0.9)
    # ]


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
