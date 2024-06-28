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