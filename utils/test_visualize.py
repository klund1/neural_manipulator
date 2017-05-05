from robot_visualize import Manipulator, TransformFrame
import visual as vis
from math import pi

#Desribe the manipulator
arm = Manipulator()
arm.addDHTableRow("th0", 0.3,  0.15, pi/2)
arm.addDHTableRow(0,     "d1", 0.5,  0)
arm.addDHTableRow("th2", -0.2, 0.25, 0)

#Set the joint values and display
arm.setJoints(th0=0, d1=0.4, th2=0)
arm.visualize()

end_frame = TransformFrame(arm.getEndFrame())

th0 = 0
d1=0.4
dx = 0.01
th2 = 0

while True:
    vis.rate(30)
    th0 = (th0+pi/240) % (2*pi)
    th2 = (th2+pi/180) % (2*pi)
    d1 = d1+dx
    if d1 > 1: dx = -0.01
    if d1 < 0.4: dx = 0.01
    arm.setJoints(th0=th0, d1=d1, th2=th2)
    arm.visualize()
    end_frame.setTransform(arm.getEndFrame())


