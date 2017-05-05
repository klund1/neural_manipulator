import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils")))
from generateData import generateData
from dhTable import DHTable
from math import pi

dh_table = DHTable() 
dh_table.load("dh_table.txt")

if len(sys.argv) > 1:
  num_pts = int(sys.argv[1])
else:
  num_pts = 100000

generateData([["th0",-pi,pi], ["th1",0,pi]], num_pts, dh_table, "data.txt", trig=True)
