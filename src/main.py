from dash import Dash, html, dcc
from src import config
from src.Dataset import Dataset
from src.widgets import projection_radio_buttons, gallery, scatterplot, wordcloud, left_tab_radio_buttons, placeholder
from src.widgets.table import create_table
import dash_bootstrap_components as dbc

import callbacks.table
import callbacks.scatterplot
import callbacks.projection_radio_buttons
import callbacks.data_is_filtered
#import callbacks.left_tab_radio_buttons

def run_ui():
    external_stylesheets = [dbc.themes.BOOTSTRAP]
    app = Dash(__name__, external_stylesheets=external_stylesheets)

    projection_radio_buttons_widget = projection_radio_buttons.create_projection_radio_buttons()
    #left_tab_radio_buttons_widget = left_tab_radio_buttons.create_left_tab_radio_buttons()
    table_widget = create_table()
    scatterplot_widget = scatterplot.create_scatterplot(config.DEFAULT_PROJECTION)
    wordcloud_widget = wordcloud.create_wordcloud()
    gallery_widget = gallery.create_gallery()
    placeholder_widget = placeholder.create_placeholder()

    tabs = dcc.Tabs([
        dcc.Tab(label='table', children=[table_widget]),
        dcc.Tab(label='placeholder', children=placeholder_widget)
    ])

    app.layout = dbc.Container([
        html.Div(
            dbc.Stack(
                [
                    projection_radio_buttons_widget,
                    #left_tab_radio_buttons_widget
                ],
                direction='horizontal',
                gap=3,
                id='header-stack'),
            id='header'
        ),
        dbc.Row([
            dbc.Col(scatterplot_widget, width=True, className='main-col'),
            dbc.Col(wordcloud_widget, width='auto', align="center")],
            className='g-10 main-row', justify='between'),
        dbc.Row([
            dbc.Col(tabs, className='main-col', width=6),
            dbc.Col(gallery_widget, className='main-col', width=6)
        ], className='g-10 main-row')
    ], fluid=True, id='container')

    app.run(debug=True, use_reloader=False)


def main():
    if not Dataset.files_exist():
        print('File', config.AUGMENTED_DATASET_PATH, 'missing or directory', config.IMAGES_DIR, 'missing')
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
