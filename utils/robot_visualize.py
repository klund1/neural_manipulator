import visual as vis
from dhTable import *

from math import pi

AXIS = vis.vector(1,0,0)
UP = vis.vector(0,1,0)

class TransformFrame():
    def __init__(self, transform, size=0.2):
        if type(transform) not in [np.matrix, np.ndarray] or transform.shape != (4,4):
            raise ValueError("Input transform must be a 4x4 numpy matrix or array")
        self.size = size

        pos = transform[0:3, 3]
        self.x_axis = vis.arrow(pos = pos, axis = self.size*transform[0:3, 0], color = vis.color.red)
        self.y_axis = vis.arrow(pos = pos, axis = self.size*transform[0:3, 1], color = vis.color.green)
        self.z_axis = vis.arrow(pos = pos, axis = self.size*transform[0:3, 2], color = vis.color.blue)

    def setTransform(self, transform):
        if type(transform) not in [np.matrix, np.ndarray] or transform.shape != (4,4):
            raise ValueError("Input transform must be a 4x4 numpy matrix or array")

        pos = transform[0:3, 3]
        self.x_axis.pos = pos
        self.x_axis.axis = self.size*transform[0:3, 0]
        self.y_axis.pos = pos
        self.y_axis.axis = self.size*transform[0:3, 1]
        self.z_axis.pos = pos
        self.z_axis.axis = self.size*transform[0:3, 2]


class Link():
    def __init__(self, theta, d, r, alpha, next_link=None, link_color=vis.color.red):
        self.frame = vis.frame()
        self.theta = theta
        self.d = d
        self.r = r
        self.alpha = alpha

        self.color = link_color

        self.first_piece = vis.cylinder(frame = self.frame,
                                        pos = (0,0,0),
                                        radius = 0.1,
                                        axis = self.d * AXIS,
                                        color = self.color)

        self.second_piece = vis.cylinder(frame = self.frame,
                                         pos = self.d * AXIS,
                                         radius = 0.1,
                                         axis = self.r * UP.rotate(theta, AXIS),
                                         color = self.color)

        self.elbow_piece = vis.sphere(frame = self.frame,
                                      pos = self.d * AXIS,
                                      radius = 0.1,
                                      color = self.color)

        self.base_piece = vis.cylinder(frame = self.frame,
                                       pos = -0.1 * AXIS,
                                       radius = 0.11,
                                       axis = 0.2 * AXIS)

        self.next_link = next_link
        self.update()

    def setTheta(self, theta):
        self.theta = theta
        self.update()

    def setD(self, d):
        self.d = d
        self.update()

    def setR(self, r):
        self.r = r
        self.update()

    def setAlpha(self, alpha):
        self.alpha = alpha
        self.update()

    def setNextLink(self, next_link):
        self.next_link = next_link
        self.update()

    def setColor(self, color):
        self.color = color
        self.update()

    def setFrame(self, new_frame):
        self.frame.pos = new_frame.pos
        self.frame.axis = new_frame.axis
        self.frame.up = new_frame.up

    def update(self):
        self.first_piece.axis = self.d*AXIS
        self.first_piece.color = self.color
        self.second_piece.pos = self.d * AXIS
        self.second_piece.axis = self.r * UP.rotate(self.theta, AXIS)
        self.second_piece.color = self.color
        self.elbow_piece.pos = self.d * AXIS
        self.elbow_piece.color = self.color

        if self.next_link != None:
            self.next_link.setFrame(self.getNextFrame())

    def getNextFrame(self):
        new_up = self.frame.up.rotate(self.theta, self.frame.axis)
        new_axis = self.frame.axis.rotate(self.alpha, new_up)
        new_pos = self.frame.pos + self.d*self.frame.axis + self.r*new_up

        new_frame = vis.frame()
        #axis MUST be set before up
        new_frame.axis = new_axis
        new_frame.up = new_up
        new_frame.pos = new_pos

        return new_frame

class Manipulator():
    def __init__(self):
        self.dh_table = DHTable()
        self.links = []
        self.joint_values = {}

        self.base_frame = vis.frame()
        self.base_frame.axis = (0,0,1)
        self.base_frame.up = (1,0,0)

    def setBaseFrame(self, new_frame):
        self.base_frame.pos = new_frame.pos
        self.base_frame.axis = new_frame.axis
        self.base_frame.up = new_frame.up

    def addDHTableRow(self, theta, d, r, alpha):
        self.dh_table.addRow(theta, d, r, alpha)

    def setDHTable(self, dh_table):
        self.dh_table = dh_table
        self.joint_values = {}
        while len(self.links) > 0:
            link = self.links.pop()
            del link

    def setJoints(self, **kwargs):
        for joint in kwargs:
            self.joint_values[joint] = kwargs[joint]
        self.eval_dh = self.dh_table.evaluate(**self.joint_values)
        self.endTransform = self.dh_table.getEndFrame(**self.joint_values)
    
    def getEndFrame(self):
        return self.endTransform

    def visualize(self):
        for i, (theta, d, r, alpha) in enumerate(self.eval_dh):
            if len(self.links) <= i:
                new_link = Link(theta, d, r, alpha)
                if i == 0:
                    new_link.setFrame(self.base_frame)
                else:
                    self.links[-1].setNextLink(new_link)
                self.links.append(new_link)
            else:
                self.links[i].setTheta(theta)
                self.links[i].setD(d)
                self.links[i].setR(r)
                self.links[i].setAlpha(alpha)

