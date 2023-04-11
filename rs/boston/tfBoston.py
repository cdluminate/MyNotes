'''
https://www.tensorflow.org/tutorials/keras/basic_regression
'''
import tensorflow as tf
from tensorflow import keras

import numpy as np

boston = keras.datasets.boston_housing
(x_train, y_train), (x_test, y_test) = boston.load_data()

order = np.argsort(np.random.random(y_train.shape))
x_train, y_train = x_train[order], y_train[order]
print('Training set size', x_train.shape, y_train.shape)
print('Test set size', x_test.shape, y_test.shape)


mean = x_train.mean(axis=0)
std  = x_train.std(axis=0)
x_train = (x_train - mean) / std
x_test  = (x_test  - mean) / std

def createModel():
    model = keras.Sequential([
        keras.layers.Dense(64, activation=tf.nn.relu,
            input_shape=(x_train.shape[1],)),
        keras.layers.Dense(64, activation=tf.nn.relu),
        keras.layers.Dense(1),
        ])
    model.compile(optimizer=tf.train.RMSPropOptimizer(1e-3),
            loss='mse', metrics=['mae'])
    return model

model = createModel()
model.summary()

cp_callback = tf.keras.callbacks.ModelCheckpoint('checkpoints/cp.ckpt', save_weights_only=True, verbose=1)

model.fit(x_train, y_train, epochs=500, validation_split=0.2, verbose=1,
        callbacks=[cp_callback])


[loss, mae] = model.evaluate(x_test, y_test, verbose=1)
print('Test Result:', loss, mae)

model = createModel()
[loss, mae] = model.evaluate(x_test, y_test, verbose=1)
print('Raw Model Test Result:', loss, mae)

model.load_weights('checkpoints/cp.ckpt')
[loss, mae] = model.evaluate(x_test, y_test, verbose=1)
print('Pre-trained Model Test Result:', loss, mae)
