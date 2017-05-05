import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils")))
from dhTable import DHTable

from keras.models import load_model
import numpy as np

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.colors as colors

dh_table = DHTable() 
dh_table.load("dh_table.txt")

def model_error(model,x,y):
    if np.sqrt(x**2 + y**2) > 2:
       return 1e-5
    
    S0,C0,S1,C1 = model.predict(np.array([[x,y]]))[0]
    th0 = np.arctan2(S0,C0)
    th1 = np.arctan2(S1,C1)
    end_transform = dh_table.getEndFrame(th0=th0, th1=th1)
    x_model = end_transform[0,3]
    y_model = end_transform[1,3]
    return np.sqrt( (x-x_model)**2 + (y-y_model)**2 )

def plot_performance(model):
    x = np.linspace(-2,2,200)
    y = np.linspace(-2,2,200)
    x,y = np.meshgrid(x,y)

    n,m = x.shape

    error = np.array([[model_error(model,x[i,j],y[i,j]) for j in range(m)] for i in range(n)])

    plt.pcolor(x,y,error, 
               norm = colors.LogNorm(vmin=error.min(), vmax=error.max()))
    plt.colorbar()
    plt.xlabel("x position")
    plt.ylabel("y position")
    plt.title("Position error for the 2D manipulator")
    plt.grid(True)
    plt.savefig("new_performance.png")

if __name__ == "__main__":
    model = load_model('model.h5')
    plot_performance(model)
    
