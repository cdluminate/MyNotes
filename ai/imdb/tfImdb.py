'''
https://www.tensorflow.org/tutorials/keras/basic_text_classification
'''
import tensorflow as tf
from tensorflow import keras

import numpy as np

print('Using TF', tf.__version__)


imdb = keras.datasets.imdb
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=10000)
print('Training set size', x_train.shape, y_train.shape)
print('> data in variable length:', [len(x) for x in x_train[:10]])
print('Test set size', x_test.shape, y_test.shape)


vocab = imdb.get_word_index()
vocab = {k:(v+3) for (k, v) in vocab.items()}
vocab['<pad>'] = 0
vocab['<start>'] = 1
vocab['<unk>'] = 2
vocab['<unused>'] = 3
rvocab = dict([(v, k) for (k, v) in vocab.items()])

def decode(text):
    return ' '.join([rvocab.get(i, '?') for i in text])
print(decode(x_train[0]))


x_train = keras.preprocessing.sequence.pad_sequences(
        x_train, value=vocab['<pad>'], padding='post', maxlen=256)
x_test  = keras.preprocessing.sequence.pad_sequences(
        x_test, value=vocab['<pad>'], padding='post', maxlen=256)
print(x_train[0].shape, x_test[0].shape)


model = keras.Sequential()
model.add(keras.layers.Embedding(10000, 16))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation=tf.nn.relu))
model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))
model.summary()

model.compile(optimizer=tf.train.AdamOptimizer(),
        loss='binary_crossentropy',
        metrics=['accuracy'])

model.fit(x_train, y_train, epochs=40, batch_size=512, validation_data=(x_test, y_test), verbose=1)

print(model.evaluate(x_test, y_test))
