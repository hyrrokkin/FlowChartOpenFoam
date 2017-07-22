from core.Project import *
from core.OFVertex import *

w1 = Weight(5)
w2 = Weight(6)
w3 = Weight(10)

graph = Graph()

blockMeshFilePath = '/home/rocketman/OFProject/cavity/system/blockMeshDict'
sourceTutorial = '/home/rocketman/OFProject/cavity/'
blockMeshTemplatePath = '/home/rocketman/OFProject/cavity/system/blockMeshDict.template'
varList = ['xElem', 'yElem']
valList = [[20, 50], [20, 50]]

paramStudy = ParameterVariation(blockMeshTemplatePath, sourceTutorial, varList, valList)
blockMesh = BlockMesh( blockMeshFilePath)
solver = Solver( sourceTutorial )
paraFoam = ParaFoam()

graph.add_vertex(blockMesh)
graph.add_vertex(solver)
#graph.add_vertex(paraFoam)
graph.add_vertex(paramStudy)

graph.connect(blockMesh, solver, w1)
graph.connect(solver, paramStudy, w2)
graph.connect(paramStudy, blockMesh, w3)

project = Project(name='cavityProj', graph=graph, clearPath=True)
project.run(2)
