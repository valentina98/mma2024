# src/widgets/prompt_history_plotter_widget.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

class PromptHistoryPlotter:
    def __init__(self):
        self.history = []

    def plot_initial(self, prompt, suggestion1, suggestion2, suggestion3):
        fig = go.Figure()
        fig.add_hline(y=prompt, line_color="maroon", line_width=4, x0=-0.25, x1=0.25)
        fig.add_hline(y=suggestion1, line_color="yellow", line_width=4, x0=0.75, x1=1.25)
        fig.add_hline(y=suggestion2, line_color="pink", line_width=4, x0=1.75, x1=2.25)
        fig.add_hline(y=suggestion3, line_color="blue", line_width=4, x0=2.75, x1=3.25)

        fig.update_layout(
            title='Prompt and Suggestions',
            xaxis=dict(
                tickvals=[0, 1, 2, 3],
                ticktext=['Prompt 1', 'Suggestion 1', 'Suggestion 2', 'Suggestion 3']
            ),
            yaxis=dict(range=[0, 1]),
            showlegend=False
        )

        return fig

    def plot_collapsed(self, fig, prompt, suggestion1, suggestion2, suggestion3, selected_suggestion, step):
        initial_prompt_relevance = prompt
        selected_suggestion_relevance = selected_suggestion
        low = min(initial_prompt_relevance, selected_suggestion_relevance)
        high = max(initial_prompt_relevance, selected_suggestion_relevance)
        
        color = 'green' if selected_suggestion_relevance > initial_prompt_relevance else 'red'

        fig.add_vline(x=step, line_color=color, line_width=4, y0=low, y1=high)
        fig.add_hline(y=initial_prompt_relevance, line_color=color, line_width=4, x0=step-0.25, x1=step)
        fig.add_hline(y=selected_suggestion_relevance, line_color=color, line_width=4, x0=step, x1=step+0.25)

        return fig

    def plot_intermediate(self, step, suggestions):
        fig = go.Figure()

        for idx, (prev_prompt, _, selected) in enumerate(self.history):
            fig = self.plot_collapsed(fig, prev_prompt, *self.history[idx][1], selected, idx)

        fig.add_hline(y=suggestions[0], line_color="yellow", line_width=4, x0=step + 0.75, x1=step + 1.25)
        fig.add_hline(y=suggestions[1], line_color="pink", line_width=4, x0=step + 1.75, x1=step + 2.25)
        fig.add_hline(y=suggestions[2], line_color="blue", line_width=4, x0=step + 2.75, x1=step + 3.25)

        fig.update_layout(
            xaxis=dict(
                tickvals=list(range(step + 4)),  # Convert range to list
                ticktext=[f'Prompt {i+1}' for i in range(step + 1)] + [f'Suggestion {i}' for i in range(1, 4)]
            ),
            yaxis=dict(range=[0, 1]),
            showlegend=False
        )

        return fig

    def plot_final(self, step, suggestions, selected_suggestion):
        fig = go.Figure()

        for idx, (prev_prompt, _, selected) in enumerate(self.history):
            fig = self.plot_collapsed(fig, prev_prompt, *self.history[idx][1], selected, idx)

        fig = self.plot_collapsed(fig, self.history[-1][0], *suggestions, selected_suggestion, step)

        fig.add_hline(y=suggestions[0], line_color="yellow", line_width=4, x0=step + 0.75, x1=step + 1.25)
        fig.add_hline(y=suggestions[1], line_color="pink", line_width=4, x0=step + 1.75, x1=step + 2.25)
        fig.add_hline(y=suggestions[2], line_color="blue", line_width=4, x0=step + 2.75, x1=step + 3.25)

        fig.update_layout(
            xaxis=dict(
                tickvals=list(range(step + 5)),  # Convert range to list
                ticktext=[f'Prompt {i+1}' for i in range(step + 2)] + [f'Suggestion {i}' for i in range(1, 4)]
            ),
            yaxis=dict(range=[0, 1]),
            showlegend=False
        )

        return fig

    def plot_sequence(self, initial_prompt, initial_suggestions, subsequent_suggestions_and_selections):
        fig = self.plot_initial(initial_prompt, *initial_suggestions)
        
        self.history.append((initial_prompt, initial_suggestions, None))

        for step, (suggestions, selected_suggestion) in enumerate(subsequent_suggestions_and_selections, start=1):
            previous_prompt = self.history[-1][2] if self.history[-1][2] is not None else initial_prompt
            self.history[-1] = (previous_prompt, self.history[-1][1], selected_suggestion)
            fig = self.plot_intermediate(step, suggestions)
            self.history.append((selected_suggestion, suggestions, selected_suggestion))
            fig = self.plot_final(step, suggestions, selected_suggestion)

        return fig

def create_prompt_history_chart(initial_prompt, initial_suggestions, subsequent_suggestions_and_selections):
    plotter = PromptHistoryPlotter()
    fig = plotter.plot_sequence(initial_prompt, initial_suggestions, subsequent_suggestions_and_selections)
    return html.Div(dcc.Graph(figure=fig))

# Example usage in the widget file
chart_data = {
    'initial_prompt': 0.8,
    'initial_suggestions': [0.2, 0.4, 0.6],
    'subsequent_suggestions_and_selections': [
        ([0.5, 0.7, 0.9], 0.6),
        ([0.65, 0.85, 0.95], 0.9)
    ]
}
