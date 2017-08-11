from core.Project import *
from core.OFVertex import *

#sys.exit(1)
w1 = Weight(5)
w2 = Weight(6)
w3 = Weight(10)

graph = Graph()

#sourceTutorial = '/home/rocketman/OFProject/cavity/'
#UtemplatePath = '/home/rocketman/OFProject/cavity/0/U.template'
#controlDictPath = '/home/rocketman/OFProject/cavity/system/controlDict'
lhsValues = '/home/rocketman/CODES/Python/lhs-canopy-vel.csv'
sourceTutorial = '/home/rocketman/OFProject/canopy_coarse/'
UtemplatePath = '/home/rocketman/OFProject/canopy_coarse/0/U.template'
controlDictPath = '/home/rocketman/OFProject/canopy_coarse/system/controlDict'


Uvars = ['Ux', 'Uy', 'Uz']
Uvals = [[1, 5 , 10], [0, 0, 0], [0, 0, 0]]
varList = ['xElem', 'yElem']
valList = [[20, 50], [20, 50]]


connector = EmptyVertex()
#paramStudy = ParameterVariation(templateFile=UtemplatePath, templateCase=sourceTutorial, variables=Uvars, values=Uvals) 
paramStudy = ParameterVariation(templateFile=UtemplatePath, templateCase=sourceTutorial, parFile=lhsValues) 
solver = Solver( sourceTutorial )
paraFoam = ParaFoam()

graph.add_vertex(solver)
graph.add_vertex(connector)
graph.add_vertex(paramStudy)

graph.connect(solver, connector, w2)
graph.connect(connector, paramStudy, w2)
graph.connect(paramStudy, solver, w3)

print "lauch project"

project = Project(name='canopyProj', graph=graph, clearPath=True)
project.run(2)
