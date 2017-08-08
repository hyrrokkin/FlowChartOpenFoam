from core.Project import *
from core.OFVertex import *

from pyDOE import *
import numpy as np
import sys

Roll = lambda phi: np.matrix([[1., 0., 0.], [0., np.cos(phi), -np.sin(phi)],[0., np.sin(phi),  np.cos(phi)]])
Pitch = lambda teta:  np.matrix([[np.cos(teta), 0., np.sin(teta)], [0., 1, 0.], [-np.sin(teta), 0,  np.cos(teta)]])
Yaw = lambda psi: np.matrix([[np.cos(psi), -np.sin(psi), 0.],[np.sin(psi),  np.cos(psi), 0.], [0., 0., 1.]])

n = 3
smpl = 36
design = lhs(n, samples=smpl)
magU = 8.333
parameters = []
angles = []
for i in design[:]:
    i*=2
    i*=np.pi
    tRoll = Roll(i[0])
    tPitch = Pitch(i[1])
    tYaw = Yaw(i[2])
    Transform = tRoll*tPitch*tYaw
    Velocity = np.matrix([magU, 0., 0.])
    Velocity *=Transform
    checkSum = (Velocity[0,0]**2 + Velocity[0,1]**2 + Velocity[0,2]**2)**0.5
    print Velocity, checkSum
    #gamma = np.acos(np.sqrt(1 - np.cos(alpha)**2 - np.cos(beta)**2))
    parameters.append(Velocity.tolist()[0])
    #parameters[-1][-1] = 0.0
    #parameters[-1][1] = 0.0
    angles.append(i.tolist())
    print parameters[-1], angles[-1]


#sys.exit(1)
w1 = Weight(5)
w2 = Weight(6)
w3 = Weight(10)

graph = Graph()

#sourceTutorial = '/home/rocketman/OFProject/cavity/'
#UtemplatePath = '/home/rocketman/OFProject/cavity/0/U.template'
#controlDictPath = '/home/rocketman/OFProject/cavity/system/controlDict'
sourceTutorial = '/home/rocketman/OFProject/canopy_coarse/'
UtemplatePath = '/home/rocketman/OFProject/canopy_coarse/0/U.template'
controlDictPath = '/home/rocketman/OFProject/canopy_coarse/system/controlDict'


Uvars = ['Ux', 'Uy', 'Uz']
Uvals = [[1, 5 , 10], [0, 0, 0], [0, 0, 0]]
varList = ['xElem', 'yElem']
valList = [[20, 50], [20, 50]]


connector = EmptyVertex()
paramStudy = ParameterVariation(UtemplatePath, sourceTutorial, Uvars, parameters) 
solver = Solver( sourceTutorial )
paraFoam = ParaFoam()

graph.add_vertex(solver)
graph.add_vertex(connector)
graph.add_vertex(paramStudy)

graph.connect(solver, connector, w2)
graph.connect(connector, paramStudy, w2)
graph.connect(paramStudy, solver, w3)

project = Project(name='canopyProj', graph=graph, clearPath=True)
project.run(2)
