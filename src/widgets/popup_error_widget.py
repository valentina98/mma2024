from dash import html, dcc
from utils import logger

def create_popup_error(error_message):
    logger.info(f"Popup error message: {error_message}")
    return html.Div([
        html.Div([
            dcc.ConfirmDialog(
                displayed=True,
                id='popup-message',
                message=error_message
            ),
        ], className='popup-content'),
    ], className='popup-overlay')

