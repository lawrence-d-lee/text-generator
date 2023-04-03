import tensorflow as tf
import numpy as np
import os
import time

directory = os.getcwd()
path_to_file = tf.keras.utils.get_file('text_data', "file:\\" + directory + "\\text_data.txt")
text = open(path_to_file, 'rb').read().decode(encoding='utf-8')

#print(f'Length of text: {len(text)} characters')

#print(text[:250])

vocab = sorted(set(text))
#print(f'{len(vocab)} unique characters')
#print(vocab)

ids_from_chars = tf.keras.layers.StringLookup(
    vocabulary=list(vocab), mask_token=None)

chars_from_ids = tf.keras.layers.StringLookup(
    vocabulary=ids_from_chars.get_vocabulary(), invert=True, mask_token=None)

all_ids = ids_from_chars(tf.strings.unicode_split(text, 'UTF-8'))
#all_ids
ids_dataset = tf.data.Dataset.from_tensor_slices(all_ids)

for ids in ids_dataset.take(10):
    print(chars_from_ids(ids).numpy().decode('utf-8'))
