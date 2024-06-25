from dash import dcc, html
import dash_bootstrap_components as dbc
from utils import generate_chart

def create_input():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Label('Prompt:', className='label'),
                        html.Span("", id='prompt-score', className='prompt-score')
                    ], width=12),
                    dbc.Col(dcc.Loading(
                        id="loading-prompt",
                        className='dash-loading',
                        type="circle",
                        children=dcc.Textarea(id='prompt-input', className='dash-textarea', placeholder='Enter your prompt here...')
                    ), width=12)
                ]),
                dbc.Row([
                    html.Label('Code and Chart:', className='label'),
                    dbc.Col(
                        dcc.Loading(
                            id="loading-answer",
                            className='dash-loading',
                            type="circle",
                            children=dcc.Textarea(id='answer-input', className='dash-textarea', style={'height': '200px'}, placeholder='Answer will be displayed here...')
                        ), width=8),
                    dbc.Col(
                        dcc.Loading(
                            id="loading-chart",
                            className='dash-loading',
                            type="graph",
                            fullscreen=False,
                            children=html.Div(
                                'The chart will be displayed here...',
                                id='resulting-chart', className='resulting-chart'
                            )
                        ), width=4),
                ]),
                dbc.Row([
                    dbc.Col(dbc.Button('Save', id='save-button', color='primary', className='dash-button me-2'), width='auto'),
                    dbc.Col(dbc.Button('Submit', id='submit-button', color='success', className='dash-button'), width='auto')
                ], justify='center', style={'margin': '20px'}),
            ], width=8),
            dbc.Col([
                html.Div([
                    html.Label('Suggestions:', className='label'),
                    html.Div(id='suggestions-container', className='suggestions-container'),
                ])
            ], width=4)
        ]),
    ], fluid=True)

def create_score_span(score):
    if score and isinstance(score, float):
        score = round(score, 3)
    return html.Span(f"({score})", className='suggestion-score')

def create_suggestion(suggestion_prompt, index):
    return html.Button(suggestion_prompt, id={'type': 'suggestion-button', 'index': index}, n_clicks=0, className='suggestion-button')

def create_main_chart(code, dataset_name):
    return dcc.Graph(id="main-chart", figure=generate_chart(code, dataset_name), className='main-chart')

def create_suggestion_chart(suggestion_code, dataset_name, index):
    chart_graph = dcc.Graph(figure=generate_chart(suggestion_code, dataset_name), className='suggestion-chart')
    chart_div = html.Div(id={'type': 'suggestion-chart', 'index': index}, children=chart_graph, className='suggestion-chart-div')
    return chart_div

def create_suggestions(suggestions, dataset_name):
    return [
        html.Div([
            create_score_span(suggestion_score),
            dcc.Loading(
                id={'type': 'loading-suggestion', 'index': i},
                className='dash-loading',
                type="circle",
                children=create_suggestion(suggestion_prompt, i),
            ),
            create_suggestion_chart(suggestion_code, dataset_name, i),
            html.Div(hidden=True, children=suggestion_code, id={'type': 'suggestion-code', 'index': i})
        ], className='suggestion-container') for i, (suggestion_prompt, suggestion_score, suggestion_code) in enumerate(suggestions)
    ]
