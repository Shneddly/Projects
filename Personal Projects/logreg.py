'''
Simple logistic regression algorithm (not yet complete)
'''

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def sigmoid(z):
    # Sigmoid function = 1/(1+e^(-z))
    return 1 / (1 + np.exp(-z))

def gradient_descent(features, target, alpha, epochs):
    
    size = features.shape[0]
    weights = np.zeros(features.shape[1])
    bias = 0
    parameters = {}
    J = []
    
    for epoch in range(epochs):
        
        sigma = sigmoid(np.dot(features.T, weights) + bias)
        cost = -1/size * np.sum(target * np.log(sigma) + (1 - target) * np.log(1 - sigma))
        dW = 1/size * np.dot(features.T, (sigma - target))
        dB = 1/size * np.sum(sigma - target)
        weights -= alpha * dW
        bias -= alpha * dB
        J.append(cost)
    
    parameters['weights'] = weights
    parameters['bias'] = bias
    
    return parameters, J
