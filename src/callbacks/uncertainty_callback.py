from dash import callback, Output, Input, State, no_update, ctx, Dash, html, dcc
from dash.dependencies import ALL
from utils import logger
from src.widgets import prompt_history_plotter_widget

# Store the history globally
history = []

def initialize_placeholder():
    plotter = prompt_history_plotter_widget.PromptHistoryPlotter()
    initial_prompt = 0.8
    initial_suggestions = [0.2, 0.4, 0.6]
    fig = plotter.plot_initial(initial_prompt, *initial_suggestions)
    return fig

app = Dash(__name__)

@callback(
    Output('custom-ohlc-chart', 'children'),
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
    #debugging
    print(f"Handling manage the custom OHLC: {save_n_clicks}, prompt_score: {prompt_score}, suggestion_scores: {suggestion_scores}")

    # Convert scores to float
    prompt_score = float(prompt_score)
    suggestion_scores = [float(score) for score in suggestion_scores]
    
    # Append the current scores to the history
    history.append((prompt_score, suggestion_scores, suggestion_scores[0]))  # Assuming first suggestion is selected

    # Generate the new plot using the updated history
    plotter = prompt_history_plotter_widget.PromptHistoryPlotter()
    initial_prompt, initial_suggestions, _ = history[0]
    subsequent_suggestions_and_selections = [(sug, sel) for _, sug, sel in history[1:]]
    fig = plotter.plot_sequence(initial_prompt, initial_suggestions, subsequent_suggestions_and_selections)
    
    return html.Div(dcc.Graph(figure=fig))

# Initialization to display the initial plot as placeholder
fig = initialize_placeholder()
app.layout = html.Div([
    html.Button('Save', id='save-button'),
    dcc.Store(id='prompt-score', data='0.8'),
    dcc.Store(id='suggestion-score-1', data='0.2'),
    dcc.Store(id='suggestion-score-2', data='0.4'),
    dcc.Store(id='suggestion-score-3', data='0.6'),
    html.Div(id='custom-ohlc-chart', children=html.Div(dcc.Graph(figure=fig))),
])
