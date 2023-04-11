# http://tensorfly.cn/tfdoc/tutorials/mnist_pros.html
# http://oldblog.fuyangzhen.com/bootstrap/blog/001484103400778194a18ec4c8e4e599d4df98c338590f7000#

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
x = tf.placeholder(tf.float32, [None, 784])
y = tf.placeholder(tf.float32, [None, 10])
W = tf.Variable(tf.zeros([784, 10]), dtype=tf.float32, name="W")
b = tf.Variable(tf.zeros([1, 10]), dtype=tf.float32, name="b")
y_ = tf.nn.softmax(tf.matmul(x, W) + b)
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y * tf.log(y_), reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
correct_pred = tf.equal(tf.argmax(y_, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

tf.summary.scalar('cross_entropy', cross_entropy)
tf.summary.scalar('accuracy', accuracy)

### Train and Val ###
sess = tf.Session()
merged = tf.summary.merge_all()
train_writer = tf.summary.FileWriter("/home/lumin/tblog/train", sess.graph)
test_writer = tf.summary.FileWriter("/home/lumin/tblog/test")
saver = tf.train.Saver()

sess.run(tf.global_variables_initializer())

for i in range(10000):
    # FIXME: the batch will be zero when i==671, since the index is 33550:0
    batch_images = train_images.iloc[(i*50)%33600:((i+1)*50)%33600].values
    batch_labels = train_labels.iloc[(i*50)%33600:((i+1)*50)%33600].values

    loss, acc, summary, _ = sess.run([cross_entropy, accuracy, merged, train_step],
            feed_dict={x: batch_images, y: batch_labels})
    train_writer.add_summary(summary, i)
    if i % 500 == 0:
        tacc, summary = sess.run([accuracy, merged], feed_dict={x:val_images, y:val_labels})
        print('-> step {:5d} | loss: {:5.2f} | train acc: {:.03f} | test accuracy: {:.05f}'.format( i, loss, acc, tacc))
        test_writer.add_summary(summary, i)

print('Save file to path:', saver.save(sess, 'kaggle_mnist.tfs'))
### saver restore ### 
# W = tf.Variable(tf.zeros([784, 10]), dtype=tf.float32, name='Weights')
# b = tf.Variable(tf.zeros([1, 10]), dtype=tf.float32, name='biases')
# saver = tf.train.Saver()
# with tf.Session() as sess:
#     saver.restore(sess,'/Users/fuyangzhen/Desktop/kaggle_MNIST_net.ckpt')
#     print('W:',sess.run(W))
#     print('b:',sess.run(b))

### Test ###
test_predictions = sess.run( tf.argmax(y_, 1), feed_dict={x: test_images})
print('-> made predictions', test_predictions.shape)
df_predictions = pd.DataFrame(np.array([np.arange(1,28000+1), test_predictions]).T,
        columns=["ImageID", "Label"])
print(df_predictions.head())
df_predictions.to_csv("predictions.csv", header=True, index=False)
