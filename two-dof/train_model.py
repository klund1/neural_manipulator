from __future__ import division
import os, re
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Lambda
import numpy as np
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

class Data():
    pass


def generate_model(inputs, outputs, layers, units):
    model = Sequential()

    model.add(Dense(input_dim=inputs, units=units))
    model.add(Activation("sigmoid"))

    for i in range(layers-1):
        model.add(Dense(input_dim=units, units=units))
        model.add(Activation("sigmoid"))

    model.add(Dense(input_dim=units, units=outputs))
    model.add(Activation("linear"))

    model.compile(loss="mean_squared_error", optimizer="nadam")
    return model

def load_data(datafile, num_inputs, num_outputs):
    raw_data = np.loadtxt(datafile, comments="#")
    angle = raw_data[:, 0:num_outputs]
    position = raw_data[:, num_outputs:num_outputs+num_inputs]

    return position, angle

def plot_from_history(history):
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(history["loss"], label="Training Data")
    if "val_loss" in history:
        ax.plot(history["val_loss"], label="Validation Data")
    ax.legend(loc="best")
    ax.set_title("Model Accuracy")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss (Mean Absolute Error)")
    fig.savefig("training.png")
    plt.close(fig)

def main():
    
    D = Data()
    D.num_inputs = 2
    D.num_outputs = 4
    D.layers = 4
    D.units = 40
    D.epochs = 100
    D.batch_size = 256

    print "Building Model"
    model = generate_model(D.num_inputs, D.num_outputs, D.layers, D.units)

    print "Loading Data"
    position, angle = load_data("data.txt", D.num_inputs, D.num_outputs)

    print "Training"
    out = model.fit(position, angle, epochs=D.epochs, batch_size=D.batch_size)

    print "Saving model.h5"
    model.save("model.h5")

    #plot_from_history(out.history)

if __name__ == "__main__":
    main()
