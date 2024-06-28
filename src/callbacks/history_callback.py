from dash import callback, html, Output, Input, State, no_update, dcc, ctx
from dash.dependencies import ALL
import pandas as pd
import os
import matplotlib.pyplot as plt
import io
import base64
from utils import get_dataset_path, logger
from src.widgets.history_widget import create_new_entry, create_error
from utils import generate_chart

@callback(
    [Output('combined-history', 'children'),
     Output('initial-chart-store', 'data'),
     Output('full-history-store', 'data'),
     Output('deleted-history-store', 'data'),
     Output('ohls-chart', 'children')],
    [Input('save-button', 'n_clicks'),
     Input({'type': 'delete-button', 'index': ALL}, 'n_clicks'),
     Input('clear-history-button', 'n_clicks'),
     Input('restore-history-button', 'n_clicks')],
    [State('prompt-input', 'value'),
     State('prompt-score', 'children'),
     State('selected-dataset-store', 'data'),
     State('answer-input', 'value'),
     State('combined-history', 'children'),
     State('initial-chart-store', 'data'),
     State('full-history-store', 'data'),
     State('deleted-history-store', 'data')],
    prevent_initial_call=True
)
def manage_history(save_n_clicks, delete_n_clicks, clear_n_clicks, restore_n_clicks,
                   prompt_value, prompt_score, selected_dataset_store, answer_input_value, history_children, initial_chart_present, full_history, deleted_history):
    
    if not ctx.triggered:
        return no_update, no_update, no_update, no_update, no_update

    # triggered_index = ctx.triggered_id['index'] # Can we use this instead of the below?
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    new_combined_history = history_children
    new_initial_chart_store = initial_chart_present
    new_full_history = full_history
    new_deleted_history = deleted_history
    new_ohlc_chart = no_update

    # Handle submit button
    if triggered_id == 'save-button' and save_n_clicks > 0 and answer_input_value and selected_dataset_store:
        try:
            # modified_code = answer_input_value.replace("housing", "df") # ToDo: do we need that
            fig = generate_chart(answer_input_value, selected_dataset_store)

            new_entry = create_new_entry(prompt_score, prompt_value, fig, len(full_history))

            if initial_chart_present:
                new_combined_history = [new_entry]
                new_full_history = [new_entry]
                new_initial_chart_store = False  # Set the flag to False after removing the initial entry
            else:
                new_combined_history = [new_entry] + history_children
                new_full_history = [new_entry] + full_history
        except Exception as e:
            return no_update, no_update, no_update, no_update, no_update, [create_error(str(e))] + history_children
        
    # Handle delete button
    if 'delete-button' in triggered_id:
        index = int(triggered_id.split(':')[1].split(',')[0])
        deleted_entry = new_combined_history.pop(len(new_combined_history) - 1 - index)
        new_deleted_history.append(deleted_entry)
        if initial_chart_present and not new_combined_history:
            new_initial_chart_store = True

    # Handle clear history button
    if triggered_id == 'clear-history-button' and clear_n_clicks > 0:
        new_combined_history = []
        new_deleted_history = history_children

    # Handle restore history button
    if triggered_id == 'restore-history-button' and restore_n_clicks > 0:
        if not full_history:
            new_combined_history = new_deleted_history
        else:
            new_combined_history = new_full_history + new_deleted_history
        new_deleted_history = []

    return new_combined_history, new_initial_chart_store, new_full_history, new_deleted_history, new_ohlc_chart
