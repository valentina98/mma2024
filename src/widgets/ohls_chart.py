import dash
from dash import dcc
import plotly.graph_objects as go
import pandas as pd

def create_ohlc_chart(data):
    fig = go.Figure(data=[go.Ohlc(
        x=data['Iteration'],
        open=data['Certainty Prompt'],
        high=data['Highest Suggested Certainty'],
        low=data['Lowest Suggested Certainty'],
        close=data['Close'], #can be the certainty after the next one is chosen
        increasing_line_color='green', decreasing_line_color='red'
    )])

    fig.update_layout(
        title='Uncertainty Chart',
        xaxis_title='Iteration',
        yaxis_title='Relevance'
    )

    return dcc.Graph(figure=fig)
