from dash import dcc, html
import dash_bootstrap_components as dbc
from utils import generate_chart

def create_input():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Label('Prompt:', style={'fontWeight': 'bold', 'fontSize': '18px', 'display': 'inline-block'}),
                        html.Span(f"()", id='prompt-score', style={'fontWeight': 'bold', 'margin': '10px', 'display': 'inline-block'})
                    ], width=12),
                    dbc.Col(dcc.Loading(
                        id="loading-prompt",
                        type="circle",
                        children=dcc.Textarea(id='prompt-input', style={
                            'width': '100%', 'height': 150, 'resize': 'none',
                            'padding': '10px', 'fontSize': '16px', 'borderRadius': '10px',
                            'border': '1px solid gray', 'scrollbar-gutter': 'stable'
                        }, placeholder='Enter your prompt here...')
                    ), width=12)
                ]),
                dbc.Row([
                    html.Label('Code and Chart:', style={'fontWeight': 'bold', 'fontSize': '18px'}),
                    dbc.Col(
                        dcc.Loading(
                            id="loading-answer",
                            type="circle",
                            children=dcc.Textarea(id='answer-input', style={
                                'width': '100%', 'height': 200, 'resize': 'none',
                                'padding': '10px', 'fontSize': '16px', 'borderRadius': '10px',
                                'border': '1px solid gray', 'scrollbar-gutter': 'stable'
                            }, placeholder='Answer will be displayed here...')
                        ), width=8),
                    dbc.Col(
                        html.Div(
                        'The chart will be displayed here...',
                        id='resulting-chart', style={
                        'width': '100%', 'height': 200, 'resize': 'none',
                        'padding': '10px', 'scrollbar-gutter': 'stable',
                        'color': 'gray', 'fontSize': '16px'}
                    ), width=4),
                ]),
                dbc.Row([
                    dbc.Col(dbc.Button('Save', id='save-button', color='primary', className='me-2', style={'width': '100%', 'min-width': '150px', 'padding': '5px'}), width='auto'),
                    dbc.Col(dbc.Button('Submit', id='submit-button', color='success', style={'width': '100%', 'min-width': '150px', 'padding': '5px'}), width='auto')
                ], justify='center', style={'margin': '20px'}),
            ], width=8),
            dbc.Col([
                html.Div([
                    html.Label('Suggestions:', style={'fontWeight': 'bold', 'fontSize': '18px'}),
                    html.Div(id='suggestions-container', style={
                        'height': 450, 'padding': '10px', 'borderRadius': '10px',
                        'overflowY': 'scroll', 'overflowX': 'hidden', 'scrollbar-gutter': 'stable'
                    }),
                ])
            ], width=4)
        ]),
    ], fluid=True)

def get_score(score):
    # round to 3 decimal places
    score = round(score, 3)
    return html.Span(f"({score})", style={'fontWeight': 'bold', 'margin': '10px'})

def get_suggestion(suggestion_prompt, index):
    return html.Button(suggestion_prompt, id={'type': 'suggestion-button', 'index': index}, n_clicks=0, style={
        'margin': '5px', 'borderRadius': '10px', 'border': 'none', 'padding': '10px',
        'backgroundColor': '#F9F9F9', 'width': '100%', 'display': 'flex', 'alignItems': 'center'
    })

def get_suggestion_chart(suggestion_code, dataset_name, index):
    chart_graph = dcc.Graph(figure=generate_chart(suggestion_code, dataset_name), 
        style={'display': 'inline-block', 'width': '100px', 'height': '100px', 'marginLeft': '10px'})
    chart_div = html.Div(id={'type': 'suggestion-chart', 'index': index}, children=chart_graph, style={
        'display': 'inline-block', 'width': '100px', 'height': '100px', 'marginLeft': '10px'
    })
    return chart_div

def create_suggestions(suggestions, dataset_name):
    return [
        html.Div([
            get_score(suggestion_score),
            dcc.Loading(
                id={'type': 'loading-suggestion', 'index': i},
                type="circle",
                children=get_suggestion(suggestion_prompt, i),
            ),
            get_suggestion_chart(suggestion_code, dataset_name, i),
            html.Div(hidden=True, children=suggestion_code, id={'type': 'suggestion-code', 'index': i})
        ], style={
            'display': 'flex', 'alignItems': 'center', 'borderRadius': '10px', 
            'padding': '10px', 'marginBottom': '10px', 'cursor': 'pointer', 'backgroundColor': '#F9F9F9'
        }) for i, (suggestion_prompt, suggestion_score, suggestion_code) in enumerate(suggestions)
    ]
