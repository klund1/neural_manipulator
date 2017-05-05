from quaternion import *
from dhTable import *

d = DHTable()
d.load('dh_table.txt')
T = d.getEndFrame(th0=0.5,th1=1.2,th2=0.01)
p,q = get_pos_and_quat(T)
new_T = get_transform(p,q)

print T
print new_T
