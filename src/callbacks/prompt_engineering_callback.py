from dash import callback, html, Output, Input, State, no_update, dcc, ctx
from dash.dependencies import ALL
import matplotlib.pyplot as plt
import io
import base64
from src.widgets import prompt_engineering_widget
from utils import logger, load_dataset, get_code_and_suggestions

# Callback when the "Save" button is clicked
@callback(
    [Output('answer-input', 'value', allow_duplicate=True),
     Output('suggestions-container', 'children')],
    Input('save-button', 'n_clicks'),
    State('prompt-input', 'value'),
    State('selected-dataset-store', 'data'),
    prevent_initial_call=True
)
def save_clicked(n_clicks, prompt, dataset_name):
    logger.info(f"Handling save and suggestions for prompt: {prompt}, n_clicks: {n_clicks}, selected_dataset_store: {dataset_name}")
    if n_clicks > 0 and prompt and dataset_name:
                
        code, trustworthiness_score, suggestions = get_code_and_suggestions(prompt, dataset_name)

        # Generate suggestions and charts
        suggestions_list = prompt_engineering_widget.create_suggestions(suggestions, dataset_name)
        return code, suggestions_list
    return "", ""

# Callback when the one of the suggestions is selected
@callback(
    [Output('prompt-input', 'value'),
     Output('answer-input', 'value', allow_duplicate=True)],
    Input({'type': 'suggestion-button', 'index': ALL}, 'n_clicks'),
    State({'type': 'suggestion-button', 'index': ALL}, 'children'),
    State({'type': 'suggestion-code', 'index': ALL}, 'children'),
    prevent_initial_call=True
)
def suggestion_clicked(n_clicks, suggestions, suggestion_codes):
    
    # Identify which button was clicked
    triggered_index = ctx.triggered_id['index']
    logger.info(f"Updating prompt from suggestion index: {triggered_index}")

    return suggestions[triggered_index], suggestion_codes[triggered_index]


# The "Submit" button is handled in history_callback.py
