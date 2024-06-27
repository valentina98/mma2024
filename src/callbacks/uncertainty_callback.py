from dash import callback, Output, Input, State, no_update, ctx, Dash, html, dcc
from dash.dependencies import ALL
from utils import logger
from src.widgets import prompt_history_plotter_widget

# Store the history globally
history = []

def initialize_placeholder_1():
    plotter = prompt_history_plotter_widget.PromptHistoryPlotter()
    initial_prompt = 0.8
    initial_suggestions = [0.2, 0.4, 0.6]
    fig = plotter.plot_initial(initial_prompt, *initial_suggestions)
    return fig

def initialize_placeholder_2():
    plotter = prompt_history_plotter_widget.PromptHistoryPlotter()
    initial_prompt = 0.8
    initial_suggestions = [0.2, 0.4, 0.6]
    subsequent_suggestions_and_selections = [
        ([0.5, 0.7, 0.9], 0.6),
        ([0.1, 0.3, 0.95], 0.9)
    ]
    fig = plotter.plot_sequence(initial_prompt, initial_suggestions, subsequent_suggestions_and_selections)
    return fig

app = Dash(__name__)

@callback(
    [Output('custom-ohlc-chart', 'children', allow_duplicate=True),
    Output('initial-chart-store', 'data', allow_duplicate=True),
    Output('placeholder-buttons', 'style')],
    Input('save-button', 'n_clicks'),
    State('prompt-score', 'children'),
    State({'type': 'suggestion-score', 'index': ALL}, 'children'),
    State('initial-chart-store', 'data'),
    prevent_initial_call=True
)
def save_clicked_update_custom_ohlc(save_n_clicks, prompt_score, suggestion_scores, initial_chart_present):
    global history
    
    logger.info(f"Handling manage the custom OHLC: {save_n_clicks}, prompt_score: {prompt_score}, suggestion_scores: {suggestion_scores}")
    
    # Convert scores to float
    prompt_score = float(prompt_score)
    suggestion_scores = [float(score) for score in suggestion_scores]

    # Append the current scores to the history
    history.append((prompt_score, suggestion_scores, suggestion_scores[0]))  # Assuming first suggestion is selected

    # Generate the new plot using the updated history
    plotter = prompt_history_plotter_widget.PromptHistoryPlotter()
    initial_prompt, initial_suggestions, _ = history[0]
    subsequent_suggestions_and_selections = [(sug, sel) for _, sug, sel in history[1:]]

    if initial_chart_present:
        fig = plotter.plot_sequence(initial_prompt, initial_suggestions, subsequent_suggestions_and_selections)
        initial_chart_present = False  # Set the flag to False after removing the initial entry
    else:
        fig = plotter.plot_sequence(initial_prompt, initial_suggestions, subsequent_suggestions_and_selections)

    return html.Div(dcc.Graph(figure=fig)), initial_chart_present, {'display': 'none'}

@callback(
    Output('custom-ohlc-chart', 'children', allow_duplicate=True),
    Input('placeholder-1-button', 'n_clicks'),
    Input('placeholder-2-button', 'n_clicks'),
    prevent_initial_call=True
)
def switch_placeholder(placeholder_1_clicks, placeholder_2_clicks):
    if ctx.triggered_id == 'placeholder-1-button':
        fig = initialize_placeholder_1()
    elif ctx.triggered_id == 'placeholder-2-button':
        fig = initialize_placeholder_2()
    else:
        return no_update

    return html.Div(dcc.Graph(figure=fig))

# Initialization to display the initial plot as placeholder
fig = initialize_placeholder_1()
app.layout = html.Div([
    html.Button('Save', id='save-button'),
    html.Button('Placeholder 1', id='placeholder-1-button'),
    html.Button('Placeholder 2', id='placeholder-2-button'),
    dcc.Store(id='prompt-score', data='0.8'),
    dcc.Store(id='suggestion-score-1', data='0.2'),
    dcc.Store(id='suggestion-score-2', data='0.4'),
    dcc.Store(id='suggestion-score-3', data='0.6'),
    dcc.Store(id='initial-chart-store', data=True),  # Store to track if the initial chart is present
    html.Div(id='custom-ohlc-chart', children=html.Div(dcc.Graph(figure=fig))),
    html.Div(id='placeholder-buttons', children=[
        html.Button('Placeholder 1', id='placeholder-1-button'),
        html.Button('Placeholder 2', id='placeholder-2-button')
    ], style={'display': 'block'}),
])
