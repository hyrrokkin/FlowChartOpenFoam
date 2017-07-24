from core.Project import *
from core.OFVertex import *

w1 = Weight(5)
w2 = Weight(6)
w3 = Weight(10)

graph = Graph()

blockMeshFilePath = '/home/rocketman/OFProject/cavity/system/blockMeshDict'
sourceTutorial = '/home/rocketman/OFProject/cavity/'
blockMeshTemplatePath = '/home/rocketman/OFProject/cavity/system/blockMeshDict.template'
UtemplatePath = '/home/rocketman/OFProject/cavity/0/U.template'
Uvars = ['Ux', 'Uy', 'Uz']
Uvals = [[1, 5 , 10], [0, 0, 0], [0, 0, 0]]
varList = ['xElem', 'yElem']
valList = [[20, 50], [20, 50]]

controlDictPath = '/home/rocketman/OFProject/cavity/system/controlDict'

paramStudy = ParameterVariation(UtemplatePath, sourceTutorial, Uvars, Uvals) 
#ParameterVariation(blockMeshTemplatePath, sourceTutorial, varList, valList)
blockMesh = BlockMesh( blockMeshFilePath)
probe = Probe( controlDictPath, 10, 'p', [0.0254, 0.0253, 0.] )
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
