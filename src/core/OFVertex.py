from Graph import Vertex
import os
import sys
#import PyFoam
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

def check_dir(item):
    if not isinstance(item, str):
        raise TypeError('Type error')
    if not os.path.isdir(item):
        raise ValueError('Can not find case dir %s' %item) 

def check_file(item):
    if not isinstance(item, str):
        raise TypeError('Type error')
    if not os.path.isfile(item):
        raise ValueError('Can not find file %s' %item) 


class BlockMesh(Vertex):
    def __init__(self, ofDictPath =''):
        super(BlockMesh, self).__init__(name='blockMesh')
        try:
            check_file(ofDictPath)
        except ValueError:
            raise ValueError('File blockMeshDict should be provided by user')

    def initialize(self, **kwargs):
        print self
             
    def action(self, **kwargs):
        print self
        try:
            check_dir(kwargs['path'])
        except:
            raise ValueError('Vertex blockMesh can not find path to case')
            
        os.system('blockMesh -case ' + kwargs['path'])
        #os.system('blockMesh')

        if len(self.edges()) > 0:
            self.edges().keys()[0].action(path=kwargs['path'])


class Solver(Vertex):
    def __init__(self, tutorialPath=''):
        try:
            check_file(tutorialPath +'/system/controlDict')
        except ValueError:
            raise ValueError('Path to tutorial template case for Solver should be provided by user')
        self.__setupCase = tutorialPath
        parsedControlDict=ParsedParameterFile(tutorialPath+'/system/controlDict')    
        solverNameFromTutorial = parsedControlDict["application"]
        
        #Very good way to control previously parsed OpenFOAM file
        #parsedControlDict["endTime"] = 1
        #parsedControlDict.writeFile()
        
        super(Solver, self).__init__(name=solverNameFromTutorial)

    @property
    def setupCase(self):
        return self.__setupCase
        
    def initCase(self, casePath):
        self.copyTutorialIfEmpty(casePath)
        return True
    
    def copyTutorialIfEmpty(self, casePath):
        try:
            check_dir(casePath)        
        except ValueError:
            raise ValueError('Vertex Solver error: case structure was not created')
        try:
            check_file(casePath +'/system/controlDict')
        except:
            os.system('cp -rn ' + self.setupCase + '/* ' + casePath)

    def initialize(self, **kwargs):
        self.copyTutorialIfEmpty(kwargs['path'])
        print self
         
    def action(self, **kwargs):
        print self
        os.system(self.name + ' -case ' + kwargs['path'])

        if len(self.edges()) > 0:
            self.edges().keys()[0].action(path=kwargs['path'])


class ParaFoam(Vertex):
    def __init__(self):
        super(ParaFoam, self).__init__(name='ParaFoam')

    def initialize(self, **kwargs):
        print self
     
    def action(self, **kwargs):
        os.system('paraFoam -case ' + kwargs['path'])
        print self

        if len(self.edges()) > 0:
            self.edges().keys()[0].action(kwargs)
