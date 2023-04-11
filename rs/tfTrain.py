#!/usr/bin/env python3
'''
Neural Network Replays with the unholy TensorFlow2.X
Copyright (C) 2019 M. Zhou
'''
import os
import sys
import json
import argparse
import numpy as np
import Color as C
import tensorflow as tf  # requires tensorflow 2.0
os.putenv('TF_CPP_MIN_LOG_LEVEL', '1')  # have TF shutup


def fashion_kr_cnn():
    '''
    Fashion-MNIST | keras API | CNN model
    '''
    (train_images, train_labels), (test_images, test_labels) = \
        tf.keras.datasets.fashion_mnist.load_data()
    train_images = train_images.reshape((60000, 28, 28, 1))
    test_images = test_images.reshape((10000, 28, 28, 1))
    train_images = train_images / 255.0
    test_images = test_images / 255.0

    strategy = tf.distribute.MirroredStrategy() # will use all the GPUs that are visible to TensorFlow
    with strategy.scope():
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Conv2D(
            32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
        model.add(tf.keras.layers.MaxPooling2D((2, 2)))
        model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(tf.keras.layers.MaxPooling2D((2, 2)))
        model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(64, activation='relu'))
        model.add(tf.keras.layers.Dense(10, activation='softmax'))

        model.compile(optimizer=tf.keras.optimizers.Adam(),
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
    model.summary()

    model.fit(train_images, train_labels, epochs=5,
              validation_data=(test_images, test_labels))
    model.save_weights('fashion_kr_cnn.tfw')


def fashion_kr_mlp():
    '''
    Fashion-MNIST | keras API | MLP model
    '''
    (train_images, train_labels), (test_images, test_labels) = \
        tf.keras.datasets.fashion_mnist.load_data()
    train_images = train_images / 255.0
    test_images = test_images / 255.0

    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.summary()

    model.fit(train_images, train_labels, epochs=10,
              validation_data=(test_images, test_labels),
              callbacks=[
                  tf.keras.callbacks.ModelCheckpoint(filepath='fashion_kr_mlp.ckpt',
                                                     save_weights_only=True, verbose=0)
              ]
              )
    # load with model.load_weights(...)
    model.save_weights('fashion_kr_mlp.tfw')
    #test_loss, test_acc = model.evaluate(test_images, test_labels)
    #print('\nTest accuracy:', test_acc)
    #predictions = model.predict(test_images)
    # print(predictions)


def mnist_kr_mlp():
    '''
    MNIST | keras API | MLP model
    '''
    mnist = tf.keras.datasets.mnist

    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=5)

    model.evaluate(x_test, y_test)


def mnist_tf_mlp():
    '''
    MNIST | TF2 API | MLP model
    '''
    mnist = tf.keras.datasets.mnist

    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    # Add a channels dimension
    x_train = x_train[..., tf.newaxis]
    x_test = x_test[..., tf.newaxis]

    train_ds = tf.data.Dataset.from_tensor_slices(
        (x_train, y_train)).shuffle(10000).batch(32)

    test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32)

    class MyModel(tf.keras.Model):
        def __init__(self):
            super(MyModel, self).__init__()
            self.conv1 = tf.keras.layers.Conv2D(32, 3, activation='relu')
            self.flatten = tf.keras.layers.Flatten()
            self.d1 = tf.keras.layers.Dense(128, activation='relu')
            self.d2 = tf.keras.layers.Dense(10, activation='softmax')

        def call(self, x):
            x = self.conv1(x)
            x = self.flatten(x)
            x = self.d1(x)
            return self.d2(x)

    # Create an instance of the model
    model = MyModel()

    loss_object = tf.keras.losses.SparseCategoricalCrossentropy()

    optimizer = tf.keras.optimizers.Adam()

    train_loss = tf.keras.metrics.Mean(name='train_loss')
    train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(
        name='train_accuracy')

    test_loss = tf.keras.metrics.Mean(name='test_loss')
    test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(
        name='test_accuracy')

    @tf.function
    def train_step(images, labels):
        with tf.GradientTape() as tape:
            predictions = model(images)
            loss = loss_object(labels, predictions)
        gradients = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))

        train_loss(loss)
        train_accuracy(labels, predictions)

    @tf.function
    def test_step(images, labels):
        predictions = model(images)
        t_loss = loss_object(labels, predictions)

        test_loss(t_loss)
        test_accuracy(labels, predictions)

    EPOCHS = 5

    for epoch in range(EPOCHS):
        for images, labels in train_ds:
            train_step(images, labels)

        for test_images, test_labels in test_ds:
            test_step(test_images, test_labels)

        template = 'Epoch {}, Loss: {}, Accuracy: {}, Test Loss: {}, Test Accuracy: {}'
        print(template.format(epoch+1,
                              train_loss.result(),
                              train_accuracy.result()*100,
                              test_loss.result(),
                              test_accuracy.result()*100))

        # Reset the metrics for the next epoch
        train_loss.reset_states()
        train_accuracy.reset_states()
        test_loss.reset_states()
        test_accuracy.reset_states()


if __name__ == '__main__':

    ag = argparse.ArgumentParser()
    ag.add_argument('-M', '--model', type=str, required=True,
            choices=['mnist_kr_mlp', 'mnist_tf_mlp',
                'fashion_kr_mlp', 'fashion_kr_cnn'
                ])
    ag = ag.parse_args(sys.argv[1:])
    print(C.fgOrange(vars(ag)))
    print(C.fgOrange("GPU Available: ", tf.test.is_gpu_available()))

    eval(ag.model)()
