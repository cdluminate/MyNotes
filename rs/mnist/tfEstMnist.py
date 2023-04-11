'''
https://www.tensorflow.org/tutorials/estimators/cnn
'''
import os
import sys

import numpy as np
import tensorflow as tf


tf.flags.DEFINE_string('model_dir', 'XXX', 'where to put the model')
tf.flags.DEFINE_integer('batch', 100, 'batch size')
tf.flags.DEFINE_bool('train', False, 'do training')
tf.flags.DEFINE_bool('validate', False, 'only validate the trained model')
tf.flags.DEFINE_bool('predict', False, 'do prediction')
tf.flags.DEFINE_integer('epochs', 40, 'max epochs to run')


def input_fn_builder(images, labels, shuffle):
    def input_fn():
        dataset = tf.data.Dataset.from_tensor_slices({
            'images': images, 'labels': labels})
        dataset = dataset.cache()
        if shuffle:
            dataset.shuffle(buffer_size=50000)
        return dataset.batch(tf.flags.FLAGS.batch).repeat(tf.flags.FLAGS.epochs)
    return input_fn


def cnn_model_fn(features, labels, mode):
    '''
    Model function for CNN.
    '''
    labels = features['labels']
    input_layer = tf.reshape(features["images"], [-1, 28, 28, 1])

    conv1 = tf.layers.conv2d(inputs=input_layer, filters=32, kernel_size=[5,5],
            padding="same", activation=tf.nn.relu)
    pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2,2], strides=2)

    conv2 = tf.layers.conv2d(inputs=pool1, filters=64, kernel_size=[5,5],
            padding="same", activation=tf.nn.relu)
    pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2,2], strides=2)

    pool2_flat = tf.reshape(pool2, [-1, 7*7*64])
    dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)
    dropout = tf.layers.dropout(inputs=dense, rate=0.4, training=(mode==tf.estimator.ModeKeys.TRAIN))

    logits = tf.layers.dense(inputs=dropout, units=10)

    predictions = {
        'classes': tf.argmax(input=logits, axis=1),
        'prob': tf.nn.softmax(logits, name='softmax_tensor')
        }

    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=1e-3)
        train_op = optimizer.minimize(loss=loss, global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

    elif mode == tf.estimator.ModeKeys.EVAL:
        eval_metric_ops = {
            'accuracy': tf.metrics.accuracy(labels=labels, predictions=predictions['classes'])
            }
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)

    else:
        raise NotImplementedError


def main(argv):

    # load data
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    y_train, y_test = y_train.astype(np.int32), y_test.astype(np.int32)

    # input functions
    train_input_fn = input_fn_builder(x_train, y_train, True)
    eval_input_fn = input_fn_builder(x_test, y_test, False)
    #train_input_fn = tf.estimator.inputs.numpy_input_fn(
    #        x={'images': x_train}, y=y_train, batch_size=100, num_epochs=tf.flags.FLAGS.epochs, shuffle=True)
    #eval_input_fn = tf.estimator.inputs.numpy_input_fn(
    #        x={'images': x_test}, y=y_test, num_epochs=1, shuffle=False)

    # build model
    estimator = tf.estimator.Estimator(model_fn=cnn_model_fn, model_dir=tf.flags.FLAGS.model_dir)

    # train / validate / predict
    if tf.flags.FLAGS.train:
        estimator.train(input_fn=train_input_fn)
        results = estimator.evaluate(input_fn=eval_input_fn)
        tf.logging.info(str(results))

    elif tf.flags.FLAGS.validate:
        results = estimator.evaluate(input_fn=eval_input_fn)
        tf.logging.info(str(results))

    elif tf.flags.FLAGS.predict:
        for result in estimator.predict(input_fn=eval_input_fn):
            tf.logging.info(result)

    else:
        tf.logging.warn('nothing to do')


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
