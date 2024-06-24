import os
import io
import base64
import logging
import pandas as pd
import matplotlib.pyplot as plt
import textwrap
import plotly.graph_objects as go
from dash import dcc, html
from openai import OpenAI
from cleanlab_studio import Studio
from dotenv import load_dotenv
import ast

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize clients based on environment variables
USE_OPEN_AI = os.getenv("USE_OPEN_AI", "false").lower() == "true"
CALCULATE_SCORES = os.getenv("CALCULATE_SCORES", "false").lower() == "true"
openai_client = None
tlm_client = None

if USE_OPEN_AI:
    openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
else:
    studio = Studio(api_key=os.environ.get("TLM_API_KEY"))
    tlm_client = studio.TLM()


def get_dataset_path(dataset_name):
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../dataset/ourdata'))
    return os.path.join(base_path, f'{dataset_name}.csv')


def load_dataset(dataset_name):
    data_path = get_dataset_path(dataset_name)
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    raise Exception(f"Dataset {dataset_name} not found")


def send_prompt(client, prompt, max_tokens):
    if USE_OPEN_AI:
        logger.info(f"Sending prompt to OpenAI: {prompt}")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
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


def get_code(prompt, df, dataset_name):
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
        return send_prompt(openai_client if USE_OPEN_AI else tlm_client, code_prompt, 150)
    except Exception as e:
        return e

def get_trustworthiness_score(prompt):
    if CALCULATE_SCORES:
        return tlm_client.prompt(prompt)["trustworthiness_score"]
    return ""


def get_suggestions(prompt):
    improvement_prompt = (
        "An LLM will be provided with the following prompt and a dataset. "
        "Your goal is to improve the prompt so that the LLM returns a more accurate response. "
        "Provide 3 different suggestions how to improve the prompt keeping the same information. "
        "You should return only 1 line containing an array of suggestions and nothing else. "
        "Example response: ['Plot a bar chart', 'Generate a pie chart', 'Plot a visualization'] "
        f"Prompt: {prompt}"
    )

    suggestions_response = send_prompt(openai_client if USE_OPEN_AI else tlm_client, improvement_prompt, 100)
    try:
        return ast.literal_eval(suggestions_response)
    except Exception as e:
        return e


def get_code_and_suggestions(prompt, dataset_name):

    df = load_dataset(dataset_name)

    try:
        code = get_code(prompt, df, dataset_name)
        logger.info(f"Code received: {code}")

        trustworthiness_score = get_trustworthiness_score(prompt)
        logger.info(f"Trustworthiness score: {trustworthiness_score}")

        suggestions_array = get_suggestions(prompt)
        suggestions = []
        for suggestion in suggestions_array:
            suggestion_code = get_code(suggestion, df, dataset_name)
            suggestion_trustworthiness_score = get_trustworthiness_score(suggestion)
            suggestions.append((suggestion, suggestion_trustworthiness_score, suggestion_code))
            logger.info(f"Suggestion code received: {suggestion_code}")

        return code, trustworthiness_score, suggestions

    except Exception as e:
        logger.exception(f"Error getting suggestions: {e}")
        return "", "", []


def generate_chart(code_str, dataset_name):
    try:
        data = load_dataset(dataset_name)

        plt.close('all')

        code_str = textwrap.dedent(code_str)

        local_namespace = {
            'pd': pd,
            'plt': plt,
            'data': data
        }

        exec(code_str, {}, local_namespace)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)

        img_base64 = base64.b64encode(buf.read()).decode('ascii')
        buf.close()

        fig = go.Figure()
        fig.add_layout_image(
            dict(
                source='data:image/png;base64,' + img_base64,
                xref="paper", yref="paper",
                x=0, y=1, 
                sizex=1, sizey=1,
                xanchor="left",
                yanchor="top",
                sizing="contain",
                layer="below"
            )
        )

        fig.update_xaxes(visible=False, range=[0, 1])
        fig.update_yaxes(visible=False, range=[0, 1])
        fig.update_layout(
            title="Chart",
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor="white",
            plot_bgcolor="white"
        )

        return fig

    except Exception as e:
        error_message = f"An error occurred while plotting the chart: {str(e)}"
        fig = go.Figure()
        fig.add_annotation(
            text=error_message,
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(color="red", size=14)
        )
        fig.update_layout(
            title="Error",
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        return fig

def encode_image(image):
    image_base64 = base64.b64encode(image).decode('utf-8')
    return f'data:image/png;base64,{image_base64}'


