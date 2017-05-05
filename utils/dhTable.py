import numpy as np
import re
import copy
from math import sin, cos, tan, pi

class DHTable():
  def __init__(self):
    self.rows = []
    self.variables = {}

  def __repr__(self):
    if len(self.rows) == 0:
      return "<EMPTY DHTable>"
    fmt_str = "{:<16.7}"*4 + "\n"
    s = fmt_str.format("Theta","d","r","alpha")
    for row in self.rows:
      s += fmt_str.format(row[0], row[1], row[2], row[3])
    return s

  def save(self, filename):
    with open(filename, "w") as f:
      f.write("#")
      f.write(self.__repr__())

  def load(self, filename):
    self.rows = []
    self.variables = {}
    with open(filename, "r") as f:
      for line in f.readlines():
        if not re.match("\s*#", line):
          match = re.match("\s*(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s*", line)
          if match:
            self.addRow(match.group(1), match.group(2), match.group(3), match.group(4))

  def numRows(self):
    return len(self.rows)

  def addRow(self, theta, d, r, alpha):
    row = []
    new_variables = {}
    row_number = len(self.rows)
    elem_number = 0
    for param in [theta, d, r, alpha]:
      try:
        row.append(float(param))
      except ValueError:
        if type(param) == str:
          if not re.match("^\w+$", param):
            raise ValueError("Invalid input parameter string: ```{}```".format(param))
          elif param in self.variables or param in new_variables:
            raise ValueError("Cannot repeat parameter names in DH Table: {}".format(param))
          row.append(param)
          new_variables[param] = (row_number, elem_number)
        else:
          raise TypeError("Invalid type for parameter input: {}".format(type(param)))
      elem_number += 1
    self.rows.append(row)
    for param, (row, elem) in new_variables.iteritems():
      self.variables[param] = (row,elem)
    return


  def evaluate(self, **kwargs):
    eval_rows = copy.deepcopy(self.rows)
    for var,(row,pos) in self.variables.iteritems():
      if var not in kwargs:
        msg = "All variables must be assigned in call to evaluate: {} unassigned".format(var)
        raise ValueError(msg)
      eval_rows[row][pos] = float(kwargs[var])
    return eval_rows


  def getEndFrame(self, **kwargs):
    eval_rows = self.evaluate(**kwargs)
    T = np.eye(4)
    for row in eval_rows:
      A = DHTable.getTransform(row)
      T = T*A
    return T


  @staticmethod
  def getTransform(dh_table_row):
    if len(dh_table_row) != 4:
      raise ValueError("DH Table rows must have exactly 4 elements")
    th, d, r, alpha = dh_table_row
    return np.mat([[cos(th), -sin(th)*cos(alpha),  sin(th)*sin(alpha), r*cos(th)],
                   [sin(th),  cos(th)*cos(alpha), -cos(th)*sin(alpha), r*sin(th)],
                   [0,        sin(alpha),          cos(alpha),         d        ],
                   [0,        0,                   0,                  1        ]])

