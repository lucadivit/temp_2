from keras.models import *
from keras.layers import *
from keras.optimizers import *
from keras.utils import *


class NeuralNetwork():

    def __init__(self, input_shape, output_dim):
        self.input_shape = input_shape
        self.output_dim = output_dim

    def get_input_shape(self):
        return self.input_shape

    def set_input_shape(self, shape):
        self.input_shape = shape

    def set_output_dim(self, dim):
        self.output_dim = dim

    def get_output_dim(self):
        return self.output_dim

    def create_default_mlp_network(self, num_of_hidden_layers=10, perceptrons_per_layer=16, activation_function='relu', dropout_percentage=0.2):
        model = Sequential()
        model.add(Flatten(input_shape=self.get_input_shape()))
        for i in range(0, num_of_hidden_layers):
            model.add(Dense(perceptrons_per_layer, activation=activation_function))
            model.add(Dropout(dropout_percentage))

        model.add(Dense(self.get_output_dim(), activation='sigmoid'))
        return model



