from dash import callback, Output, Input, State, ctx, no_update
from dash.dependencies import ALL
from src.widgets import prompt_engineering_widget, popup_error_widget
from utils import logger, get_code_and_suggestions, generate_chart


# Callback when the "Submit The Prompt" button is clicked
@callback(
    [Output('answer-input', 'value', allow_duplicate=True),
     Output('suggestions-container', 'children'),
     Output('main-chart-container', 'children', allow_duplicate=True),
     Output('prompt-score', 'children', allow_duplicate=True),
     Output('error-popup-container', 'children', allow_duplicate=True)],
    Input('submit-button', 'n_clicks'),
    State('prompt-input', 'value'),
    State('selected-dataset-store', 'data'),
    prevent_initial_call=True
)
def save_clicked(n_clicks, prompt, dataset_name):
    logger.info(f"Handling save and suggestions for prompt: {prompt}, n_clicks: {n_clicks}, selected_dataset_store: {dataset_name}")
    if dataset_name:
        code, trustworthiness_score, suggestions = get_code_and_suggestions(prompt, dataset_name)

        # Generate suggestions and charts
        suggestions_list = prompt_engineering_widget.create_suggestions(suggestions, dataset_name)
        
        # Generate the main chart
        prompt_chart = prompt_engineering_widget.create_prompt_chart(code, dataset_name)
        prompt_score = prompt_engineering_widget.create_prompt_score_span(trustworthiness_score)
        
        return code, suggestions_list, prompt_chart, prompt_score, no_update
    else:
        return "", "", "The chart will be displayed here...", "", popup_error_widget.create_popup_error("Please select a dataset before submitting the prompt.")


# Callback when one of the suggestions is selected
@callback(
    [Output('prompt-input', 'value'),
     Output('answer-input', 'value', allow_duplicate=True),
     Output('main-chart-container', 'children', allow_duplicate=True),
     Output('prompt-score', 'children', allow_duplicate=True)],
    Input({'type': 'suggestion-button', 'index': ALL}, 'n_clicks'),
    State({'type': 'suggestion-button', 'index': ALL}, 'children'),
    State({'type': 'suggestion-code', 'index': ALL}, 'children'),
    # State({'type': 'suggestion-chart', 'index': ALL}, 'children'), # If you use this you get a small chart in the main chart container
    State({'type': 'suggestion-score', 'index': ALL}, 'children'),
    State('selected-dataset-store', 'data'),
    prevent_initial_call=True
)
def suggestion_clicked(n_clicks, suggestions, suggestion_codes, suggestion_scores, dataset_name):

    # Avoid updating the prompt if no suggestion was clicked
    if not any(n_clicks):
        return no_update, no_update, no_update, no_update

    # Identify which button was clicked
    triggered_index = ctx.triggered_id['index']
    logger.info(f"Updating prompt from suggestion index: {triggered_index}")

    # Create a new main chart and new main score components
    new_prompt_chart = prompt_engineering_widget.create_prompt_chart(suggestion_codes[triggered_index], dataset_name)
    new_prompt_score = prompt_engineering_widget.create_prompt_score_span(suggestion_scores[triggered_index])

    return suggestions[triggered_index], suggestion_codes[triggered_index], new_prompt_chart, new_prompt_score


# The "Save The Prompt" button is handled in history_callback.py
