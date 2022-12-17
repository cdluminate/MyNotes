'''
Pure Numpy w/o any Machine Learning Lib
'''
import sys
import os
import numpy as np
os.putenv('OPENBLAS_NUM_THREADS', '4')

from dataloader import DataLoader
dataloader = DataLoader()

### Model ###
W = 0.1 * np.random.randn(10, 784) + 0.  # ~N(0, 0.1^2)
B = np.zeros((10, 1))  # ~const(0)
LR = 0.1
batchsize = 64
batchsizeT = 100

### Helper ###
def transform(images, labels):
    images = images / 255.
    images = images.astype(np.double)
    labels = labels.reshape(-1).astype(np.long)
    return images, labels

def toOneHot(labels, classes):
    labels_onehot = np.zeros((labels.size, classes))
    labels_onehot[np.arange(labels.size), labels] = 1.
    return labels_onehot

### Train-Val ###
for i in range(1000+1):
    # read data
    images, labels = dataloader.getBatch('train', batchsize)
    images, labels = transform(images, labels)
    #print(' * X shape', images.shape)  # (64,784)
    labels_onehot = toOneHot(labels, 10)
    #print(' * y shape', labels_onehot.shape)  # (64,10)

    # -- forward --
    '''
    o = Wx + b ->batch WX+B
    y^ = softmax(o) ->batch ...
    L(y^, y) = - \sum_k y_k ln y^_k ->batch -tr(Y logY^^T)
    '''
    o = np.matmul(W, images.T) + B.repeat(batchsize, 1)
    #print(' * o shape', o.shape)  # (10,64)
    yhat = np.exp(o) / np.exp(o).sum(0)
    #print(' * yhat shape', yhat.shape)  # (10,64)
    L = -np.trace(np.matmul(labels_onehot, np.log(yhat)))
    #print(' * loss', L)  # scalar

    #print(' ** predict', np.argmax(yhat, 0))
    #print(' ** ground', labels)
    #print(' ** predict - ground', np.argmax(yhat, 0) - labels)
    batchacc = (np.argmax(yhat, 0) - labels < 1e-7).sum() / labels.size
    #print(' ** batch accuracy', batchacc)

    print('-> Iter {:5d} |'.format(i),
            'loss {:7.3f} |'.format(L),
            'Bch Train Accu {:.2f}'.format(batchacc))

    # -- backward --
    '''
    gy^ = -y ./ y^
    go = J_sf * gy^
    gw = go * x^T
    gb = go
    '''
    gyhat = - labels_onehot.T / (yhat + 1e-7)  # 1e-7 fot stability
    #print(' ** gyhat', gyhat.shape)  # (10,64)
    go = np.zeros((10, batchsize))
    for k in range(batchsize):
        jacob_k = np.diag(yhat[:,k]) - np.matmul(
                yhat[:,k].reshape(10,1), yhat[:,k].reshape(1,10))
        go[:,k] = np.matmul(jacob_k, gyhat[:, k])
    #print(' ** go', go.shape)  # (10,64)
    gb = go.sum(1) / batchsize
    #print(' ** gb', gb.shape)  # (10,)
    gw = np.zeros(W.shape)  # (10,784)
    for k in range(batchsize):
        gw += np.matmul(go[:,k].reshape(10,1), images[k].reshape(1,784))
    gw /= batchsize
    #print(' ** gw', gw.shape)  # (10,784)
    print(' ** Gradient: W', gw.sum(), np.abs(gw).sum(), 'B', gb.sum(), np.abs(gb).sum())

    # -- update --
    '''
    gw <- W - LR * gw
    gb <- B - LR * gb
    '''
    W -= LR * gw
    B -= LR * gb.reshape(10, 1)

    # -- conditional validation --
    if i%100==0:
        print('-> TEST @ {} |'.format(i), end='')
        correct = 0
        total = 0
        lossaccum = 0
        dataloader.reset('val')
        for j in range(dataloader.itersInEpoch('val', batchsizeT)):
            images, labels = dataloader.getBatch('val', batchsizeT)
            images, labels = transform(images, labels)
            labels_onehot = toOneHot(labels, 10)
            # forward only
            o = np.matmul(W, images.T) + B.repeat(batchsizeT, 1)
            yhat = np.exp(o) / np.exp(o).sum(0)
            L = -np.trace(np.matmul(labels_onehot, np.log(yhat)))
            correct += (np.argmax(yhat, 0) - labels < 1e-7).sum()
            total += labels.size
            lossaccum += L
            print('.', end=''); sys.stdout.flush()
        print('|')
        print('-> TEST @ {} |'.format(i),
                'Loss {:7.3f} |'.format(lossaccum),
                'Accu {:.2f}|'.format(correct / total))
