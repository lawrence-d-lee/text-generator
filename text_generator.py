import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
import numpy as np
import random


def get_data():
    sentences = pd.read_csv("all_sentences")
    sentences = sentences.astype(str).values.flatten().tolist()
    return sentences


def tokenize(sentences):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(sentences)
    tokenized_sentences = tokenizer.texts_to_sequences(sentences)
    num_words = len(tokenizer.word_index)
    return tokenized_sentences, num_words, tokenizer


def get_training_sequences(tokenized_sentences):
    training_sequences = []
    for tokenized_sentence in tokenized_sentences:
        for word_number in range(1, len(tokenized_sentence)):
            partial_sentence = tokenized_sentence[: word_number + 1]
            training_sequences.append(partial_sentence)
    return training_sequences


def get_padded_sequences(training_sequences):
    max_length = max([len(x) for x in training_sequences])
    padded_sequences = np.array(
        pad_sequences(training_sequences, padding="pre", maxlen=max_length)
    )
    return padded_sequences, max_length


def get_training_data(padded_sequences):
    predictors = padded_sequences[:, :-1]
    targets = padded_sequences[:, -1]
    return predictors, targets


def build_model(num_words, max_length):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Embedding(num_words + 1, 10, input_length=max_length - 1))
    model.add(tf.keras.layers.LSTM(128))
    model.add(tf.keras.layers.Dense(num_words + 1, activation="softmax"))
    model.compile(loss="sparse_categorical_crossentropy", optimizer="adam")
    return model


tokenized_sentences, num_words, tokenizer = tokenize(get_data())
padded_sequences, max_length = get_padded_sequences(
    get_training_sequences(tokenized_sentences)
)
predictors, targets = get_training_data(padded_sequences)

# model = build_model(num_words, max_length)
# model.fit(predictors, targets, epochs=20)

model = tf.keras.models.load_model("tensorflow_model")


def generate_random_word(tokenizer, num_words):
    word_list = list(tokenizer.word_index.keys())
    word_counts = tokenizer.word_counts
    random_word_count = 0
    while random_word_count < 100:
        random_number = random.randint(0, num_words)
        random_word = word_list[random_number]
        random_word_count = word_counts[random_word]
        print(random_word, random_word_count)
    return random_word


def text_generator(seed, model, max_length, tokenizer):
    for word_number in range(30):
        list_of_tokens = tokenizer.texts_to_sequences([seed])[0]
        padded_list = pad_sequences(
            [list_of_tokens], maxlen=max_length - 1, padding="pre"
        )
        prediction = np.argmax(model.predict(padded_list), axis=-1)
        next_word = ""
        for word, index in tokenizer.word_index.items():
            if index == prediction:
                next_word = word
                break
        seed += " " + next_word
    return seed.capitalize()
