from Graph import Vertex
import os
import PyFoam


class BlockMesh(Vertex):
    def __init__(self):
        super(BlockMesh, self).__init__(name='BlockMesh')

    def action(self, **kwargs):
        print self
        os.system('blockMesh -case ' + kwargs['path'])
        #os.system('blockMesh')

        if len(self.edges()) > 0:
            self.edges().keys()[0].action(path=kwargs['path'])


class Solver(Vertex):
    def __init__(self):
        super(Solver, self).__init__(name='IcoFoam')

    def action(self, **kwargs):
        print self
        os.system('icoFoam -case ' + kwargs['path'])

        if len(self.edges()) > 0:
            self.edges().keys()[0].action(path=kwargs['path'])


class ParaFoam(Vertex):
    def __init__(self):
        super(ParaFoam, self).__init__(name='ParaFoam')

    def action(self, **kwargs):
        os.system('paraFoam -case ' + kwargs['path'])
        print self

        if len(self.edges()) > 0:
            self.edges().keys()[0].action(kwargs)
