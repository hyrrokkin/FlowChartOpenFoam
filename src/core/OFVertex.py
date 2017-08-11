from Graph import Vertex
import os
import sys
import csv
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

class EmptyVertex(Vertex):
    def __init__(self):
        super(EmptyVertex, self).__init__(name='empty')
    def initialize(self, **kwargs):
        pass             
    def action(self, **kwargs):
        if len(self.edges()) > 0:
            self.edges().keys()[0].action(path=kwargs['path'])

class ParameterVariation(Vertex):
    def __init__(self, **kwargs):
        super(ParameterVariation, self).__init__(name='ParameterVariation')
        tFile = kwargs.pop('templateFile', '')
        tCase = kwargs.pop('templateCase', '')
        try:
            check_file(tFile)
            check_dir(tCase)
        except ValueError:
            raise ValueError('ParameterVariation: provide templates')
        self.__templateFile = tFile        
        self.__templateCase = tCase
        parFile = kwargs.pop('parFile', '')
        argvar = kwargs.pop('variables', [])
        argval = kwargs.pop('values', [])
        if len(parFile) == 0:
            if len(argvar) == 0 or len(argval)==0:
                raise ValueError('ParameterVariation: no input data')
                exit(0)
        else:
            try:
                check_file(parFile)
            except ValueError:
                raise ValueError('ParameterVariation: no input file')

            csvFile = open(parFile, 'rb')
            reader = csv.reader(csvFile)
            try:
                for row in reader:
                    if reader.line_num == 1:
                        for field in row:
                            argvar.append(str(field))
                        continue
                    fList = []
                    for field in row:
                        fList.append(float(field))
                    argval.append(fList)
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (parFile, reader.line_num, e))
            csvFile.close()   # <---IMPORTANT
        self.__vars = argvar
        self.__vals = argval
        self.__counter = -1
        self.__size = len(argval)
        self.__parPaths = []
        self.__parDict = dict.fromkeys(self.__vars, 0.0)

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
        if(i>len(self.__vals)):
            print "ParameterVertex is out of values. Exit"
            exit()
        baseFile = str(self.__templateFile)
        savePath = (baseFile.split("."))[0]
        baseFile = (baseFile.split("/"))[-1]
        baseFile = (baseFile.split("."))[0]
        t=TemplateFileOldFormat(name=self.__templateFile)
        
        for key, value in self.__parDict.items():
            j = self.__vars.index(key)
            self.__parDict[key] = self.__vals[i][j]
            sys.stdout.write(key+"="+str(self.__vals[i][j])+"; ")
        sys.stdout.write("\n")
        sys.stdout.flush()
        t.writeToFile(savePath, self.__parDict)
            
    def action(self, **kwargs):
        self.__counter+=1
        if (self.__counter>=self.__size):
            exit()
        print self
        print "running value %d of %d" % (self.__counter, self.__size)
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

        if len(self.edges()) > 0:
            self.edges().keys()[0].action(path=kwargs['path'])

class Probe(Vertex):
    def __init__(self, templateDict ='', interval = 1, field = 'p', point = [0.,0.,0.]):
        super(Probe, self).__init__(name='probe')
        try:
            if (str(templateDict).split("/")[-1]!="controlDict"):
                raise ValueError
            check_file(templateDict)
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
        self.controlDict = ParsedParameterFile(templateDict)    
        self.interval = interval
        self.field = field
        self.probeCoords = []
        strPoint = str('('+ ' '.join(map(str, point)) + ')')
        self.probeCoords.append(strPoint)

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

    def addProbe(self):
        #Now actually overwrites probes
        try:
            self.controlDict['functions'] = {'ProbeVertex': {'type': 'probes', 'fields':[self.field], 'libs': ['"libsampling.so"'], 'writeControl': 'timeStep', 'writeInterval': self.interval, 'probeLocations': self.probeCoords}}
        except:
            print "Can not add ProbeVertex function to controlDict"
        self.controlDict.writeFile()
        
    def initialize(self, **kwargs):
        if self.checkForProbe():
            print "Probe Vertex: controlDict contains probes. It will be updated"
        else:
            print "Probe Vertex: no probes detected in controlDict"
        self.addProbe()
        pass
             
    def action(self, **kwargs):
        print self
        print 'Probe control. Just pass'
        try:
            check_dir(kwargs['path'])
        except:
            raise ValueError('Vertex Probe can not find path to case')
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
        #Here could be solution control algo
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
        os.system(self.__solverName + ' -case ' + kwargs['path'] +      '>' + kwargs['path'] + '/' + 'log.'+self.__solverName)

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
