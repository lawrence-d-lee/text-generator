import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
import numpy as np
import os
import time
from text_generator import *

import dash
import flask
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

tokenized_sentences, num_words, tokenizer = tokenize(get_data())
padded_sequences, max_length = get_padded_sequences(
    get_training_sequences(tokenized_sentences)
)
predictors, targets = get_training_data(padded_sequences)
model = tf.keras.models.load_model("tensorflow_model")


server = flask.Flask(__name__)
app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        html.Div(
            children=[
                html.H1(
                    children="Estate Agent Text Generator", className="header-title"
                ),
                html.P(
                    children="Uses an LSTM (a type of neural network) to generate text in the style of estate agents. Click generate to see the results (it might take a few seconds).",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Button(id="generate_button", type="submit", children="Generate"),
        html.Div(id="output_text"),
    ]
)


@app.callback(Output("output_text", "children"), Input("generate_button", "n_clicks"))
def get_generated_text(click):
    if click is not None:
        random_word = generate_random_word(tokenizer, num_words)
        return text_generator(random_word, model, max_length, tokenizer)


if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=8050)
