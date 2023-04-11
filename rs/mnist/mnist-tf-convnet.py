# http://tensorfly.cn/tfdoc/tutorials/mnist_pros.html
# http://oldblog.fuyangzhen.com/bootstrap/blog/001484103400778194a18ec4c8e4e599d4df98c338590f7000#

profilename='default'

import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
print('-> Using TF', tf.__version__)

### Read Train-Val data and split ###
trainval = pd.read_csv("train.csv")
trainval_images = trainval.iloc[:, 1:].div(255)
trainval_labels = pd.get_dummies(trainval.iloc[:, :1].label)
train_images, val_images, train_labels, val_labels = train_test_split(
        trainval_images, trainval_labels, train_size=0.8, random_state=0)
print('-> train set shape', train_images.shape)
print('-> val   set shape', val_images.shape)

### Read Test data ###
test = pd.read_csv('test.csv')
test_images = test.iloc[:,:].div(255)
print('-> test  set shape', test_images.shape)

### Setup Graph ###
x = tf.placeholder(tf.float32, [None, 784], name='x')         # <-- Placeholder
y = tf.placeholder(tf.float32, [None, 10], name='y')          # <-- Placeholder

x_image = tf.reshape(x, [-1,28,28,1]) # localid, width, height, channel

W_conv1 = tf.Variable(tf.truncated_normal([5, 5, 1, 32], stddev=0.1))
b_conv1 = tf.Variable(tf.constant(0.1, shape=[32]))
h_conv1 = tf.nn.relu(tf.nn.conv2d(
    x_image, W_conv1, strides=[1, 1, 1, 1], padding='SAME') + b_conv1)
h_pool1 = tf.nn.max_pool(h_conv1, ksize=[1, 2, 2, 1],
    strides=[1, 2, 2, 1], padding='SAME')

W_conv2 = tf.Variable(tf.truncated_normal([5, 5, 32, 64], stddev=0.1))
b_conv2 = tf.Variable(tf.constant(0.1, shape=[64]))
h_conv2 = tf.nn.relu(tf.nn.conv2d(
    h_pool1, W_conv2, strides=[1, 1, 1, 1], padding='SAME') + b_conv2)
h_pool2 = tf.nn.max_pool(h_conv2, ksize=[1, 2, 2, 1],
    strides=[1, 2, 2, 1], padding='SAME')

W_fc1 = tf.Variable(tf.truncated_normal([7 * 7 * 64, 1024], stddev=0.1))
b_fc1 = tf.Variable(tf.constant(0.1, shape=[1024]))
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
keep_prob = tf.placeholder(tf.float32, name='keep_prob')      # <-- Placeholder
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = tf.Variable(tf.truncated_normal([1024, 10], stddev=0.1))
b_fc2 = tf.Variable(tf.constant(0.1, shape=[10]))
y_ = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

cross_entropy = -tf.reduce_sum(y*tf.log(y_))

train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_,1), tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

### Train and Val ###
sess = tf.Session()
sess.run(tf.global_variables_initializer())
saver = tf.train.Saver()

tf.summary.scalar('cross_entropy', cross_entropy)
tf.summary.scalar('accuracy', accuracy)
tfsmmall = tf.summary.merge_all()
train_writer = tf.summary.FileWriter("mnist-convnet/train-{}".format(profilename), sess.graph)
test_writer  = tf.summary.FileWriter("mnist-convnet/test-{}".format(profilename))

for i in range(20000):
# NOTE:
# could not set cudnn tensor descriptor: CUDNN_STATUS_BAD_PARAM
# batchsize 0 will cause the above zero, be careful when reading.
# when your index for reading data is wrong, the batch could be 0.
    batch_images = train_images.iloc[
        (i*50)%33600:
        (i+1)%672==0 and 33600 or ((i+1)*50)%33600].values
    batch_labels = train_labels.iloc[
        (i*50)%33600:
        (i+1)%672==0 and 33600 or ((i+1)*50)%33600].values

    loss, acc, summary, _ = sess.run([cross_entropy, accuracy,
            tfsmmall , train_step],
            feed_dict={x: batch_images, y: batch_labels, keep_prob: 0.5})
    train_writer.add_summary(summary, i)
    if i % 5 == 0:
        #print('-> data range {} - {}'.format( (i*50)%33600,
        #    (i+1)%672==0 and 33600 or ((i+1)*50)%33600))
        testacc, summary = sess.run([accuracy, tfsmmall ],
            feed_dict={x:val_images, y:val_labels, keep_prob: 1.0})
        test_writer.add_summary(summary, i)
        print('-> step {:5d} | loss: {:5.2f} | train acc {:.03f} | test accuracy: {:.05f}'.format(
            i, loss, acc, testacc))

print('Save file to path:', saver.save(sess, 'kaggle_MNIST_net.ckpt'))
### saver restore ### 
# W = tf.Variable(tf.zeros([784, 10]), dtype=tf.float32, name='Weights')
# b = tf.Variable(tf.zeros([1, 10]), dtype=tf.float32, name='biases')
# saver = tf.train.Saver()
# with tf.Session() as sess:
#     saver.restore(sess,'/Users/fuyangzhen/Desktop/kaggle_MNIST_net.ckpt')
#     print('W:',sess.run(W))
#     print('b:',sess.run(b))

### Test ###
test_predictions = sess.run( tf.argmax(y_, 1), feed_dict={x: test_images, keep_prob: 1.0})
print('-> made predictions', test_predictions.shape)
df_predictions = pd.DataFrame(np.array([np.arange(1,28000+1), test_predictions]).T,
        columns=["ImageID", "Label"])
print(df_predictions.head())
df_predictions.to_csv("predictions.csv", header=True, index=False)
