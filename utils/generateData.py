from dhTable import DHTable
from math import ceil
from itertools import product
import numpy as np
from math import sin,cos,pi
from quaternion import *

# take a list (param, low, high) and a desired minimum number of points n
def generateData(param_list, num_points, dh_table, data_file, trig=False):
    num_params = len(param_list)
    points_per_param = int(ceil(num_points ** (1.0/num_params)))
    print "Generating {} points per parameter, for a total of {} points".format(points_per_param, points_per_param**num_params)
    param_settings = [np.linspace(low,high,points_per_param) for param,low,high in param_list]

    f = open(data_file, "w")
    s = "#"
    for param,_,_ in param_list:
        if trig:
            s += "sin({0})\tcos({0})\t".format(param)
        else:
            s += "{}\t".format(param)
    s += "\tx\ty\tz\tqw\tqx\tqy\tqz\n"
    f.write(s)
    
    param_values = {}
    for setting in product(*param_settings):
        for i in range(num_params):
            param = param_list[i][0]
            param_values[param] = setting[i]
        end_frame = dh_table.getEndFrame(**param_values)

        p,q = get_pos_and_quat(end_frame)
        x,y,z = p
        qw,qx,qy,qz = q

        s = ""
        for val in setting:
            if trig:
                s += "{}\t{}\t".format(sin(val), cos(val))
            else:
                s += "{}\t".format(val)
        s += "\t{}\t{}\t{}".format(x,y,z)
        s += "\t{}\t{}\t{}\t{}".format(qw,qx,qy,qz)
        s += "\n"

        f.write(s)
