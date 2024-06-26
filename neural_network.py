import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math

import numpy as np
from sklearn.datasets import make_moons

def calculate_loss(model, X, y):
    # First, to compute our predictions y_hat I will compute a,h,and z as defined in our project description
    # Note, these are not singular values as we are evaluating this element wise for each data point in X
    a = np.dot(X,model['W1'])+model['b1']
    h = np.tanh(a)
    z = np.dot(h,model['W2'])+model['b2']
    y_hat = softmax(z)
    #Now I want to multiply the log of my predictions by the actual values y
    product = np.multiply(np.log(y_hat),y)
    #Now I sum all the elements together
    sum = np.sum(product)
    #Finally, I multiply by -1/N
    return (-1/(len(X)))*sum

def predict(model, x):
    #We do the same thing as above to compute y_hat, but now x is a single sample
    a = np.dot(x,model['W1']) + model['b1']
    h = np.tanh(a)
    z = np.dot(h,model['W2']) + model['b2']
    y_hat = softmax(z)
    print("y_hat:", y_hat)
    return y_hat

def y_sum(y_hat,y, k, j):
    sum = 0
    for x in range(k):
        for g in range(j):
            if(y_hat[x][0] == 1 and y_hat[x][1] == 0):
                sum += y[x][g] * math.log(0,2)
            else:
                sum += y[x][g] * math.log(1,2)
    return sum

def build_model(X,y,nn_hdim, num_passes=20000,printloss=False):
    featureSize = np.size(X, 0)
    sampleSize = np.size(X, 1)
    #print(featureSize)
    #print(sampleSize)
    step = 0.01
    b1 = np.ones((1,nn_hdim))
    b2 = np.ones((1,2)) ##there will always be two outputs
    nn = None
    W1 = np.full((sampleSize, nn_hdim), 1)
    W2 = np.full((nn_hdim, 2), 1)
    en_y = np.full((featureSize, 2), 1)
    for index, v in enumerate(y):
        if(v == 0):
            en_y[index][0] = 1
            en_y[index][1] = 0
        else:
            en_y[index][0] = 0
            en_y[index][1] = 1
    #print(en_y)
    #print(y)

    for i in range(num_passes):
        print(i)
        a = X.dot(W1) + b1
        #print(a)
        h = np.tanh(a)
        #print(h)
        z = h.dot(W2) + b2
        #print(z)
        y1 = softmax(z)
    #    print(y1)
        #if(math.isnan(y1[0][0])):
            #print(i)

        back2 = y1
        a1 = 1 - ((np.tanh(a))**2)
        #test = np.sum(y for n in y[,:]
        for k in range(featureSize):
            for j in range(0,2):
                #print(j)
                #print(k)
                #if(i == 1):
                #    print(back2[k][j])
                #    print(j)
            #        print(featureSize)
                back2[k][j] = (-1/featureSize) * y_sum(back2, en_y, k, j)

                if(i == 1):
                    sum = y_sum
                    #print(back2[k][j])

        gW2 = (h.T).dot(back2)
        gb2 = np.sum(back2, axis=0, keepdims=True)

        back1 = a1 * back2.dot(W2.T)
        gW1 = np.dot(X.T, back1)
        gb1 = np.sum(back1, axis=0)
        if(i % 5000 == 0):
            print(W1, W2, gW1, gW2)


        W1 = W1 - (step * gW1)
        b1 = b1 - (step * gb1)
        W2 = W2 - (step * gW2)
        b2 = b2 - (step * gb2)


        nn = {'W1': W1, 'b1': b1, 'W2':W2, 'b2': b2}


    print(nn)
    return nn


def softmax(z):
    i = np.exp(z)
    y = i / np.sum(i, axis=1, keepdims=True)
    #print("Sum of i is this", np.sum(i, axis=1, keepdims=True))
    return y

def plot_decision_boundary(pred_func, X, y):
    x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
    y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
    h = 0.01
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = pred_func(np.c_[xx.ravel(), yy.ravel()]) #error here used to be predict but this was not passed
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Spectral)


np.random.seed(0)
X, y = make_moons ( 200 , noise =0.20)
plt.scatter (X [ : , 0 ] , X [ : , 1 ] , s =40 , c=y , cmap=plt.cm.Spectral )

plt.figure( figsize =(16 , 32 ) )
hidden_layer_dimensions = [1 , 2 , 3 , 4]
for i , nn_hdim in enumerate ( hidden_layer_dimensions ) :
    plt.subplot( 5 , 2 , i +1)
    plt.title( 'HiddenLayerSize%d' % nn_hdim )
    model = build_model(X, y , nn_hdim )
    plot_decision_boundary(lambda x : predict( model , x ) , X, y )
plt.show( )