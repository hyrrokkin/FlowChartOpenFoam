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
lhsAngles = '/home/rocketman/CODES/Python/lhs-canopy-ang.csv'
lhsNorms = '/home/rocketman/CODES/Python/lhs-canopy-norm.csv'
sourceTutorial = '/home/rocketman/OFProject/canopy_coarse/'
UtemplatePath = '/home/rocketman/OFProject/canopy_coarse/0/U.template'
topoTemplatePath = '/home/rocketman/OFProject/canopy_coarse/system/topoSetDict.template'
controlDictPath = '/home/rocketman/OFProject/canopy_coarse/system/controlDict'


Uvars = ['Ux', 'Uy', 'Uz']
Uvals = [[1, 5 , 10], [0, 0, 0], [0, 0, 0]]
varList = ['xElem', 'yElem']
valList = [[20, 50], [20, 50]]


connector = EmptyVertex()
#paramStudy = ParameterVariation(templateFile=UtemplatePath, templateCase=sourceTutorial, variables=Uvars, values=Uvals) 
paramStudy = ParameterVariation(templateFile=UtemplatePath, templateCase=sourceTutorial, parFile=lhsValues) 
meshVar = ParameterVariation(templateFile=topoTemplatePath, templateCase=sourceTutorial, parFile=lhsNorms) 
#solver = Solver( sourceTutorial )
solver = SolverParallel(2)
paraFoam = ParaFoam()
fResults = ForcesCollector()
faceSelection = TopoSet()
patchCreation = CreatePatch()

graph.add_vertex(solver)
graph.add_vertex(connector)
graph.add_vertex(paramStudy)
graph.add_vertex(meshVar)
graph.add_vertex(fResults)
graph.add_vertex(faceSelection)
graph.add_vertex(patchCreation)

graph.connect(fResults, paramStudy, w2)
graph.connect(paramStudy, connector, w2)
graph.connect(connector, meshVar, w2)
graph.connect(meshVar,faceSelection,w2)
graph.connect(faceSelection, patchCreation, w2)
graph.connect(patchCreation, solver, w2)
graph.connect(solver, fResults, w3)

print "launch project"

project = Project(name='canopyProj', graph=graph, clearPath=True)
project.run(2)
