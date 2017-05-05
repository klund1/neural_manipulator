import sys
import os
from keras.models import load_model
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils")))

from time import sleep

from subprocess import Popen

import visual as vis
from robot_visualize import Manipulator
from dhTable import DHTable

# load the manipulator
dh_table = DHTable() 
dh_table.load("dh_table.txt")
arm = Manipulator()
arm.setDHTable(dh_table)


#generate the trajectory

x_pts = [1, -1, -1, 1, 1]
y_pts = [1, 1, -1, -1, 1]
num_pts = 100

def get_traj(waypoints, num_pts):
  traj = np.array([])
  for i in range(len(waypoints)-1):
    traj = np.append(traj, np.linspace(waypoints[i], waypoints[i+1], num_pts))
  return traj

x_traj = get_traj(x_pts, num_pts)
y_traj = get_traj(y_pts, num_pts)

trajectory = np.array([x_traj, y_traj]).T

model = load_model("model.h5")
nn_angles = model.predict(trajectory)

for i in range(len(x_pts)-1):
  x1 = x_pts[i]
  y1 = y_pts[i]
  x2 = x_pts[i+1]
  y2 = y_pts[i+1]
  vis.cylinder(pos=(x1,y1,0), axis=(x2-x1,y2-y1,0), color=vis.color.yellow, radius=0.01)

def getScreenshot(num):
  image_dir = os.path.abspath(os.path.dirname(__file__))+"/images/"
  if not os.path.isdir(image_dir):
      mkdir_process = Popen(["mkdir", image_dir])
      mkdir_process.wait()
  screenshot_process = Popen(["screencapture", image_dir+"frame{:04d}.png".format(num)])
  screenshot_process.wait()

vis.scene.waitfor('click keydown')

#visualize the trajectory
target = vis.sphere(radius = 0.05, color = vis.color.yellow)

for i in range(len(trajectory[:,0])):
  S0,C0,S1,C1 = nn_angles[i,:]
  th0 = np.arctan2(S0,C0)
  th1 = np.arctan2(S1,C1)
  x,y = trajectory[i,:]
  target.pos = (x,y,0)
  arm.setJoints(th0=th0, th1=th1)
  arm.visualize()
  vis.rate(20)
  # getScreenshot(i)

