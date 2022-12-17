'''
https://www.tensorflow.org/tutorials/keras/basic_classification
'''
import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt

print('Using TF', tf.__version__)

fashion = keras.datasets.fashion_mnist
(x_train, y_train), (x_test, y_test) = fashion.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
print('Training set size', x_train.shape, y_train.shape)
print('Teset set size', x_test.shape, y_test.shape)

plt.figure()
plt.imshow(x_train[0])
plt.colorbar()
plt.grid(False)
#plt.show()

x_train, x_test = x_train / 255.0, x_test / 255.0

plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5, 5, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(x_train[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[y_train[i]])
#plt.show()

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.softmax),
    ])
model.compile(optimizer=tf.train.AdamOptimizer(),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)
test_loss, test_acc = model.evaluate(x_test, y_test)
print('Test accuracy:', test_acc)

predictions = model.predict(x_test)
print(predictions[0])
print(np.argmax(predictions[0]), y_test[0])

img = np.expand_dims(x_test[0], 0)
print(img.shape)
pred = model.predict(img)
print(np.argmax(pred), y_test[0])
