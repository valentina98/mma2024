from dash import callback, html, Output, Input, State, no_update, dcc, ALL
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
     Output('selected-dataset-store', 'data'),
     Output('answer-input', 'value'),
     Output('combined-history', 'children'),
     Output('initial-chart-store', 'data'),
     Output('full-history-store', 'data'),
     Output('deleted-history-store', 'data')],
    [Input('dataset-dropdown', 'value'),
     Input('save-button', 'n_clicks'),
     Input('submit-button', 'n_clicks'),
     Input({'type': 'delete-button', 'index': ALL}, 'n_clicks'),
     Input('clear-history-button', 'n_clicks'),
     Input('restore-history-button', 'n_clicks')],
    [State('prompt-input', 'value'),
     State('selected-dataset-store', 'data'),
     State('answer-input', 'value'),
     State('combined-history', 'children'),
     State('initial-chart-store', 'data'),
     State('full-history-store', 'data'),
     State('deleted-history-store', 'data')],
    prevent_initial_call=True
)
def handle_callbacks(dataset_value, save_n_clicks, submit_n_clicks, delete_n_clicks, clear_n_clicks, restore_n_clicks,
                     prompt_value, selected_dataset_store, answer_input_value, history_children, initial_chart_present, full_history, deleted_history):
    
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    new_answer_input_value = no_update
    new_combined_history = history_children
    new_initial_chart_store = initial_chart_present
    new_full_history = full_history
    new_deleted_history = deleted_history

    # Handle dataset dropdown
    if triggered_id == 'dataset-dropdown' and dataset_value:
        data_path = get_dataset_path(dataset_value)
        if os.path.exists(data_path):
            data = pd.read_csv(data_path)
            return dataset_selection.create_table(data), dataset_value, no_update, no_update, no_update, no_update, no_update
        else:
            return f"Dataset {dataset_value} not found.", "", no_update, no_update, no_update, no_update, no_update

    # Handle save button
    if triggered_id == 'save-button' and save_n_clicks > 0 and prompt_value and selected_dataset_store:
        data_path = get_dataset_path(selected_dataset_store)
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            column_names = ", ".join(df.columns)
            first_two_rows = df.head(2).to_string(index=False)
            modified_prompt = f"Dataset: {selected_dataset_store}\n\nDataset columns: {column_names}\n\nFirst two rows:\n{first_two_rows}\n\nPrompt: {prompt_value}"
            response = tlm.prompt(modified_prompt)
            new_answer_input_value = response["response"]

    # Handle submit button
    if triggered_id == 'submit-button' and submit_n_clicks > 0 and answer_input_value and selected_dataset_store:
        data_path = get_dataset_path(selected_dataset_store)
        if os.path.exists(data_path):
            data = pd.read_csv(data_path)
            try:
                modified_code = answer_input_value.replace("housing", "df")
                exec(modified_code, {'df': data, 'plt': plt, 'pd': pd})

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                image_base64 = base64.b64encode(buf.read()).decode('utf-8')
                plt.close()

                new_prompt_div = html.Div([html.P(prompt_value, style={'text-align': 'center'})], style={'flex': '1', 'padding': '10px'})
                new_chart_div = html.Div([html.Img(src=f'data:image/png;base64,{image_base64}')], style={'flex': '1', 'padding': '10px'})
                delete_button = html.Button('Delete', id={'type': 'delete-button', 'index': len(full_history)}, n_clicks=0)

                new_entry = html.Div([new_prompt_div, new_chart_div, delete_button], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'})

                if initial_chart_present:
                    new_combined_history = [new_entry]
                    new_full_history = [new_entry]
                    new_initial_chart_store = False  # Set the flag to False after removing the initial entry
                else:
                    new_combined_history = [new_entry] + history_children
                    new_full_history = [new_entry] + full_history
            except Exception as e:
                return no_update, no_update, no_update, [html.Div(f"An error occurred while plotting the chart: {str(e)}")] + history_children, no_update, no_update, no_update
        else:
            return no_update, no_update, no_update, [html.Div(f"Dataset {selected_dataset_store} not found.")] + history_children, no_update, no_update, no_update

    # Handle delete button
    if 'delete-button' in triggered_id:
        index = int(triggered_id.split(':')[1].split(',')[0])
        deleted_entry = new_combined_history.pop(len(new_combined_history) - 1 - index)
        new_deleted_history.append(deleted_entry)

    # Handle clear history button
    if triggered_id == 'clear-history-button' and clear_n_clicks > 0:
        new_combined_history = []
        new_deleted_history = history_children

    # Handle restore history button
    if triggered_id == 'restore-history-button' and restore_n_clicks > 0:
        new_combined_history = new_full_history
        new_deleted_history = []

    return no_update, no_update, new_answer_input_value, new_combined_history, new_initial_chart_store, new_full_history, new_deleted_history
