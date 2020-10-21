import tensorflow as tf
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import tflearn
import numpy as np

'''
Snake Neural Network
A simple neural network used to play the snake game

Current inputs:
    1. Distance Left wall
    2. Distance Top Wall
    3. Distance Right Wall
    4. Distance Bottom Wallbuild_dqn
    5. Distance Apple
    6. Angle Apple
    7. left blocked
    8. up blocked
    9. right blocked
    9. down blocked


'''


class NeuralNetwork:

    def __init__(self, training_data, max_steps):


        x = np.array([i[0] for i in training_data])
        X = x.reshape(-1, 10, 1)
        y = [i[1] for i in training_data]
        input_size = len(X[0])
        output_size = len(y[0])

        network = input_data(shape=[None, input_size, 1], name='input')
        network = tflearn.fully_connected(network, 32)
        network = tflearn.fully_connected(network, 32)
        network = fully_connected(network, output_size, activation='softmax')
        network = regression(network, name='targets')

        self.model = tflearn.DNN(network, tensorboard_verbose=1)

    def train_model(self, training_data):
        shape_second_parameter = len(training_data[0][0])
        x = np.array([i[0] for i in training_data])
        X = x.reshape(-1, shape_second_parameter, 1)
        y = [i[1] for i in training_data]

        self.model.fit({'input': X}, {'targets': y}, n_epoch=10, batch_size=16, show_metric=True)
        self.model.save('miniskake_trained.tflearn')


    def predict(self, training_data):
        prediction = self.model.predict(training_data)
        return np.argmax(prediction[0])

class Generation:
    def __init__(self, population_size):
        self.population_size = population_size

    def evaluate(self):
        for i in range(self.population_size):
            print(i)
