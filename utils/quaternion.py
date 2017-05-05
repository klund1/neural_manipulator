from math import sqrt
import numpy as np

def get_pos_and_quat(T):
  """ return the x,y,z position and quaternion representation of the input transform """
  x = T[0,3]
  y = T[1,3]
  z = T[2,3]

  S0 = 1 + T[0,0] + T[1,1] + T[2,2]
  S1 = 1 + T[0,0] - T[1,1] - T[2,2]
  S2 = 1 - T[0,0] + T[1,1] - T[2,2]
  S3 = 1 - T[0,0] - T[1,1] + T[2,2]

  L = [S0, S1, S2, S3]

  best_index = L.index(max(L))

  if best_index == 0:
    qw = 0.5*sqrt(S0)
    qx = (T[2,1] - T[1,2])/(4*qw)
    qy = (T[0,2] - T[2,0])/(4*qw)
    qz = (T[1,0] - T[0,1])/(4*qw)
    
  elif best_index == 1:
    qx = 0.5*sqrt(S1)
    qw = (T[2,1] - T[1,2])/(4*qx)
    qy = (T[0,1] + T[1,0])/(4*qx)
    qz = (T[0,2] + T[2,0])/(4*qx)

  elif best_index == 2:
    qy = 0.5*sqrt(S2)
    qw = (T[0,2] - T[2,0])/(4*qy)
    qx = (T[0,1] + T[1,0])/(4*qy)
    qz = (T[1,2] + T[2,1])/(4*qy)

  elif best_index == 3:
    qz = 0.5*sqrt(S3)
    qw = (T[1,0] - T[0,1])/(4*qz)
    qx = (T[0,2] + T[2,0])/(4*qz)
    qy = (T[1,2] + T[2,1])/(4*qz)

  return (x,y,z),(qw,qx,qy,qz)

def get_transform(pos,quat):
  x,y,z = pos
  qw,qx,qy,qz = quat

  T = np.zeros([4,4])

  T[0,0] = qw**2 + qx**2 - qy**2 - qz**2
  T[0,1] = 2*(qx*qy - qw*qz)
  T[0,2] = 2*(qw*qy + qx*qz)
  T[1,0] = 2*(qx*qy + qw*qz)
  T[1,1] = qw**2 - qx**2 + qy**2 - qz**2
  T[1,2] = 2*(qy*qz + qw*qx)
  T[1,2] = 2*(qy*qz - qw*qx)
  T[2,0] = 2*(qx*qz - qw*qy)
  T[2,1] = 2*(qw*qx + qy*qz)
  T[2,2] = qw**2 - qx**2 - qy**2 + qz**2
  
  T[0,3] = x
  T[1,3] = y
  T[2,3] = z
  T[3,3] = 1

  return T

