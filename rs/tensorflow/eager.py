'''
https://www.tensorflow.org/tutorials/eager/custom_training
'''
import tensorflow as tf
import numpy as np

tf.enable_eager_execution()

class Model(object):
    def __init__(self):
        self.w = tf.Variable(5.0)
        self.b = tf.Variable(0.0)
    def __call__(self, x):
        return self.w * x + self.b

model = Model()
assert model(3.0).numpy() == 15.0

def loss(yhat, y):
    return tf.reduce_mean(tf.square(yhat - y))

inputs = tf.random_normal(shape=[1000])
noise  = tf.random_normal(shape=[1000])
outputs = inputs * 3.0 + 2.0 + noise

print('Initial loss:', loss(model(inputs), outputs))


def train(model, inputs, outputs, lr):
    with tf.GradientTape() as t:
        cur_loss = loss(model(inputs), outputs)
    dw, db = t.gradient(cur_loss, [model.w, model.b])
    model.w.assign_sub(lr * dw)
    model.b.assign_sub(lr * db)

for eph in range(20):
    cur_loss = loss(model(inputs), outputs)
    train(model, inputs, outputs, lr=1e-1)
    print(f'Eph[{eph}] loss={cur_loss} w={model.w.numpy()} b={model.b.numpy()}')
