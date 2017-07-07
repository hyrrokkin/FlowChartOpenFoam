from core.Project import *
from core.OFVertex import *

w1 = Weight(5)
w2 = Weight(6)

graph = Graph()

blockMesh = BlockMesh()
solver = Solver()
paraFoam = ParaFoam()

graph.add_vertex(blockMesh)
graph.add_vertex(solver)
graph.add_vertex(paraFoam)

graph.connect(blockMesh, solver, w1)
graph.connect(solver, paraFoam, w2)

project = Project(name='s', graph=graph)
project.run()
