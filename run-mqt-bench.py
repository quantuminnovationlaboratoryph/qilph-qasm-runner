#================================================#
#                File Information                #
#================================================#

# run-mqt-bench.py 
# Created on: 2023 June 21
# Updated by: Ren Tristan A. de la Cruz

#================================================#
#                   LIBRARIES                    #
#================================================#

import os
import sys
from datetime import datetime
#import platform # ToDo:for detecting operating systems
#from multiprocessing import Process
#from multiprocessing import Pool

#================================================#
#                   DEFAULTS                     #
#================================================#

gTestSetString = '''qaoa_indep_qiskit_ : 3-5
                     vqe_indep_qiskit_ : 3-5
           portfolioqaoa_indep_qiskit_ : 3-5
            portfoliovqe_indep_qiskit_ : 3-5
        grover-noancilla_indep_qiskit_ : 2-5
          grover-v-chain_indep_qiskit_ : 2,3,4,5-9+2
         qwalk-noancilla_indep_qiskit_ : 3-5
           qwalk-v-chain_indep_qiskit_ : 3-11+2
                     ghz_indep_qiskit_ : 2-5
              graphstate_indep_qiskit_ : 3-5
                     qft_indep_qiskit_ : 2-5
                      dj_indep_qiskit_ : 2-5
                qpeexact_indep_qiskit_ : 2-5
              qpeinexact_indep_qiskit_ : 2-5
                      ae_indep_qiskit_ : 2-5
           realamprandom_indep_qiskit_ : 2-5
       groundstate_small_indep_qiskit_ : 4,12,14'''

gTestSetString2 ='''qaoa_indep_qiskit_ : 3-15
                     vqe_indep_qiskit_ : 3-19
           portfolioqaoa_indep_qiskit_ : 3-13
            portfoliovqe_indep_qiskit_ : 3-22
        grover-noancilla_indep_qiskit_ : 2-15
          grover-v-chain_indep_qiskit_ : 2,3,4,5-27+2
         qwalk-noancilla_indep_qiskit_ : 3-18
           qwalk-v-chain_indep_qiskit_ : 3-129+2
                     ghz_indep_qiskit_ : 2-129
              graphstate_indep_qiskit_ : 3-129
                     qft_indep_qiskit_ : 2-129
                      dj_indep_qiskit_ : 2-129
                qpeexact_indep_qiskit_ : 2-129
              qpeinexact_indep_qiskit_ : 2-129
                      ae_indep_qiskit_ : 2-129
           realamprandom_indep_qiskit_ : 2-129
       groundstate_small_indep_qiskit_ : 4,12,14'''

gTestListFilename = ""
gBackend          = "dd-qasm"
gQasmRunnerScript = "run-qasm.py"
gQasmDirectory    = "MQTBench"
gLogsDirectory    = "logs"


#================================================#
#               PARAMETER SETTING                #
#================================================#

for parameter in sys.argv:
   if parameter.endswith(".py"):
      continue
   elif parameter.startswith("list="):
      gTestListFilename = parameter.replace("list=","")
      continue
   elif parameter.startswith("back="):
      gBackend = parameter.replace("back=","")
      continue
   elif parameter.startswith("qasm="):
      gQasmDirectory = parameter.replace("qasm=","")
      continue
   elif parameter.startswith("logs="):
      gLogsDirectory = parameter.replace("logs=","")
      continue
   else:
      continue

#================================================#
#             PARAMETER CHECKING                 #
#================================================#

if (os.path.exists(gLogsDirectory) == False):
  print("The logs directory \"" + gLogsDirectory + "\" does not exists.")
  print("Creating logs directory \"" + gLogsDirectory + "\" now.")
  os.mkdir(gLogsDirectory, mode = 0o777)


if (os.path.exists(gQasmDirectory) == False):
  print("The Qasm/MQTBench directory \"" + gQasmDirectory + "\" does not exists.")
  exit()


if ( os.path.exists(gTestListFilename) == False):
  print("The test list file \"" + gTestListFilename + "\" does not exists.")
  print("Using default test list instead.")

#================================================#
#                GET TEST LIST                   #
#================================================#

if gTestListFilename != "":
   gTestListFile  = open(gTestListFilename, "r")
   gTestSetString = gTestListFile.read()
   gTestListFile.close()


#================================================#
#           TEST LIST STRING PARSER              #
#================================================#
 
def ParseRangeString(rangeString):
   if ("-" not in rangeString):
      return [int(rangeString)]
   if ("+" not in rangeString):
      minQubitNo = int(rangeString.split("-")[0])
      maxQubitNo = int(rangeString.split("-")[1])
      return [minQubitNo+i for i in range(maxQubitNo-minQubitNo+1)]
   stepSize = int(rangeString.split("+")[1])
   minQubitNo = int(rangeString.split("+")[0].split("-")[0])
   maxQubitNo = int(rangeString.split("+")[0].split("-")[1])
   return [minQubitNo+(stepSize*i) for i in range(int((maxQubitNo-minQubitNo)/stepSize)+1)]


def ParseTestSetString(testSetString):
   tests = []
   testSetArray = testSetString.split("\n")
   for testSet in testSetArray:
      if ":" in testSet:
         testSetInfo     = testSet.split(":")
         testSetName     = testSetInfo[0].replace(" ", "")
         testSetNumStr   = testSetInfo[1].replace(" ", "")
      else:
         continue
      testSetNumArray = []
      if "," in testSetNumStr:
         testSetNumTempArray = testSetNumStr.split(",")
         for testSubsetString in testSetNumTempArray:
            testSetNumArray += ParseRangeString(testSubsetString)
      else:
         testSetNumArray += ParseRangeString(testSetNumStr)
      tests.append((testSetName,testSetNumArray))
      
   return tests


#================================================#
#                   RUN TESTS                    #
#================================================#

print("+-----------------------------+")
print("|          Test List          |")
print("+-----------------------------+\n")
print(gTestSetString)

allTest = ParseTestSetString(gTestSetString)

setCount = len(allTest) 

setIndex = 1
for testSet in allTest:
   testSetName = testSet[0]
   testCount   = len(testSet[1])
   testIndex   = 1
   for qubitNo in testSet[1]:
      #qasmFile = testSetName + str(qubitNo)
      qasmFile = testSetName + str(qubitNo).rjust(3,'0')
      commandString  = "python3 "
      commandString += gQasmRunnerScript + " "
      commandString += gQasmDirectory + "/"
      commandString += qasmFile + ".qasm"
      commandString += " back=" + gBackend
      commandString += " > "
      commandString += gLogsDirectory + "/"
      commandString += qasmFile + "." + gBackend + ".log"
      print("==================================================")
      print("SET     : " + str(setIndex)  + "/" + str(setCount))
      print("TEST    : " + str(testIndex) + "/" + str(testCount))
      print("START   : " + str(datetime.now()))
      print("COMMAND : " + commandString)
      os.system(commandString)
      print("END     : " + str(datetime.now()))
      print("\n")
      testIndex += 1
   setIndex += 1





























