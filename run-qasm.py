#================================================#
#                  Information                   #
#================================================#

# Created On : 2023 January 11
# Created By : DOST-ASTI Quantum Circuit Simulation (QCS) Project
# Updated On : 2023 December 04
# Updated By : DOST-ASTI QCS Project


#================================================#
#               Required Packages                #
#================================================#


import sys
import time
from memory_profiler import memory_usage
from memory_profiler import profile
from qiskit import *
from mqt import ddsim
import hashlib
from datetime import datetime
from qiskit.providers.aer import AerSimulator
import subprocess
import numpy as np# for printing numpy arrays
import math
import psutil # for physical memory retrieval

#================================================#
#    Formatted Matrix/Vector Print Functions     #
#================================================#

def PrintStateVector(ddsimStateVector):                                                      
   nonZeroThreshold = 0.00001                                                                 
   indexDigit    = math.ceil(math.log10(len(ddsimStateVector)))
   indexDigitStr = "{:0" + str(indexDigit) + "}"
   index = 0
   for item in ddsimStateVector: 
      realString = "{:+2.3f}".format(np.real(item))    
      if ( np.real(item) < nonZeroThreshold):    
         realString = "      "    
      imagString = "{:+2.3f}".format(np.imag(item))    
      if ( np.imag(item) < nonZeroThreshold):    
         imagString = "      "    
      if ((realString != "      ") or (imagString != "      ")):
         print(indexDigitStr.format(index) + " (" + realString + "," + imagString + ") ")
      index = index + 1

def PrintMatrix(matrix):                                                            
   nonZeroThreshold = 0.00001                                                                 
   #operatorArray  = qiskitOperator.data                                                       
   for row in matrix:                                                                  
      rowString = ""                                                                          
      for item in row:                                                                        
         realString = "{:+2.3f}".format(np.real(item))                                        
         if ( abs(np.real(item)) < nonZeroThreshold):                                         
            realString = "      "                                                             
         imagString = "{:+2.3f}".format(np.imag(item))                                        
         if ( abs(np.imag(item)) < nonZeroThreshold):                                         
            imagString = "      "                                                             
         rowString +=  "(" + realString + "," + imagString + ") "                             
      print(rowString) 


def PrintHelp():
   print("\n-------------------------------")
   print("How to Run : <python> run-qasm.py <.qasm file>")
   print("   Example :  python3 run-qasm.py shors-algorithm.qasm")
   print("-------------------------------\n")

   print("OPTIONS")

   print("")
   print("-------------------------------------------")
   print("BACKEND + MODE : back=<BACKEND> mode=<MODE>")
   print("-------------------------------------------\n")

   print("Example 1: python3 run-qasm.py shors-algorithm.qasm back=dd-qasm")
   print("Example 2: python3 run-qasm.py shors-algorithm.qasm back=dd-state-hybrid mode=dd")
   print("Example 3: python3 run-qasm.py shors-algorithm.qasm back=dd-qasm-path    mode=bracket")
   print("")
   print("++-------------+-----------------+--------------------+")
   print("| TYPE         | BACKEND         | MODE               |")
   print("+--------------+-----------------+--------------------+")
   print("| unitary      | dd-unitary      | sequential         |")
   print("| unitary      | dd-unitary      | recursive          |")
   print("+--------------+-----------------+--------------------+")
   print("| state vector | dd-state        | <none>             |")
   print("+--------------+-----------------+--------------------+")
   print("| state vector | dd-state-hybrid | dd                 |")
   print("| state vector | dd-state-hybrid | amplitude          |")
   print("+--------------+-----------------+--------------------+")
   print("| qasm         | dd-qasm         | <none>             |")
   print("+--------------+-----------------+--------------------+")
   print("| qasm         | dd-qasm-hybrid  | dd                 |")
   print("| qasm         | dd-qasm-hybrid  | amplitude          |")
   print("+--------------+-----------------+--------------------+")
   print("| qasm         | dd-qasm-path    | sequential         |")
   print("| qasm         | dd-qasm-path    | pairwise_recursive |")
   print("| qasm         | dd-qasm-path    | bracket            |")
   print("| qasm         | dd-qasm-path    | alternating        |")
   print("| qasm         | dd-qasm-path    | cotengra           |")
   print("+--------------+-----------------+--------------------+")

   print("\n")
   print("------------------------------------")
   print("SHOT COUNTS : shot=<number of shots>")
   print("------------------------------------\n")
   print("Specifies the number of shots to be performed.")
   print("Example : python3 run-qasm.py shors-algorithm.qasm shot=1024")

   print("\n")
   print("----------------------------")
   print("LOG LEVEL : logs=<log level>")
   print("----------------------------\n")
   print("Specifies which log levels to print out.\n")
   print(" 1 (000001) : Prints the [benchmark] level logs.")
   print(" 2 (000010) : Prints the [error    ] level logs.")
   print(" 4 (000100) : Prints the [info     ] level logs.")
   print(" 8 (001000) : Prints the [banner   ] level logs.")
   print("16 (010000) : Prints the [result   ] level logs.")
   print("32 (100000) : Prints the [visual   ] level logs.")
   print("15 (001111) : Prints the [banner and lower] level logs.")
   print("31 (011111) : Prints the [result and lower] level logs.")
   print("63 (111111) : Prints the [all      ] level logs.\n")
   print("Example : python3 run-qasm.py shors-algorithm.qasm logs=31")

   print("\n")
   print("----------------------------")
   print("TEST TYPE : test=<test type>")
   print("----------------------------\n")
   print("Specifies what benchmarking test (with or w/o memory consumption test) to run \n")
   print("      Test : memo (default value)")
   print("Decription : run-qasm.py will measure memory consumption. ")
   print("   Example : python3 run-qasm.py shors-algorithm.qasm test=memo\n")
   print("      Test : run")
   print("Decription : run-qasm.py will NOT measure memory consumption.")
   print("   Example : python3 run-qasm.py shors-algorithm.qasm test=run")
   print("")


#================================================#
#                 Repeated Logs                  #
#================================================#


logRunID       = "{:06}".format(abs(hash("Hello, world!") + int(time.time())) % (10**6))
logRunString   = "[" + sys.argv[0] + ":" + logRunID + "] "
logBorder1     = "+---------------------------------+\n"
logBorder2     = "+---------------------------------+"
logStart       = "| " + logRunID + " | DDSIM QASM Run | START |\n"
logEnd         = "| " + logRunID + " | DDSIM QASM Run | END   |\n"
logStartBanner =  logBorder1 + logStart + logBorder2
logEndBanner   =  logBorder1 + logEnd   + logBorder2


logLvlBench    = 1    #000001 
logLvlError    = 2    #000010
logLvlInfo     = 4    #000100
logLvlBanner   = 8    #001000 
logLvlResult   = 16   #010000
logLvlVisual   = 32   #100000

logLvlAll      = 63   #111111
logLvlNoVis    = 31   #011111
logLvlNoRes    = 15   #001111

gLogLevel      = logLvlNoVis


#================================================#
#                Logging Function                #
#================================================#


def printLog (logString, logLevel, logThreshold):
   if ((logLevel & logThreshold) > 0):
      print(logString)


#================================================#
#                   Variables                    #
#================================================#


gShotCount           = 1000
gQasmFilename        = ""
gQasmFile            = ""
gQasmString          = ""
gQuantumCircuit      = ""
gCircuitDepth        = 0
gCircuitQubits       = 0
gCircuitGates        = 0

gFileReadTime        = 0
gCircuitCreationTime = 0
gCreationTime        = 0
gSimulationTime      = 0
gTotalRunTime        = 0

gMaxCreationMemory   = 0
gMaxSimulationMemory = 0
gMaxMemoryUsage      = -1
gTestMode            = "memo"
gBackend             = "dd-qasm"
gSimulationMode      = "" # for DDSim backend
gNThreads            = 1
   
gBackEnds = {"dd-unitary"      : "unitary_simulator",
             "dd-state"        : "statevector_simulator",
             "dd-state-hybrid" : "hybrid_statevector_simulator",
             "dd-qasm"         : "qasm_simulator",
             "dd-qasm-hybrid"  : "hybrid_qasm_simulator",
             "dd-qasm-path"    : "path_sim_qasm_simulator"} 

gJobOptions = dict()

#================================================#
#               Parameter Checking               #
#================================================#



if ( len(sys.argv) < 2 ):
   printLog(logStartBanner,
            logLvlBanner, 
            gLogLevel)
   printLog(logRunString + "No provided QSAM file name.", 
            logLvlError,
            gLogLevel)
   printLog(logEndBanner,
            logLvlBanner,
            gLogLevel)
   exit()


for parameter in sys.argv:
   if parameter.endswith(".py"):
      continue
   elif "--help" in parameter:
      PrintHelp()
      exit()
   elif parameter.startswith("shot="):
      gShotCount = int(parameter.replace("shot=",""))
      gJobOptions["shots"]=gShotCount
      continue
   elif parameter.startswith("logs="):
      gLogLevel = int(parameter.replace("logs=",""))
      continue
   elif parameter.startswith("test="):
      gTestMode = parameter.replace("test=","")
      continue
   elif parameter.startswith("proc="):
      gNThreads = int(parameter.replace("proc=",""))
      gJobOptions["nthreads"]=gNThreads
      continue
   elif parameter.startswith("back="):
      gBackend = parameter.replace("back=","")
      if ("dd"  in gBackend):
         if ("unitary" in gBackend):
            gJobOptions["mode"]="sequential"
            if ("rec" in gBackend):
               gJobOptions["mode"]="recursive"
            gBackend = "dd-unitary"
         elif ("hybrid" in gBackend):
            gJobOptions["mode"]="dd"
            if ("amp" in gBackend):
               gJobOptions["mode"]="amplitude"
            gBackend = "dd-qasm-hybrid"
            if ("state" in gBackend):
               gBackend = "dd-state-hybrid"
         elif ("path" in gBackend):
            gJobOptions["mode"]="sequential"
            if ("pair" in gBackend):
               gJobOptions["mode"]="pairwise_recursive"
            if ("brac" in gBackend):
               gJobOptions["mode"]="bracket"
            if ("alt" in gBackend):
               gJobOptions["mode"]="alternating"
            if ("cot" in gBackend):
               gJobOptions["mode"]="cotengra"
            gBackend = "dd-qasm-path"
         else:
            continue
      elif ("aer" in gBackend):
         print("Test AER")
      else:
         print("Test Defaul")
      continue
   elif parameter.startswith("option:"):
      optionKeyValue = parameter.replace("option:","").split("=")
      optionKey      = optionKeyValue[0]
      if ("_fidelity" in optionKey):
         gJobOptions[optionKey]=float(optionKeyValue[1])
         continue
      if ("nthreads" in optionKey):
         gJobOptions[optionKey]=int(optionKeyValue[1])
         continue
      gJobOptions[optionKey]=optionKeyValue[1]
      continue
   elif parameter.endswith(".qasm"):
      gQasmFilename = parameter
      continue
   else:
      printLog(logRunString + "[err ] [preprocess] Ignoring parameter \"" + parameter + "\".", 
               logLvlError,
               gLogLevel)
      continue

printLog(logStartBanner,
         logLvlBanner, 
         gLogLevel)
 

#================================================#
#      Get Hardware Information (CPU, RAM)       #
#================================================#

gTestStartTime = datetime.now()
printLog(logRunString + "[info] [Start Time]     Date : " + str(gTestStartTime),
         logLvlInfo, 
         gLogLevel)

cpuInfo = subprocess.check_output("lscpu | grep \"Model name\"", shell=True)
printLog(logRunString + "[info] [Hardware  ]      CPU : " + str(cpuInfo).replace("  ", "").replace("\\n\'","").replace("b\'","").replace("Model name:",""),
         logLvlInfo, 
         gLogLevel)

printLog(logRunString + "[info] [Hardware  ]   Memory : " + str(psutil.virtual_memory().total >> 30) + " GiB",
         logLvlInfo, 
         gLogLevel)


#================================================#
#            File Existence Checking             #
#================================================#

try:
   gQasmFile = open(gQasmFilename, "r")
except OSError:
   printLog(logRunString +"[err ] [Circuit   ]     QASM : \"" + gQasmFilename + "\" NOT FOUND.",
            logLvlError,
            gLogLevel)
   printLog(logEndBanner,
            logLvlBanner, 
            gLogLevel)
   exit()
with gQasmFile:
   gQasmFile.close() 
   printLog(logRunString + "[info] [Circuit   ]     QASM : " + gQasmFilename,
            logLvlInfo, 
            gLogLevel) 


#================================================#
#        File Reading & Circuit Creation         #
#================================================#

def CreateQCFromQasm(qasmFilename):
   printLog(logRunString + "[info] [Creation  ]   Status : STARTED",
            logLvlInfo,
            gLogLevel)
   global gCreationTime
   startTime      = time.time()
   quantumCircuit = QuantumCircuit.from_qasm_file(qasmFilename)
   gCreationTime  = time.time() - startTime
   return quantumCircuit

if (gTestMode == "memo"):
   (mem_usage, gQuantumCircuit) = memory_usage((CreateQCFromQasm, (gQasmFilename,)),retval=True )
   gMaxCreationMemory = max(mem_usage) 
   printLog(logRunString + "[info] [Creation  ]   Memory : %s MiB" % gMaxCreationMemory,
            logLvlInfo, 
            gLogLevel)
else:
   gQuantumCircuit = CreateQCFromQasm(gQasmFilename)

printLog(logRunString + "[info] [Creation  ]     Time : %s sec" % gCreationTime,
         logLvlInfo, 
         gLogLevel)


#================================================#
#           Print Circuit Information            #
#================================================#

gCircuitGates  = 0
gCircuitQubits = gQuantumCircuit.num_qubits 
gCircuitDepth  = gQuantumCircuit.depth()
gateCounts     = gQuantumCircuit.count_ops()

for gate in gateCounts:
   if (gate != "measure" and gate != "barrier"):
      gCircuitGates += gateCounts[gate]

printLog(logRunString + "[info] [QC Info   ]   Qubits : " + str(gCircuitQubits),
         logLvlInfo,
         gLogLevel)
printLog(logRunString + "[info] [QC Info   ]    Gates : " + str(gCircuitGates),
         logLvlInfo,
         gLogLevel)
printLog(logRunString + "[info] [QC Info   ]    Depth : " + str(gCircuitDepth),
         logLvlInfo,
         gLogLevel)

if ( (gLogLevel & logLvlVisual) > 1):
   print(logRunString + "[visu] [CIRCUIT   ]   Visual : ")
   print(gQuantumCircuit)


#================================================#
#              Simulation Function               #
#================================================#

def runSimulation(quantumCircuit, backend, jobOptions):
   global gSimulationTime
   global gBackEnds

   printLog(logRunString + "[info] [Simulation]   Status : STARTED",
            logLvlInfo,
            gLogLevel)

   printLog(logRunString + "[info] [Simulation]  backend : " + backend,
            logLvlInfo,
            gLogLevel)

   for optionName in jobOptions:
      optionName2 = optionName.rjust(9, ' ') + " : "
      printLog(logRunString + "[info] [Simulation]"+ optionName2 + str(jobOptions[optionName]),
               logLvlInfo,
               gLogLevel)

   startTime = time.time()
   if ( "dd" in backend ):
      if ( backend == "dd-unitary" ):
         quantumCircuit = quantumCircuit.remove_final_measurements(inplace=False)

      if ( "approx" in backend ):
         simulator = ddsim.CircuitSimulator(quantumCircuit, approximation_step_fidelity=0.6, approximation_steps=5)
         simResults = simulator.simulate(int (jobOptions["shots"]) )
         gSimulationTime  = time.time() - startTime
         return simResults

      backendSimulator = ddsim.DDSIMProvider().get_backend(gBackEnds[backend])
   elif ("aer" in backend ):
      backendSimulator = Aer.get_backend('qasm_simulator')
   else:
      backendSimulator = Aer.get_backend('qasm_simulator')

   myJob            = execute(quantumCircuit, backendSimulator, **jobOptions)
   simResults       = myJob.result()
   gSimulationTime  = time.time() - startTime
   return simResults
"""
   backendSimulator = Aer.get_backend('qasm_simulator')
   myJob            = execute(quantumCircuit,
                      backendSimulator, 
                      shots=shotCount)
"""

#================================================#
#                   Simulation                   #
#================================================#

printLog(logRunString + "[info] [Simulation]  Backend : " + gBackend ,
         logLvlInfo,
         gLogLevel)

if (gTestMode == "memo"):
   (mem_usage, results) = memory_usage((runSimulation, 
                                       (gQuantumCircuit, gBackend, gJobOptions)),
                                       retval=True)
   gMaxSimulationMemory = max(mem_usage)
   printLog(logRunString + "[info] [Simulation]   Memory : %s MiB" % gMaxSimulationMemory,
            logLvlInfo,
            gLogLevel)
else:
   results = runSimulation(gQuantumCircuit, gBackend, gJobOptions)


#================================================#
#           Print simulation results.            #
#================================================#

printLog(logRunString + "[info] [Simulation]     Time : %s sec" % gSimulationTime, logLvlInfo, gLogLevel)
printLog(logRunString + "[resu] [Simulation]  Results : " + str(results), logLvlResult, gLogLevel)

if "qasm" in gBackend:
   shotCounts = results.get_counts(gQuantumCircuit)
   print(shotCounts)
   printLog(logRunString + "[resu] [Simulation]    Shots : " + str(shotCounts),
            logLvlResult,
            gLogLevel)

if "state" in gBackend:
   stateVector = results.get_statevector(gQuantumCircuit)
   printLog(logRunString + "[resu] [Simulation]    State : \n" + str(stateVector),   logLvlResult, gLogLevel)

if "unitary" in gBackend:
   unitaryMatrix = results.get_unitary(gQuantumCircuit)
   printLog(logRunString + "[resu] [Simulation]   Matrix : \n" + str(unitaryMatrix),   logLvlResult, gLogLevel)


#================================================#
#             Print resources used.              #
#================================================#


if ( gTestMode == "memo" ):
   gMaxMemoryUsage = max([gMaxSimulationMemory, gMaxCreationMemory])
   printLog(logRunString + "[info] [Resource  ]   Memory : " + str(gMaxMemoryUsage) + " MiB",
            logLvlInfo,
            gLogLevel)

gTotalRunTime = gSimulationTime + gCreationTime
printLog(logRunString + "[info] [Resource  ]     Time : " + str(gTotalRunTime) + " sec",
         logLvlInfo,
         gLogLevel)


#================================================#
#            Print benchmark summary.            #
#================================================#

gQasmFilePathArray = gQasmFilename.split("/") 
gQasmFilenameOnly  = gQasmFilePathArray[-1].replace(".qasm", "")

logBenchmark  = logRunString 
logBenchmark += "[benc] [SUMMARY   ]     Info , "
logBenchmark += str(gTestStartTime)   + ", " 
logBenchmark += gBackend              + ", " 
logBenchmark += gQasmFilenameOnly     + ", " 
logBenchmark += str(gCircuitQubits)   + ", " 
logBenchmark += str(gCircuitGates)    + ", "
logBenchmark += str(gCircuitDepth)    + ", "
logBenchmark += str(gMaxMemoryUsage)  + ", "
logBenchmark += str(gTotalRunTime)

printLog(logBenchmark,
         logLvlBench,
         gLogLevel)
printLog(logEndBanner,
         logLvlBanner,
         gLogLevel)










