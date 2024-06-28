from dash import dcc, html
import dash_bootstrap_components as dbc
from utils import generate_chart

tooltip_message_score = 'A trustworthiness score of the prompt/response'

def create_input():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Label('Prompt:', className='label'),
                        html.Span("", id='prompt-score', title=tooltip_message_score)
                    ], width=12),
                    dcc.Loading(
                        id="loading-prompt",
                        className='dash-loading',
                        type="circle",
                        children=dcc.Textarea(id='prompt-input', className='dash-textarea', placeholder='Provide a prompt to generate a plot from your dataset...')
                    )
                ]),
                dbc.Row([
                    dbc.Col(dbc.Button('Submit Prompt', id='submit-button', color='primary', className='pe-button'), width='auto', style={'margin-left': 'auto'}),
                ]),
                dbc.Row([
                    html.Label('Code and Chart:', className='label'),
                    dcc.Loading(
                        id="loading-answer",
                        className='dash-loading',
                        type="circle",
                        children=dcc.Textarea(id='answer-input', className='dash-textarea', placeholder='Answer will be displayed here...')
                    )
                ]),
                dbc.Row([
                    dbc.Col(dbc.Button('Save Chart', id='save-button', color='success', className='pe-button'), width='auto', style={'margin-left': 'auto'})
                ]),
            ], width=3),
            dbc.Col([
                dcc.Loading(
                    id="loading-chart",
                    className='dash-loading',
                    type="graph",
                    fullscreen=False,
                    children=html.Div('The chart will be displayed here...', id='main-chart-container',)
                )
            ], width=5),
            dbc.Col([
                html.Div([
                    html.Label('Suggestions:', className='label'),
                    dcc.Loading(
                        id="loading-suggestions",
                        className='dash-loading',
                        type="circle",
                        fullscreen=False,
                        children=html.Div(id='suggestions-container', className='suggestions-container'))
                ])
            ], width=4)
        ]),
    ], fluid=True)

def create_prompt_chart(code, dataset_name):
    fig = generate_chart(code, dataset_name)
    return html.Div(children=dcc.Graph(figure=fig, id="main-chart"), id='main-chart-container')

def create_prompt_score_span(score):
    if score and isinstance(score, float):
        score = round(score, 3)
        return html.Span(f"({score})", className='suggestion-score', title=tooltip_message_score)
    else: 
        return html.Span(score, className='suggestion-score', title=tooltip_message_score)

def create_suggestion_score_span(score, index):
    if score and isinstance(score, float):
        score = round(score, 3)
        return html.Span(f"({score})", id={'type': 'suggestion-score', 'index': index}, className='suggestion-score', title=tooltip_message_score)
    else:
        return html.Span(f"", id={'type': 'suggestion-score', 'index': index}, className='suggestion-score', title=tooltip_message_score)

def create_suggestion(suggestion_prompt, index):
    return html.Button(suggestion_prompt, id={'type': 'suggestion-button', 'index': index}, n_clicks=0, className='suggestion-button')


def create_suggestion_chart(fig, index):
    chart_graph = dcc.Graph(figure=fig, className='suggestion-chart')
    return html.Div(id={'type': 'suggestion-chart', 'index': index}, children=chart_graph, className='suggestion-chart-container')

def create_suggestions(suggestions, dataset_name):
    return [
        html.Div([
            create_suggestion_score_span(suggestion_score, i),
            create_suggestion(suggestion_prompt, i),
            create_suggestion_chart(generate_chart(suggestion_code, dataset_name), i),
            html.Div(hidden=True, children=suggestion_code, id={'type': 'suggestion-code', 'index': i})
        ], className='suggestion-container') for i, (suggestion_prompt, suggestion_score, suggestion_code) in enumerate(suggestions)
    ]
