from dash import callback, Output, Input
from src.widgets import dataset_selection_widget
from utils import logger, load_dataset

# Callback to update the dataset table based on selected dataset
@callback(
    [Output('dataset-table', 'children'),
     Output('selected-dataset-store', 'data')],
    Input('dataset-dropdown', 'value'),
    prevent_initial_call=True
)
def table_selected(selected_dataset):
    logger.info(f"Updating table for dataset: {selected_dataset}")
    if selected_dataset:
        data = load_dataset(selected_dataset)
        logger.info(f"Dataset {selected_dataset} loaded successfully")
        return dataset_selection_widget.create_table(data), selected_dataset
    return "", ""