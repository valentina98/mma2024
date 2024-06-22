from dash import Dash, html, dcc
from src import config
from src.Dataset import Dataset
from src.widgets import help_popup, chart
import dash_bootstrap_components as dbc
import pandas as pd
import src.callbacks.combined_callback  # Import the combined callback
from src.widgets import dataset_selection

# Sample data, replace with your actual data source
chart_data = pd.DataFrame({
    'Date': pd.date_range(start='2023-01-01', periods=30, freq='D'),
    'Open': [30, 31, 32, 33, 30, 28, 29, 30, 31, 33, 34, 32, 31, 33, 35, 36, 37, 38, 39, 40, 39, 38, 37, 35, 34, 33, 32, 31, 30, 28],
    'High': [31, 32, 33, 34, 32, 29, 30, 32, 33, 35, 36, 34, 33, 35, 37, 38, 39, 40, 41, 42, 41, 40, 39, 37, 36, 35, 34, 33, 32, 30],
    'Low': [29, 30, 31, 32, 29, 27, 28, 29, 30, 32, 33, 31, 30, 32, 34, 35, 36, 37, 38, 39, 38, 37, 36, 34, 33, 32, 31, 30, 29, 27],
    'Close': [30, 31, 32, 31, 29, 28, 29, 31, 32, 34, 33, 32, 32, 34, 36, 37, 38, 39, 40, 39, 38, 37, 35, 36, 34, 33, 32, 31, 29, 28]
})

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

def run_ui():
    external_stylesheets = [dbc.themes.BOOTSTRAP]
    app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

    prompt_input = dcc.Textarea(id='prompt-input', style={'width': '100%', 'height': 100}, placeholder='Enter your prompt here...')
    answer_widget = dcc.Textarea(id='answer-input', style={'width': '100%', 'height': 100}, placeholder='Answer will be displayed here...')
    score_store = dcc.Store(id='score-store')
    initial_chart_store = dcc.Store(id='initial-chart-store', data=True)  # Store to track if the initial chart is present
    full_history_store = dcc.Store(id='full-history-store', data=[])  # Store to keep track of the full history
    deleted_history_store = dcc.Store(id='deleted-history-store', data=[])  # Store to keep track of deleted entries

    initial_chart = chart.create_chart(code, 'Housing')  # Provide the dataset name
    help_popup_widget = help_popup.create_help_popup()
    # ohls_chart_widget = ohls_chart.create_ohlc_chart(chart_data)

    initial_prompt = html.P("Initial Prompt", style={'text-align': 'center'})
    initial_entry = html.Div([
        html.Div([initial_prompt], style={'flex': '1', 'padding': '10px'}),
        html.Div([initial_chart], style={'flex': '1', 'padding': '10px'}),
        html.Button('Delete', id={'type': 'delete-button', 'index': 0}, n_clicks=0)
    ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'})

    tabs = dcc.Tabs([
        dcc.Tab(label='Dataset Selection', children=[
            dataset_selection.create_dataset_selection()
        ]),
        dcc.Tab(label='Prompt Engineering', children=[
            dbc.Container([
                dbc.Row([
                    dbc.Col(prompt_input, width=12),
                    dbc.Col(answer_widget, width=12)
                ]),
                dbc.Row([
                    dbc.Col(dbc.Button('Save', id='save-button', color='primary'), width='auto'),
                    dbc.Col(dbc.Button('Submit', id='submit-button', color='success'), width='auto')
                ], justify='center', style={'marginTop': '20px'}),
                score_store
            ], fluid=True)
        ]),
        dcc.Tab(label='Visualization History', children=[
            dbc.Container(id='history-container', children=[
                dbc.Row([
                    dbc.Col(html.Div(id='combined-history', children=[
                        initial_entry
                    ], style={'height': '500px', 'overflow': 'auto'}), width=12)
                ]),
                dbc.Row([
                    dbc.Col(dbc.Button('Clear History', id='clear-history-button', color='danger'), width='auto'),
                    dbc.Col(dbc.Button('Restore History', id='restore-history-button', color='secondary'), width='auto')
                ], justify='center', style={'marginTop': '20px'})
            ], fluid=True)
        ]),
        dcc.Tab(label='(Un)certainty Chart', children=[
            html.Div(id='uncertainty-chart', style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '100%'})
        ]),
    ], style={'marginBottom': '20px'})

    app.layout = dbc.Container([
        help_popup_widget,
        tabs,
        initial_chart_store,
        full_history_store,
        deleted_history_store
    ], fluid=True, id='container')

    app.run_server(debug=True, use_reloader=False)

def main():
    if not Dataset.files_exist():
        print('File', config.AUGMENTED_DATASET_PATH, 'missing or file', config.ATTRIBUTE_DATA_PATH, 'missing or directory', config.IMAGES_DIR, 'missing')
        print('Creating dataset.')
        Dataset.download()

    Dataset.load()

    if len(Dataset.get()) != config.DATASET_SAMPLE_SIZE:
        print('Sample size changed in the configuration. Recalculating features.')
        Dataset.download()
        Dataset.load()

    print('Starting Dash')
    run_ui()

if __name__ == '__main__':
    main()
