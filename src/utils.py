import os
import io
import base64
import logging
import pandas as pd
import matplotlib.pyplot as plt
import textwrap
import plotly.graph_objects as go
from openai import OpenAI
from cleanlab_studio import Studio
from dotenv import load_dotenv
import ast
from src import config
import random

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

openai_client = None
tlm_client = None

if config.USE_OPEN_AI:
    openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

if not config.USE_OPEN_AI or config.CALCULATE_SCORES:
    studio = Studio(api_key=os.environ.get("TLM_API_KEY"))
    tlm_client = studio.TLM()


def get_dataset_path(dataset_name):
    return os.path.join(config.DATA_PATH, f'{dataset_name}.csv')


def load_dataset(dataset_name):
    data_path = get_dataset_path(dataset_name)
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    raise Exception(f"Dataset {dataset_name} not found")


def send_prompt(client, prompt, max_tokens):
    if config.USE_OPEN_AI:
        logger.info(f"Sending prompt to OpenAI: {prompt}")
        response = client.chat.completions.create(
            model=config.OPEN_AI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    else:
        logger.info(f"Sending prompt to TLM: {prompt}")
        return client.prompt(prompt)["response"]


def get_code(prompt, dataset_name):
    df = load_dataset(dataset_name)
    code_prompt = (
        f"Dataset: {dataset_name}\n\nContext: {df.head(2).to_string(index=False)}\n\nPrompt: "
        "You are an AI that strictly conforms to responses in Python code. "
        "Your responses consist of valid python syntax, with no other comments, explanations, reasoning, or dialogue not consisting of valid python. "
        "If you have any comments or remarks they will have a # in front of it. It has to be strict python code. "
        "Use the dataset name, column names, and dataset itself as context for the correct visualization. The code implementation should make use of the correct variable names. "
        "The dataset is already loaded as df. "
        f"{prompt}"
        "Provide only Python code, do not give any reaction other than the code itself, no yapping, no certainly, no nothing like strings, only the code. "
    )
    try: 
        response = send_prompt(openai_client if config.USE_OPEN_AI else tlm_client, code_prompt, 150)
        # Match the code between ```python and ``` in the response or return the full response
        code = response.split("```python")[1].split("```")[0].strip() if "```python" in response else response.strip()
        logger.info(f"Code received: {code}")
        return code
    except Exception as e:
        return e

def get_trustworthiness_score(prompt):
    if config.CALCULATE_SCORES:
        trustworthiness_score = tlm_client.prompt(prompt)["trustworthiness_score"]
        logger.info(f"Trustworthiness score: {trustworthiness_score}")
        return trustworthiness_score
    else:
        # Return a value berween 0 and 1
        return random.random()


def get_suggestions(prompt, dataset_name):
    df = load_dataset(dataset_name)
    # ToDo: Add 2 lines from the dataset in the suggestion prompt?
    improvement_prompt = (
        "An LLM will be provided with the following prompt and a dataset. "
        "Your goal is to improve the prompt so that the LLM returns a more accurate response. "
        "Provide 3 different suggestions how to improve the prompt keeping the same information. "
        "You should return only 1 line containing an array of suggestions and nothing else. "
        "Example response: ['Plot a bar chart', 'Generate a pie chart', 'Plot a visualization'] "
        f"Prompt: {prompt}"
    )
    suggestions_response = send_prompt(openai_client if config.USE_OPEN_AI else tlm_client, improvement_prompt, 100)
    suggestions_array = ast.literal_eval(suggestions_response)
    suggestions = []
    for suggestion in suggestions_array:
        suggestion_code = get_code(suggestion, dataset_name)
        suggestion_trustworthiness_score = get_trustworthiness_score(suggestion)
        suggestions.append((suggestion, suggestion_trustworthiness_score, suggestion_code))
        logger.info(f"Suggestion code received: {suggestion_code}")
    return suggestions


def generate_chart(code_str, dataset_name):
    try:
        df = load_dataset(dataset_name)

        # Create an image from the code and save it in the buffer
        plt.close('all')
        code_str = textwrap.dedent(code_str)  # Dedent the code string to remove leading spaces
        exec(code_str, {'df': df, 'plt': plt, 'pd': pd})
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        # Create a Plotly figure with the image
        fig = go.Figure()
        fig.add_layout_image(
            dict(
                source='data:image/png;base64,' + img_base64,
                x=0.5, y=0.5,
                xanchor="center",
                yanchor="middle",
                xref="paper", yref="paper",
                sizex=1, sizey=1,
                sizing="contain",
                layer="below"
            )
        )
        fig.update_layout(
            xaxis=dict(visible=False, range=[0, 1]),
            yaxis=dict(visible=False, range=[0, 1]),
            margin=dict(l=5, r=5, t=5, b=5),
            paper_bgcolor="white",
            plot_bgcolor="white"
        )

        return fig

    except Exception as e:
        logger.exception(f"Error generating chart: {e}")
        error_message = f"An error occurred while plotting the chart: {str(e)}"
        
        # Wrap the error message to fit within the figure
        wrapped_error_message = "<br>".join(textwrap.wrap(error_message, width=20))

        fig = go.Figure()
        fig.add_annotation(
            text=wrapped_error_message,
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(color="red", size=8),
            align="center"
        )
        fig.update_layout(
            xaxis=dict(visible=False, range=[0, 1]),
            yaxis=dict(visible=False, range=[0, 1]),
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        
        return fig
    

# def encode_image(image):
#     image_base64 = base64.b64encode(image).decode('utf-8')
#     return f'data:image/png;base64,{image_base64}'


