import tensorflow as tf
import numpy as np
import os
import time

directory = os.getcwd()
path_to_file = tf.keras.utils.get_file('text_data', "file:\\" + directory + "\\text_data.txt")
text = open(path_to_file, 'rb').read().decode(encoding='utf-8')

print(f'Length of text: {len(text)} characters')

print(text[:250])
