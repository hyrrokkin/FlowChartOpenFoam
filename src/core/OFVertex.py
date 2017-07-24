from Graph import Vertex
import os
import sys
#import PyFoam
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Basics.TemplateFile import TemplateFileOldFormat


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

def copyCase(sourcePath, destPath):
    try:
        check_dir(sourcePath)
        check_dir(destPath)
    except ValueError:
        raise ValueError('copyCase error: new case structure was not created')
    try:
        check_file(destPath +'/system/controlDict')
        print "Target dir seems not empty. Pass"
        pass
    except:
        os.system('cp -rn ' + sourcePath + '/* ' + destPath)


class ParameterVariation(Vertex):
    def __init__(self, templateFile = '', templateCase = '', variables = [], values = []):
        super(ParameterVariation, self).__init__(name='ParameterVariation')
        try:
            check_file(templateFile)
            check_dir(templateCase)
        except ValueError:
            raise ValueError('Templates should be provided by user')
        if len(variables) == 0 or len(values[0])==0:
            raise ValueError('ParameterVariation must have at least one Variable and one Value')

        self.__templateFile = templateFile
        self.__templateCase = templateCase
        self.__vars = variables
        self.__vals = values
        self.__counter = -1
        self.__parPaths = []
        self.__parDict = dict.fromkeys(self.__vars, 1)

    def initialize(self, **kwargs):
        try:
            path = kwargs['path']
            check_dir(path)
        except:
            raise ValueError('Vertex ParameterVariation can not find path to case')            
        self.__cachePath=path+"/cache"
        try:
            check_dir(self.__cachePath)
        except ValueError:
            os.mkdir(self.__cachePath) 
        pass

    def prepareParameterPath(self):
        self.__currentPath=self.__cachePath+"/var" + str(self.__counter) 
        if(self.__counter>len(self.__parPaths)):
            self.__parPaths.append(self.__currentPath)
        try:
            check_dir(self.__currentPath)
        except ValueError:
            os.mkdir(self.__currentPath)
   
    def setValsOnIter(self, i):
        if(i>len(self.__vals[0])):
            print "ParameterVertex is out of values. Exit"
            exit()
        baseFile = str(self.__templateFile)
        savePath = (baseFile.split("."))[0]
        baseFile = (baseFile.split("/"))[-1]
        baseFile = (baseFile.split("."))[0]
        #print savePath
        #print baseFile
        t=TemplateFileOldFormat(name=self.__templateFile)
        for key, value in self.__parDict.items():
            j = self.__vars.index(key)
            self.__parDict[key] = self.__vals[j][i]
        t.writeToFile(savePath, self.__parDict)
            
    def action(self, **kwargs):
        self.__counter+=1
        if (self.__counter>=len(self.__vals[0])):
            exit()
        print self
        print 'run ParameterVariation'
        self.setValsOnIter(self.__counter)
        self.prepareParameterPath()
        copyCase(self.__templateCase, self.__currentPath)
        if len(self.edges()) > 0:
            self.edges().keys()[0].action(path=self.__currentPath)

class BlockMesh(Vertex):
    def __init__(self, ofDictPath =''):
        super(BlockMesh, self).__init__(name='blockMesh')
        try:
            check_file(ofDictPath)
        except ValueError:
            raise ValueError('File blockMeshDict should be provided by user')

    def initialize(self, **kwargs):
        pass
             
    def action(self, **kwargs):
        print self
        print 'run blockMesh'
        try:
            check_dir(kwargs['path'])
        except:
            raise ValueError('Vertex blockMesh can not find path to case')
            
        os.system('blockMesh -case ' + kwargs['path'] + ">log.blockMesh")
        #os.system('blockMesh')

        if len(self.edges()) > 0:
            self.edges().keys()[0].action(path=kwargs['path'])

class Probe(Vertex):
    def __init__(self, ofDictPath ='', interval = 1, field = 'p', point = [0.,0.,0.]):
        super(Probe, self).__init__(name='probe')
        try:
            if (str(ofDictPath).split("/")[-1]!="controlDict"):
                raise ValueError
            check_file(ofDictPath)
        except ValueError:
            raise ValueError('File controlDict should be provided by user')
        try:
            if(int(interval) <= 0):
                raise ValueError
            #todo field check
            #if(str(field)!=("p"))
            if(len(point)!=3):
                raise ValueError
        except ValueError:
            raise ValueError('Not valid parameters for Probe')
        #all checks passed
        self.controlDict = ParsedParameterFile(ofDictPath)    
        self.interval = interval
        self.field = field
        self.point = point

    def checkForProbe(self):
        try:
            funcField=self.controlDict['functions']
        except KeyError:
            self.controlDict['functions'] = {}
            return False
        for Name,Val in funcField.iteritems():
            for fName,fVal in Val.iteritems():
                if type(fName)!=str or type(fVal)!=str:
                    # this is not an old-school entry
                    continue
                    if(fName == 'type' & fVal == 'probes'):
                        return True
                    #print fName
                    #print fVal
        return False

    def addProbe():
        pass

    def initialize(self, **kwargs):
        if self.checkForProbe():
            print "Probe Vertex: controlDict contains probes. It will be updated"
        else:
            print "Probe Vertex: no probes detected in controlDict"
        pass
             
    def action(self, **kwargs):
        print self
        print 'Probe control'
        try:
            check_dir(kwargs['path'])
        except:
            raise ValueError('Vertex Probe can not find path to case')
        #os.system('blockMesh -case ' + kwargs['path'] + ">log.blockMesh")
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
        self.__solverName = parsedControlDict["application"]
        #Very good way to control previously parsed OpenFOAM file
        #parsedControlDict["endTime"] = 1
        #parsedControlDict.writeFile()
        
        super(Solver, self).__init__(name='solver')

    @property
    def setupCase(self):
        return self.__setupCase
        
    def initCase(self, casePath):
        copyCase(self.__setupCase, casePath)
        return True
    
    def initialize(self, **kwargs):
        #by defult it's project dir
        self.__runPath = kwargs['path'] + "/" + self.__solverName
        try:
            check_dir(self.__runPath)
        except ValueError:
            os.mkdir(self.__runPath) 
        copyCase(self.__setupCase, self.__runPath)
        pass
         
    def action(self, **kwargs):
        print self
        print 'run ' + self.__solverName
        os.system(self.__solverName + ' -case ' + kwargs['path'] + '>log.'+self.__solverName)

        if len(self.edges()) > 0:
            self.edges().keys()[0].action(path=kwargs['path'])


class ParaFoam(Vertex):
    def __init__(self):
        super(ParaFoam, self).__init__(name='paraFoam')

    def initialize(self, **kwargs):
        pass
     
    def action(self, **kwargs):
        os.system('paraFoam -case ' + kwargs['path'])
        print self
        print 'run paraFoam'

        if len(self.edges()) > 0:
            self.edges().keys()[0].action(kwargs)
