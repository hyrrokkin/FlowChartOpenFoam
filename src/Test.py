from core.Project import *
from core.OFVertex import *

w1 = Weight(5)
w2 = Weight(6)
w3 = Weight(10)

graph = Graph()

blockMeshFilePath = '/opt/openfoam4/tutorials/incompressible/icoFoam/cavity/cavity/system/blockMeshDict'
sourceTutorial = '/home/rocketman/OFProject/cavity/'
blockMeshTemplatePath = '/home/rocketman/OFProject/cavity/system/blockMeshDict.template'
UtemplatePath = '/home/rocketman/OFProject/cavity/0/U.template'

Uvars = ['Ux', 'Uy', 'Uz']
Uvals = [[1, 0 , 0], [5, 0, 0], [10, 0, 0]]
varList = ['xElem', 'yElem']
valList = [[20, 50], [20, 50]]

controlDictPath = '/home/rocketman/OFProject/cavity/system/controlDict'

paramStudy = ParameterVariation(templateFile=UtemplatePath, templateCase=sourceTutorial, variables=Uvars, values=Uvals) 
blockMesh = BlockMesh( blockMeshFilePath)
probe = Probe( controlDictPath, 10, 'p', [0.025, 0.025, 0.005] )
solver = Solver( sourceTutorial )
paraFoam = ParaFoam()

graph.add_vertex(blockMesh)
graph.add_vertex(probe)
graph.add_vertex(solver)
#graph.add_vertex(paraFoam)
graph.add_vertex(paramStudy)

graph.connect(blockMesh, probe, w1)
graph.connect(probe, solver, w1)
graph.connect(solver, paramStudy, w2)
graph.connect(paramStudy, blockMesh, w3)

project = Project(name='cavityProj', graph=graph, clearPath=True)
project.run(3)
