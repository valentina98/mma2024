from dash import callback, Output, Input, State, ctx, no_update
from dash.dependencies import ALL
from src.widgets import prompt_engineering_widget, popup_error_widget
from utils import logger, get_code, get_trustworthiness_score, get_suggestions


# Callback to update the code and chart when the "Submit The Prompt" button is clicked
@callback(
    [Output('answer-input', 'value', allow_duplicate=True),
     Output('main-chart-container', 'children', allow_duplicate=True),
     Output('error-popup-container', 'children', allow_duplicate=True)],
    Input('submit-button', 'n_clicks'),
    State('prompt-input', 'value'),
    State('selected-dataset-store', 'data'),
    prevent_initial_call=True
)
def submit_clicked_update_main(n_clicks, prompt, dataset_name):
    logger.info(f"Handling update main for prompt: {prompt}, n_clicks: {n_clicks}, selected_dataset_store: {dataset_name}")
    if dataset_name:

        # Prompt an llm for the code
        code = get_code(prompt, dataset_name)

        # Generate the main chart
        prompt_chart = prompt_engineering_widget.create_prompt_chart(code, dataset_name)
        
        return code, prompt_chart, no_update
    else:
        return "", "The chart will be displayed here...", popup_error_widget.create_popup_error("Please select a dataset before submitting the prompt.")


# Callback to update prompt score when the "Submit The Prompt" button is clicked
@callback(
    Output('prompt-score', 'children', allow_duplicate=True),
    Input('submit-button', 'n_clicks'),
    State('prompt-input', 'value'),
    # State('answer-input', 'value'), # ToDo
    State('selected-dataset-store', 'data'),
    prevent_initial_call=True
)
def submit_clicked_update_score(n_clicks, prompt, dataset_name):
    logger.info(f"Handling update score for prompt: {prompt}, n_clicks: {n_clicks}, selected_dataset_store: {dataset_name}")
    if dataset_name:
        # Get score for the prompt
        trustworthiness_score = get_trustworthiness_score(prompt)

        # Create the score widget
        prompt_score = prompt_engineering_widget.create_prompt_score_span(trustworthiness_score)
        
        return prompt_score


# Callback to update suggestions when the "Submit The Prompt" button is clicked
@callback(
    Output('suggestions-container', 'children'),
    Input('submit-button', 'n_clicks'),
    State('prompt-input', 'value'),
    State('selected-dataset-store', 'data'),
    prevent_initial_call=True
)
def submit_clicked_update_suggestions(n_clicks, prompt, dataset_name):
    logger.info(f"Handling update suggestions for prompt: {prompt}, n_clicks: {n_clicks}, selected_dataset_store: {dataset_name}")
    if dataset_name:
        
        # Prompt the llm for the suggestions
        suggestions = get_suggestions(prompt, dataset_name)

        # Generate suggestions and charts
        suggestions_list = prompt_engineering_widget.create_suggestions(suggestions, dataset_name)
        
        return suggestions_list
    else:
        return ""


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
