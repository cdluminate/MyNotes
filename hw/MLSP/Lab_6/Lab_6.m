%% Lab 6: MNIST Digit Classification with kNN and SVMs

%% Dataset
% In this lab, we will be using the MNIST Dataset, which can be downloaded
% from <http://yann.lecun.com/exdb/mnist/.
% http://yann.lecun.com/exdb/mnist/.>
% 
% The MNIST Dataset is a set of black and white photos of handwritten
% digits with their corresponding labels from 0 to 9.
% 
%  
% 
% There are four files on this website -
% 
% |<http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz
% train-images-idx3-ubyte.gz>: training set images (9912422 bytes)|
% 
% |<http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz
% train-labels-idx1-ubyte.gz>: training set labels (28881 bytes)|
% 
% |<http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz
% t10k-images-idx3-ubyte.gz>: test set images (1648877 bytes)|
% 
% |<http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz
% t10k-labels-idx1-ubyte.gz>: test set labels (4542 bytes)|
% 
% You should download these four files and use the files
% |loadMNISTImages.m| and |loadMNISTLabels.m| to load these into MATLAB
% arrays.

%% Problem Statement
% The goal of this lab is to perform classification on the MNIST dataset,
% where the input is an image of a digit and your prediction is a number
% between 0 to 9.
% 
% We will also have a competition for this lab. Extra credit will be
% awarded for each student who achieves the best results across the class
% for either the KNN method or the SVM method. There are two extra credits
% up for grabs.
% 
% The basic method for this lab is as follows -
% 
% # Train and find the PCA dimensions for the training data.
% # Project both the training and testing datasets using these PCA bases.
% # Explore the performance of KNN and SVMs by varying the number of PCA
% bases being projected on.

%% 1. KNN
% Implement the K-nearest neighbor algorithm for the 10 classes that you
% have. Find these 10 clusters using your training data, and then classify
% your testing data based on each test image's distance to your 10 trained
% clusters. Report your result for the different number of PCA bases being
% projected on.

%% 2. SVM
% Use the MATLAB |svm| function to do 10-class classification of the MNIST
% Data. Examples can be found at
% <https://www.mathworks.com/help/stats/support-vector-machine-classification.html
% https://www.mathworks.com/help/stats/support-vector-machine-classification.html>.
% Play with different C values and kernel functions and see how
% they influence your result. Report your best accuracy and settings
% include the dimension, C value, and kernel function you used.
% 
% Submit all your code and a *writeup as PDF* reporting the parameters that
% gave you your best performance. *Do not include the data directory*.
% 
