# -*- coding: utf-8 -*-
"""MLP_Training.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zK7B3ZsPzhcSZcYu3bMWXkhzQrbLZ5AA
"""

import pandas as pd
train = pd.read_csv('/content/drive/My Drive/Colab Notebooks/train')
test = pd.read_csv('/content/drive/My Drive/Colab Notebooks/test')



import numpy as np
import scipy.special
from scipy.special import softmax
from math import log
class ANN:
    def __init__(self, inputnodes, hiddennodes1,hiddennodes2, outputnodes, learningrate):
        self.inodes = inputnodes
        self.hnodes1 = hiddennodes1
        self.hnodes2 = hiddennodes2
        self.onodes = outputnodes
        self.lr = learningrate
    
        
        # creat initial random weights
        self.wih = np.random.normal(0.0, pow(self.hnodes1, -0.5), (self.hnodes1, self.inodes))
        self.whh = np.random.normal(0.0, pow(self.hnodes2, -0.5), (self.hnodes2, self.hnodes1))
        self.who = np.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes2))
        
        # Create Activation Functions
        self.sigmoid_act_funct = lambda x: scipy.special.expit(x)
        self.relu_act_funct = lambda x: np.maximum(0, x)
        self.leakyrelu_act_funct = lambda x: np.where(x > 0, x, x * 0.01)
        # Actovation Funvtion for output layer
        self.softmax_act_funct = lambda x: softmax(x)
        pass
    # Softmax
    def softmax(X):
        exps = np.exp(X - np.max(X))
        return exps / np.sum(exps)
        pass
    # SoftMax Corros Entropy
    def softmax_cross_entropy(self, actual, predicted):
        sum_score = 0.0
        for i in range(len(actual)):
            for j in range(len(actual[i])):
                sum_score += actual[i][j] * log(1e-9 + predicted[i][j])
                mean_sum_score = 1.0 / len(actual) * sum_score
                return -mean_sum_score
            pass
        pass
    
    def train(self, inputs_list, targets_list):
        # There are two main parts in trainin 1. Feedforward that we did for query function as well, 2. backpropagation
        # convert inputs and targets list in 2d array
        inputs =  np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T
        
        # 1. Feedforward
        # matreix multiplication for caclulatin WI into hidden layer
        h_input1 = np.dot(self.wih, inputs)
        
        h_output_sig1 = self.sigmoid_act_funct(h_input1)
        
        h_input2 = np.dot(self.whh, h_output_sig1)
        
        # Calculate activation function for hidden layer
        h_output_sig2 = self.sigmoid_act_funct(h_input2)
        
        #h_output_relu = self.relu_act_funct(h_input1)
        #h_output_leakyrelu = self.leakyrelu_act_funct(h_input1)
        
        # matreix multiplication for caclulatin WI into output layer
        o_input = np.dot(self.who, h_output_sig2)
        
        # Calculate activation function for output layer
        #o_output = self.softmax_act_funct(o_input)
        
        o_output= self.sigmoid_act_funct(o_input)
        
        # 2. Backpropagation
        # first we need to calculate the error for output layer wich we are using SoftMax Cross-Entropy Loss for caclularion
        o_error =  targets - o_output 
        #o_error = self.softmax_cross_entropy( o_output, targets)
        #o_error = np.sum(np.nan_to_num(-targets*np.log(o_output) - (1-targets)*np.log(1-o_output)))
        
        # scound we need to calculate hidden layer error that is the output_errors, split by weights,
        # recombined at hidden nodes

        h_error2 = np.dot(self.who.T, o_error) #  /N
        
        h_error1 = np.dot(self.whh.T, h_error2)
        
        ## update the weights for the links between the hidden and output layers
        self.who += self.lr * np.dot((o_error * o_output * (1.0 - o_output)), np.transpose(h_output_sig2))
        
        # update the weights for the links between the two hidden layers
        self.whh += self.lr * np.dot((h_error2 * h_output_sig2 * (1.0 - h_output_sig2)), np.transpose(h_output_sig1))
        
        
        # update the weights for the links between the input and hidden layers
        self.wih += self.lr * np.dot((h_error1 * h_output_sig1 * (1.0 - h_output_sig1)), np.transpose(inputs))
        return o_error
        
        #print("\nEpoch %d complete\tLoss: %f\n"%(o_error))

    
    
    
    # The query() function takes the input to a neural network and returns the network’s output.we need to pass the input signals from the
    # input layer of nodes, through the hidden layer and out of the final output layer.
    def query(self, inputs_list):
        # convert inputs list into 2d array
        inputs = np.array(inputs_list, ndmin=2).T
        
        # matreix multiplication for caclulatin WI into hidden layer 
        h_input1 = np.dot(self.wih, inputs)
        
        h_output_sig1 = self.sigmoid_act_funct(h_input1)
        
        h_input2 = np.dot(self.whh, h_output_sig1)
        
        # Calculate activation function for hidden layer 
        h_output_sig2 = self.sigmoid_act_funct(h_input2)
        #h_output_relu = self.relu_act_funct(h_input1)
        #h_output_leakyrelu = self.leakyrelu_act_funct(h_input1)
        
        ## matreix multiplication for caclulatin WI into output layer
        o_input = np.dot(self.who, h_output_sig2)
        
        # Calulate activation fumction for output layer 
        #o_output_softmax = self.sigmoid_act_funct(o_input)
        o_output = self.softmax_act_funct(o_input)
        
        return o_output_softmax
    pass

# number of input, hidden and output nodes
input_nodes = 3072
hidden_nodes1 = 1000
hidden_nodes2 = 100
output_nodes = 10
# learning rate
learning_rate = 0.01

#ValueError: operands could not be broadcast together with shapes (10,50,250) (1,10,25000)
#ValueError: shapes (10,250) and (50,25000) not aligned: 250 (dim 1) != 50 (dim 0)
#ValueError: shapes (50,300) and (300,3072,1) not aligned: 300 (dim 1) != 3072 (dim 1)
#ValueError: operands could not be broadcast together with shapes (10,50,1) (10,25000,1)

# create instance of neural network
n = ANN(input_nodes,hidden_nodes1,hidden_nodes2, output_nodes,
learning_rate)



# train the neural network
epoches = 10
for i in range(epoches):
  for inedx, row in train.iterrows():
    #all_value = row #j.split('\t')
  # scale and shift the inputs
    inputs = (np.asfarray(row[:-1]) / 255.0 * 0.99) + 0.01
  # create the target output values (all 0.01, except the desired label which is 0.99)
    targets = np.zeros(output_nodes) + 0.01
  # train[:, -1] is the target label for this record
    targets[row[-1:].astype(int)] = 0.99
    n.train(inputs, targets)
  #print("\nEpoch %d complete\tLoss: %f\n"% (o_error[0]))
pass



# evaluation
eval = []
# go through all the records in the test data set
#testtarg = list(row[-1:])
#print(type(testtarg))

for index, row in test.iterrows():
  #for i in testtarg: #range(len(row[-1:])):
  correct_label = row[-1:].astype(int) #np.array.row[-1:] #test[:, -1].astype(int)
  #print(correct_label)
  #correcy_label.astype(int64)
  #print(type(correct_label))
#for j in test[:, :-1]:
  # scale and shift the inputs
  inputs = (np.asfarray(row[:-1]) / 255.0 * 0.99) + 0.01
  #print(type(inputs))
  # query the network
  outputs = n.query(inputs)
  #print(type(outputs))
  # the index of the highest value corresponds to the label
  label = np.argmax(outputs)
  #print(label)
# append correct or incorrect to list
  if (label == correct_label.any()):
    eval.append(1)
  else:
    eval.append(0)

# Accuracy
ACC = np.asarray(eval)
print ("Acuracy = ", ACC.sum() / ACC.size * 100)
