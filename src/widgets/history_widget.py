from dash import html, dcc
import dash_bootstrap_components as dbc
from src.utils import generate_chart

code = '''import matplotlib.pyplot as plt

# Example data for the pie chart
labels = ['Rent', 'Groceries', 'Utilities']
sizes = [1200, 300, 150]
colors = ['#ff9999','#66b3ff','#99ff99']
explode = (0.1, 0, 0)  # explode 1st slice (i.e. 'Rent')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=140)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title("January Expenses")
plt.show()
'''

def create_history_widget():
    # Create initial chart
    initial_chart = dcc.Graph(figure=generate_chart(code, 'Housing'), className='history-chart')
    initial_prompt = html.P("Initial Prompt", style={'text-align': 'center'})
    initial_entry = html.Div([
        html.Div([initial_prompt], className='history-entry-content'),
        html.Div([initial_chart], className='history-entry-content', style={'width': '100px', 'height': '100px'}),
        html.Button('Delete', id={'type': 'delete-button', 'index': 0}, n_clicks=0, className='history-delete-button')
    ], className='history-entry')

    return dbc.Container(id='history-container', children=[
        dbc.Row([
            dbc.Col(html.Div(id='combined-history', children=[
                initial_entry
            ], className='history-container'), width=12)
        ]),
        dbc.Row([
            dbc.Col(dbc.Button('Clear History', id='clear-history-button', color='danger', className='history-button'), width='auto'),
            dbc.Col(dbc.Button('Restore History', id='restore-history-button', color='secondary', className='history-button'), width='auto')
        ], justify='center')
    ], fluid=True)
