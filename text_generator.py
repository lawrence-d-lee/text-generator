import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
import numpy as np
import os
import time


#directory = os.getcwd()
#path_to_file = tf.keras.utils.get_file('text_data', "file:\\" + directory + "\\text_data.txt")
#text = open(path_to_file, 'rb').read().decode(encoding='utf-8')

def get_data():
    sentences = pd.read_csv("all_sentences")
    sentences = sentences.astype(str).values.flatten().tolist()
    return sentences

def tokenize(sentences):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(sentences)
    tokenized_sentences = tokenizer.texts_to_sequences(sentences)
    num_words = len(tokenizer.word_index)
    return tokenized_sentences, num_words

def get_training_sequences(tokenized_sentences):
    training_sequences=[]
    for tokenized_sentence in tokenized_sentences:
        for word_number in range(1, len(tokenized_sentence)):
           partial_sentence = tokenized_sentence[:word_number+1]
           training_sequences.append(partial_sentence)
    return training_sequences       


def get_padded_sequences(training_sequences):
    max_length = max([len(x) for x in training_sequences])
    padded_sequences = np.array(pad_sequences(training_sequences, padding='pre', maxlen=max_length))
    return padded_sequences, max_length


def get_training_data(padded_sequences):
    predictors = padded_sequences[:, :-1]
    targets = padded_sequences[:, -1]
    return predictors, targets


def build_model(num_words, max_length):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Embedding(num_words+1, 10, input_length=max_length-1))
    model.add(tf.keras.layers.LSTM(128))
    model.add(tf.keras.layers.Dense(num_words+1, activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam')
    return model

tokenized_sentences, num_words = tokenize(get_data())
padded_sequences, max_length = get_padded_sequences(get_training_sequences(tokenized_sentences))
predictors, targets = get_training_data(padded_sequences)
model = build_model(num_words, max_length)
print(model.summary())
model.fit(predictors, targets, epochs=20)