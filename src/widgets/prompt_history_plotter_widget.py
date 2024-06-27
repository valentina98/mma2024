from dash.dependencies import Input, Output, State
import dash
from dash import dcc, html
import plotly.graph_objs as go

class PromptHistoryPlotter:
    def __init__(self):
        self.history = []

    def plot_initial(self, prompt, suggestion1, suggestion2, suggestion3):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[-0.25, 0.25],
            y=[prompt, prompt],
            mode='lines',
            line=dict(color='maroon', width=4),
            name='Prompt'
        ))
        fig.add_trace(go.Scatter(
            x=[0.75, 1.25],
            y=[suggestion1, suggestion1],
            mode='lines',
            line=dict(color='yellow', width=4),
            name='Suggestion 1'
        ))
        fig.add_trace(go.Scatter(
            x=[1.75, 2.25],
            y=[suggestion2, suggestion2],
            mode='lines',
            line=dict(color='pink', width=4),
            name='Suggestion 2'
        ))
        fig.add_trace(go.Scatter(
            x=[2.75, 3.25],
            y=[suggestion3, suggestion3],
            mode='lines',
            line=dict(color='blue', width=4),
            name='Suggestion 3'
        ))

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

        fig.add_trace(go.Scatter(
            x=[step, step],
            y=[low, high],
            mode='lines',
            line=dict(color=color, width=4),
            name=f'Prompt {step + 1} Vertical'
        ))
        fig.add_trace(go.Scatter(
            x=[step - 0.25, step],
            y=[initial_prompt_relevance, initial_prompt_relevance],
            mode='lines',
            line=dict(color=color, width=4),
            name=f'Prompt {step + 1} Left'
        ))
        fig.add_trace(go.Scatter(
            x=[step, step + 0.25],
            y=[selected_suggestion_relevance, selected_suggestion_relevance],
            mode='lines',
            line=dict(color=color, width=4),
            name=f'Prompt {step + 1} Right'
        ))

        return fig

    def plot_intermediate(self, step, suggestions):
        fig = go.Figure()

        for idx, (prev_prompt, _, selected) in enumerate(self.history):
            fig = self.plot_collapsed(fig, prev_prompt, *self.history[idx][1], selected, idx)

        fig.add_trace(go.Scatter(
            x=[step + 0.75, step + 1.25],
            y=[suggestions[0], suggestions[0]],
            mode='lines',
            line=dict(color='yellow', width=4),
            name='Suggestion 1'
        ))
        fig.add_trace(go.Scatter(
            x=[step + 1.75, step + 2.25],
            y=[suggestions[1], suggestions[1]],
            mode='lines',
            line=dict(color='pink', width=4),
            name='Suggestion 2'
        ))
        fig.add_trace(go.Scatter(
            x=[step + 2.75, step + 3.25],
            y=[suggestions[2], suggestions[2]],
            mode='lines',
            line=dict(color='blue', width=4),
            name='Suggestion 3'
        ))

        fig.update_layout(
            xaxis=dict(
                tickvals=list(range(step + 4)),
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

        fig.add_trace(go.Scatter(
            x=[step + 0.75, step + 1.25],
            y=[suggestions[0], suggestions[0]],
            mode='lines',
            line=dict(color='yellow', width=4),
            name='Suggestion 1'
        ))
        fig.add_trace(go.Scatter(
            x=[step + 1.75, step + 2.25],
            y=[suggestions[1], suggestions[1]],
            mode='lines',
            line=dict(color='pink', width=4),
            name='Suggestion 2'
        ))
        fig.add_trace(go.Scatter(
            x=[step + 2.75, step + 3.25],
            y=[suggestions[2], suggestions[2]],
            mode='lines',
            line=dict(color='blue', width=4),
            name='Suggestion 3'
        ))

        fig.update_layout(
            xaxis=dict(
                tickvals=list(range(step + 5)),
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
