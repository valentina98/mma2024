from dash import callback, Output, Input, State, dcc, ctx, no_update
from dash.dependencies import ALL
from src.widgets import prompt_engineering_widget
from utils import logger, get_code_and_suggestions, generate_chart

# Callback when the "Save" button is clicked
@callback(
    [Output('answer-input', 'value', allow_duplicate=True),
     Output('suggestions-container', 'children'),
     Output('resulting-chart', 'children')],
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
        
        # Generate the main chart
        main_chart = dcc.Graph(figure=generate_chart(code, dataset_name), style={
            'width': '100%', 'height': 200, 'resize': 'none',
            'padding': '10px', 'scrollbar-gutter': 'stable',
            'color': 'gray', 'fontSize': '16px'
        })
        
        return code, suggestions_list, main_chart
    return "", "", "The chart will be displayed here..."

# Callback when one of the suggestions is selected
@callback(
    [Output('prompt-input', 'value'),
     Output('answer-input', 'value', allow_duplicate=True)],
    Input({'type': 'suggestion-button', 'index': ALL}, 'n_clicks'),
    State({'type': 'suggestion-button', 'index': ALL}, 'children'),
    State({'type': 'suggestion-code', 'index': ALL}, 'children'),
    prevent_initial_call=True
)
def suggestion_clicked(n_clicks, suggestions, suggestion_codes):

    if not any(n_clicks):
        return no_update, no_update

    # Identify which button was clicked
    triggered_index = ctx.triggered_id['index']
    logger.info(f"Updating prompt from suggestion index: {triggered_index}")

    return suggestions[triggered_index], suggestion_codes[triggered_index]


# The "Submit" button is handled in history_callback.py
