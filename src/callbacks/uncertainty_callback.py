from dash import callback, Output, Input, State, no_update, ctx, html, dcc
from dash.dependencies import ALL
from utils import logger
from src.widgets import prompt_history_plotter_widget
# Store the history globally
from src.widgets.ohlc_chart_widget import create_prompt_history_chart
history = []

@callback(
    Output('ohls-chart', 'children', allow_duplicate=True),
    Input('save-button', 'n_clicks'),
    State('prompt-score', 'children'),
    State({'type': 'suggestion-score', 'index': ALL}, 'children'),
    prevent_initial_call=True
)
def save_clicked_update_custom_ohlc(save_n_clicks, prompt_score, suggestion_scores):
    global history
    
    if not ctx.triggered:
        return no_update

    logger.info(f"Handling manage the custom OHLC: {save_n_clicks}, prompt_score: {prompt_score}, suggestion_scores: {suggestion_scores}")
    
    # Extract and convert the prompt score to float
    prompt_value_str = prompt_score['props']['children']
    if prompt_value_str and prompt_value_str[1:-1]:
        prompt_value = float(prompt_value_str[1:-1])
    else:
        return no_update

    # Extract and convert the suggestion scores to float
    suggestion_values = []
    for score in suggestion_scores:
        score_str = score[1:-1]
        if score_str:
            suggestion_values.append(float(score_str))
        else:
            suggestion_values.append(0.0)  # Default to 0.0 if empty

    if save_n_clicks == 1:
        # Initial plot
        history.append((prompt_value, suggestion_values, None))
        history.append((prompt_value, suggestion_values, None))
        history[-1] = (history[-1][0], history[-1][1], prompt_value)
        history.append((prompt_value, suggestion_values, None))
    else:
        # Intermediate or final plot
        selected_suggestion = prompt_value  # The prompt value is the selected suggestion for the next plot
        history[-1] = (history[-1][0], history[-1][1], selected_suggestion)
        history.append((selected_suggestion, suggestion_values, None))

    subsequent_suggestions_and_selections = [(history[i][1], history[i][2]) for i in range(1, len(history))]
    return create_prompt_history_chart(history[0][0], history[0][1], subsequent_suggestions_and_selections)

