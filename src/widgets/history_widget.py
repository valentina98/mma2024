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

def create_delete_button(button_id):
    return dbc.Button('Delete', id=button_id, n_clicks=0, className='history-button', color='danger')

def create_new_prompt(prompt_value):
    return html.Div([html.P(prompt_value, className='history-prompt')], className='history-entry-content')

def create_new_chart(fig):
    return html.Div([dcc.Graph(figure=fig, className='history-chart')], className='history-entry-content')

def create_new_entry(prompt_value, fig, full_history_length):
    new_prompt_div = create_new_prompt(prompt_value)
    new_chart_div = create_new_chart(fig)
    delete_button = create_delete_button({'type': 'delete-button', 'index': full_history_length})
    return html.Div([new_prompt_div, new_chart_div, delete_button], className='history-entry')

def create_error(error_message):
    return html.Div(f"An error occurred while plotting the chart: {error_message}", className='history-error')

def create_history_widget():
    # Create initial chart
    # ToDo: Remove initial plot
    fig = generate_chart(code, 'Housing')
    initial_chart = create_new_chart(fig)
    initial_prompt = create_new_prompt("Initial Prompt")
    delete_button = create_delete_button({'type': 'delete-button', 'index': 0})
    initial_entry = html.Div([
        initial_prompt,
        initial_chart,
        delete_button
    ], className='history-entry')

    return dbc.Container(id='history-container', children=[
        dbc.Row([
            dbc.Col(html.Div(id='combined-history', children=[
                initial_entry
            ], className='history-container'), width=12)
        ]),
        dbc.Row([
            dbc.Col(dbc.Button('Clear History', id='clear-history-button', className='history-button', color='danger'), width='auto'),
            dbc.Col(dbc.Button('Restore History', id='restore-history-button', className='history-button', color='secondary'), width='auto')
        ], justify='center')
    ], fluid=True)
