import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
import numpy as np
import os
import time


directory = os.getcwd()
path_to_file = tf.keras.utils.get_file('text_data', "file:\\" + directory + "\\text_data.txt")
text = open(path_to_file, 'rb').read().decode(encoding='utf-8')
sentences = pd.read_csv("all_sentences")

sentences = sentences.astype(str).values.flatten().tolist()


def get_training_sequences(sentences):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(sentences)
    tokenized_sentences = tokenizer.texts_to_sequences(sentences)
    training_sequences=[]
    for tokenized_sentence in tokenized_sentences:
        for word_number in range(1, len(tokenized_sentence)):
           partial_sentence = tokenized_sentence[:word_number+1]
           training_sequences.append(partial_sentence)
    return training_sequences       


def get_padded_sequences(training_sequences):
    max_length = max([len(x) for x in training_sequences])
    padded_sequences = pad_sequences(training_sequences, padding='post', truncating='post', maxlen=max_length)
    return padded_sequences

#input_sequences = np.array(train_padded)

print(get_padded_sequences(get_training_sequences(sentences)[:1]))