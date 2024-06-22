from dash import callback, html, Output, Input, State, no_update, dcc
import pandas as pd
from src.widgets import chart, dataset_selection
from cleanlab_studio import Studio
import os
from dotenv import load_dotenv
import dash
import matplotlib.pyplot as plt
import io
import base64

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv('TLM_API_KEY')

# Initialize the language model with your API key
studio = Studio(api_key)
tlm = studio.TLM()

# Function to get dataset path
def get_dataset_path(dataset_name):
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dataset/ourdata'))
    return os.path.join(base_path, f'{dataset_name}.csv')

@callback(
    [Output('dataset-table', 'children'),
     Output('selected-dataset-store', 'data')],
    Input('dataset-dropdown', 'value'),
    prevent_initial_call=True
)
def update_table(selected_dataset):
    if selected_dataset:
        data_path = get_dataset_path(selected_dataset)
        if os.path.exists(data_path):
            data = pd.read_csv(data_path)
            return dataset_selection.create_table(data), selected_dataset
        else:
            return f"Dataset {selected_dataset} not found.", ""
    return "", ""

@callback(
    Output('answer-input', 'value'),
    Input('save-button', 'n_clicks'),
    State('prompt-input', 'value'),
    State('selected-dataset-store', 'data'),
    prevent_initial_call=True
)
def save_prompt(n_clicks, prompt, selected_dataset_store):
    if n_clicks > 0 and prompt and selected_dataset_store:
        data_path = get_dataset_path(selected_dataset_store)
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            column_names = ", ".join(df.columns)
            first_two_rows = df.head(2).to_string(index=False)
            modified_prompt = f"Dataset: {selected_dataset_store}\n\nDataset columns: {column_names}\n\nFirst two rows:\n{first_two_rows}\n\nPrompt: {prompt}"
            response = tlm.prompt(modified_prompt)
            return response["response"]
    return ""

@callback(
    [Output('combined-history', 'children'),
     Output('initial-chart-store', 'data')],
    Input('submit-button', 'n_clicks'),
    State('answer-input', 'value'),
    State('combined-history', 'children'),
    State('prompt-input', 'value'),
    State('selected-dataset-store', 'data'),
    State('initial-chart-store', 'data'),
    prevent_initial_call=True
)
def update_chart(n_clicks, answer_code, history_children, prompt, selected_dataset, initial_chart_present):
    if n_clicks > 0 and answer_code and selected_dataset:
        data_path = get_dataset_path(selected_dataset)
        if os.path.exists(data_path):
            data = pd.read_csv(data_path)
            try:
                modified_code = answer_code.replace("housing", "df")
                exec(modified_code, {'df': data, 'plt': plt, 'pd': pd})

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                image_base64 = base64.b64encode(buf.read()).decode('utf-8')
                plt.close()

                new_prompt_div = html.Div([html.P(prompt, style={'text-align': 'center'})], style={'flex': '1', 'padding': '10px'})
                new_chart_div = html.Div([html.Img(src=f'data:image/png;base64,{image_base64}')], style={'flex': '1', 'padding': '10px'})
                
                new_entry = html.Div([new_prompt_div, new_chart_div], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'})
                
                if initial_chart_present:
                    new_history_children = [new_entry]
                    initial_chart_present = False  # Set the flag to False after removing the initial entry
                else:
                    new_history_children = [new_entry] + history_children

                return new_history_children, initial_chart_present
            except Exception as e:
                return [html.Div(f"An error occurred while plotting the chart: {str(e)}")] + history_children, initial_chart_present
        else:
            return [html.Div(f"Dataset {selected_dataset} not found.")] + history_children, initial_chart_present
    return no_update, initial_chart_present
