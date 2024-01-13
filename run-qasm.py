#==================================================================================================#
# Information                                                                                      #
#==================================================================================================#

# Created On : 2023 January 11
# Created By : DOST-ASTI Quantum Circuit Simulation (QCS) Project
# Updated On : 2024 January 10
# Updated By : DOST-ASTI QCS Project


#==================================================================================================#
# Required Packages                                                                                #
#==================================================================================================#


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


import math
import numpy as np
from projectq          import MainEngine
from projectq.backends import Simulator
from projectq.ops      import *


#==================================================================================================#
# Formatted Matrix/Vector Print Functions                                                          #
#==================================================================================================#

def PrintStateVector(_stateVector):
  __stateVector = np.asarray(_stateVector)
  threshold     = 0.0000001
  indexDigit2   = math.ceil(math.log2(len(__stateVector)))
  indexDigit10  = math.ceil(math.log10(len(__stateVector)))
  formatStr2    = "0" + str(indexDigit2) + "b"
  formatStr10   = "{:0" + str(indexDigit10) + "}"
  print("Index (Real, Imag)")
  index = 0
  for cxNum in __stateVector:
    real = np.real(cxNum)
    imag = np.imag(cxNum)

    realStr = "{:+2.5f}".format(real)
    imagStr = "{:+2.5f}".format(imag)

    if np.fabs(real) < threshold:
      realStr = " 0.0    "
    if np.fabs(imag) < threshold:
      imagStr = " 0.0    "
   
    indexStr  = format(index, formatStr2)
    print(formatStr10.format(index), indexStr, "(" + realStr+ ", " +imagStr+")")
    index = index + 1

'''
def PrintStateVector(ddsimStateVector):                                                      
  nonZeroThreshold = 0.000001                                                                 
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
'''

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
  print("| state vector | projq-state     | <none>             |")
  print("| state vector | aer-state       | <none>             |")
  print("+--------------+-----------------+--------------------+")
  print("| state vector | dd-state-hybrid | dd                 |")
  print("| state vector | dd-state-hybrid | amplitude          |")
  print("+--------------+-----------------+--------------------+")
  print("| qasm         | dd-qasm         | <none>             |")
  print("| qasm         | aer-qasm        | <none>             |")
  print("| qasm         | projq-qasm      | <none>             |")
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


#==================================================================================================#
# Repeated Logs                                                                                    #
#==================================================================================================#


logRunID       = "{:06}".format(abs(hash("Hello, world!") + int(time.time())) % (10**6))
logRunString   = "[" + sys.argv[0] + ":" + logRunID + "] "
logBorder1     = "+---------------------------+\n"
logBorder2     = "+---------------------------+"
logStart       = "| " + logRunID + " | QASM Run | START |\n"
logEnd         = "| " + logRunID + " | QASM Run | END   |\n"
logStartBanner =  logBorder1 + logStart + logBorder2
logEndBanner   =  logBorder1 + logEnd   + logBorder2


logLvlBench    = 1    #0000001 
logLvlError    = 2    #0000010
logLvlInfo     = 4    #0000100
logLvlBanner   = 8    #0001000 
logLvlResult   = 16   #0010000
logLvlVisual   = 32   #0100000
logLvlExtra    = 64   #1000000

logLvlAll      = 127  #1111111
logLvlNoVis    = 95   #1011111
logLvlNoExtra  = 31   #0001111

gLogLevel      = logLvlNoExtra


#==================================================================================================#
# Logging Function                                                                                 #
#==================================================================================================#


def printLog (logString, logLevel, logThreshold):
   if ((logLevel & logThreshold) > 0):
      print(logString)


#==================================================================================================#
# Variables                                                                                        #
#==================================================================================================#


gShotCount           = 1
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

#==================================================================================================#
# Parameter Checking                                                                               #
#==================================================================================================#

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
    gJobOptions["shots"]=gShotCount
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
    # Condition: "dd" in gBackend
    elif ("aer" in gBackend):
      print("Test AER")
    else:
      print("Test Default")
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

#==================================================================================================#
# Get Hardware Information (CPU, RAM)                                                              #
#==================================================================================================#

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


#==================================================================================================#
# File Existence Checking                                                                          #
#==================================================================================================#

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


#==================================================================================================#
# File Reading & Circuit Creation                                                                  #
#==================================================================================================#

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


#==================================================================================================#
# Print Circuit Information                                                                        #
#==================================================================================================#

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





#==================================================================================================#
# ProjectQ                                                                                         #
#==================================================================================================#

debug = False

thres    = 0.0000000001
idGate   = MatrixGate([[1,0],
                       [0,1]])
SqrtXdag = get_inverse(SqrtX)

# Mapping of QASM gate labels to ProjectQ gate functions
qasmGateToProjectQ = {
# qubits: 1, parameters: 3

"u3"      :   MatrixGate, # tested 6
"u"       :   MatrixGate, # tested 6 

# qubits: 1, parameters: 2

"u2"      :   MatrixGate, # tested 4

# qubits: 1, parameters: 1

"rx"      :           Rx, # tested 3
"ry"      :           Ry, # tested 3
"u1"      :   MatrixGate, # tested 3
"p"       :   MatrixGate, # tested 3
"rz"      :           Rz, # tested 3

# qubits: 1, parameters: 0

"u0"      :       idGate, # tested 3
"id"      :       idGate, # tested 3 
"t"       :            T, # tested 3
"tdg"     :         Tdag, # tested 3 
"s"       :            S, # tested 3
"sdg"     :         Sdag, # tested 3
"z"       :            Z, # tested 3
"x"       :            X, # tested 3
"y"       :            Y, # tested 3 
"h"       :            H, # tested 3 
"sx"      :        SqrtX, # tested 3
"sxdg"    :     SqrtXdag, # tested 3
"barrier" :      Barrier,
"measure" :      Measure,

# qubits: 2, parameters: 0

"cx"      :         C(X), # tested 4
"cz"      :         C(Z), # tested 4
"cy"      :         C(Y), # tested 4
"ch"      :         C(H), # tested 4
"csx"     :     C(SqrtX), # tested 4 
"swap"    :         Swap, # tested 4

# qubits: 2, parameters: 1

"crx"     :           Rx, # tested 4
"cry"     :           Ry, # tested 4
"crz"     :           Rz, # tested 4
"cp"      :   MatrixGate, # tested 4
"cu1"     :   MatrixGate, # tested 4
"rzz"     :          Rzz, # tested 4
"rxx"     :          Rxx, # tested 4

# qubits: 2, parameters: 3

"cu3"     :   MatrixGate, # tested 4

# qubits: 2, parameters: 4

"cu"      :   MatrixGate, # tested 4

# qubits: 3, parameters: 0

"cswap"   :      C(Swap), # tested 2
"ccx"     :      Toffoli, # tested 4
"rccx"    :  C(idGate,2), # NOT TESTED

# qubits: 4, parameters: 0

"rc3x"    :  C(idGate,3), # NOT TESTED
"rcccx"   :  C(idGate,3), # NOT TESTED
"c3x"     :       C(X,3), # tested 4 
"c3sqrtx" :   C(SqrtX,3), # tested 4
"c3sx"    :   C(SqrtX,3), # tested 4

# qubits: 5, parameters: 0

"c4x"     :       C(X,4), # tested 5

}


# This function takes a small threshold number and a complex number cNum = p + qi, where a and b are 
# the two real components of cNum, and return new complex number cNum' = r + si where r is equal to
# p if the absolute value of p's fractional component is greater than the threshold value otherwise
# r is the integral part of p and s is equal to q if the absolute value of q's fractional component
# is greater than the threshold value otherwise s is the integral part of q.

def zeroDownFrac (cNum, threshold):
  realComp = np.modf(np.real(cNum))
  realInt  = realComp[1]
  realFrac = realComp[0]
  imagComp = np.modf(np.imag(cNum))
  imagInt  = imagComp[1]
  imagFrac = imagComp[0]
  realFrac = 0.0 if np.fabs(realFrac) < threshold else realFrac
  imagFrac = 0.0 if np.fabs(imagFrac) < threshold else imagFrac
  return complex(realInt + realFrac, imagInt + imagFrac)



def qasmU3Matrix ( _t, _p, _l, thres):
  _k = _p + _l
  p  = np.cos(_t/2.0)
  q  = np.sin(_t/2.0)
  e0 = 1
  e1 = -(np.cos(_l) + np.sin(_l)*1j)
  e2 =  (np.cos(_p) + np.sin(_p)*1j)
  e3 =  (np.cos(_k) + np.sin(_k)*1j)
  w  = p * e0
  x  = q * e1
  y  = q * e2
  z  = p * e3
  ww = zeroDownFrac(w, thres)
  xx = zeroDownFrac(x, thres)
  yy = zeroDownFrac(y, thres)
  zz = zeroDownFrac(z, thres)
  if debug == True:
    print("theta   =", _t)
    print("phi     =", _p)
    print("lambda  =", _l)
    print("p (cos) = ", p)
    print("q (sin) = ", q)
    print("e0      = ", e0)
    print("e1      = ", e1)
    print("e2      = ", e2)
    print("e3      = ", e3)
    print("w       = ", w)
    print("x       = ", x)
    print("y       = ", y)
    print("z       = ", z)
    print("ww      = ", ww)
    print("xx      = ", xx)
    print("yy      = ", yy)
    print("zz      = ", zz)
  return np.array([[w, x],[y, z]])

def qasmU3Matrix2 ( _t, _p, _l, _g):
  _k = _p + _l
  _q = _g + _l
  _r = _g + _p
  _s = _r + _l
  p  = np.cos(_t/2.0)
  q  = np.sin(_t/2.0)
  e0 =  (np.cos(_g) + np.sin(_g)*1j)
  e1 = -(np.cos(_q) + np.sin(_q)*1j)
  e2 =  (np.cos(_r) + np.sin(_r)*1j)
  e3 =  (np.cos(_s) + np.sin(_s)*1j)
  w  = p * e0
  x  = q * e1
  y  = q * e2
  z  = p * e3
  return np.array([[w, x],[y, z]])

def runSimulationProjectQ(quantumCircuit, option):

  gRegisters      = {}
  simulator1      = Simulator()
  engine1         = MainEngine(backend=simulator1)

  for qreg in quantumCircuit.qregs:
    gRegisters[qreg.name] = engine1.allocate_qureg(qreg.size)

  for gate in gQuantumCircuit.data:
    gateName      = gate.operation.name.lower()
    gateParams    = gate.operation.params
    gateNumQubits = gate.operation.num_qubits
    gateNumClbits = gate.operation.num_clbits
    gateQubits    = gate.qubits

    # For Debugging
    if gateName in ["barrier", "measure"]:
      continue
  
    if debug == True: 
      print("\n")
      print(gate)
      print("Gate Name      : " + gateName)
      print("Gate Parameters: " + str(gateParams))
      print("No. of Qubits  : " + str(gateNumQubits))
      print("No. of Clbits  : " + str(gateNumClbits))

   
    #================================================#
    # Covert the list of qubits to a tuple of qubits #
    #================================================#
    qubitsTuple = ()
    for aQubit in gateQubits:
      qubitRegName = gQuantumCircuit.find_bit(aQubit)[1][0][0].name
      qubitIndex   = gQuantumCircuit.find_bit(aQubit).registers[0][1]
      theQubit     = gRegisters[qubitRegName][qubitIndex]
      qubitsTuple  = qubitsTuple + (theQubit,)
      if debug==True:
        print("aQubit         :", aQubit)
        print("Qubit Reg Name : " + qubitRegName)
        print("Qubit Index    : " + str(qubitIndex))
        print("theQubit       :", theQubit)
        print("theQubit(type) :", type(theQubit))
  
    qubitScope  = len(qubitsTuple)
    paramsCount = len(gateParams)

    #print("No. of Params  : " + str(paramsCount))



    #================================================#
    # CASE A: Gates that need a matrix as parameter  #
    #================================================#

    if gateName in ["u3", "u2", "u1", "u", "cu3", "cu", "p", "cu1", "cp"]:
      if   len(gateParams) == 3:
         gateParams2 = (gateParams[0], gateParams[1], gateParams[2], thres)
      elif len(gateParams) == 2:
         gateParams2 = (  math.pi/2.0, gateParams[0], gateParams[1], thres)
      elif len(gateParams) == 1:
         gateParams2 = ( 0000000000.0, 00000000000.0, gateParams[0], thres)
      else:
         gateParams2 = (gateParams[0], gateParams[1], gateParams[2], gateParams[3])
         #print("gateParams2 ", gateParams2)
 
      matrixParam = qasmU3Matrix(*gateParams2)

      if "cu" == gateName:
        matrixParam = qasmU3Matrix2(*gateParams2)
        #print("matrixParam ", matrixParam)

      #print("MATRIX: ", matrixParam)   
 
      if "c" in gateName:
        #print("CASE           : A2")
        projQGate   = C(qasmGateToProjectQ[gateName](matrixParam))
      else:
        #print("CASE           : A1")
        projQGate   = qasmGateToProjectQ[gateName](matrixParam)
    
      projQGate  | qubitsTuple
      continue

    #================================================#
    # CASE B: Gates with 'no' parameters             #
    #================================================#
    if   paramsCount == 0 or gateName == "u0":
      #print("CASE           : B")
      if gateName == "mcx":
        gateName = "c3x" if len(qubitsTuple) == 4  else "c4x"
      projQGate  = qasmGateToProjectQ[gateName]
      projQGate  | qubitsTuple
      continue

  
    #================================================#
    # CASE C: Gates with a single 'angle' parameter  #
    #================================================#
    if paramsCount == 1:
      angleParam = gateParams[0] 
      if gateName in ["rxx", "rzz"] + ["rx", "ry", "rz"]:
        #print("CASE           : C1", angleParam)
        #print(qasmGateToProjectQ[gateName](angleParam).matrix)
        projQGate  = qasmGateToProjectQ[gateName](angleParam)
      else:
        #print("CASE           : C2")
        projQGate  = C(qasmGateToProjectQ[gateName](angleParam))
      projQGate  | qubitsTuple
      continue
    # CASE C: END


  #====================================================#
  # Result: Get the state vector or measure the qubits #
  #====================================================#
  if "state" in option: 
    engine1.flush()
    stateVector = engine1.backend.cheat()[1]

    for regGroup in gRegisters:
      All(Measure) | gRegisters[regGroup]
    engine1.flush()

    return stateVector
  else:
    for regGroup in gRegisters:
      All(Measure) | gRegisters[regGroup]
    engine1.flush()

    observedString = ""                                                                                     
    for regGroup in gRegisters:                                                                             
      for index in range(0, len(gRegisters[regGroup])):                                                     
        observedString += str(int(gRegisters[regGroup][index]))                                             
    return observedString

# runSimulationProjectQ


#==================================================================================================#
# Simulation Function                                                                              #
#==================================================================================================#

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
   elif ("aer" in backend ) and ("qasm" in backend):
      backendSimulator = Aer.get_backend('qasm_simulator')
   elif ("aer" in backend ) and ("state" in backend):
      backendSimulator = Aer.get_backend('statevector_simulator')
   elif ("proj" in backend):
      pqOption   = "qasm" if ("qasm" in backend) else "state"
      simResults = runSimulationProjectQ(quantumCircuit, pqOption)
      gSimulationTime  = time.time() - startTime
      return simResults
   else:
      backendSimulator = Aer.get_backend('qasm_simulator')

   if ("dd" in backend) or ("aer" in backend):
     if ("state" in backend):
       _quantumCircuit = quantumCircuit.remove_final_measurements(inplace=False)
       myJob           = execute(_quantumCircuit, backendSimulator, **jobOptions)
     else:
       myJob           = execute(quantumCircuit, 
                                 backendSimulator, 
                                 **jobOptions)
     simResults        = myJob.result()
     gSimulationTime   = time.time() - startTime
     return simResults
# END: runSimulation

#==================================================================================================#
# Simulation                                                                                       #
#==================================================================================================#

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


#==================================================================================================#
# Print simulation results                                                                         #
#==================================================================================================#

printLog(logRunString + "[info] [Simulation]     Time : %s sec" % gSimulationTime, logLvlInfo, gLogLevel)
printLog(logRunString + "[xtra] [Simulation]  Results : " + str(results), logLvlExtra, gLogLevel)

if ("proj" in gBackend) and ("state" in gBackend):
  printLog(logRunString + "[RESU] [Simulation]    State : ",   logLvlResult, gLogLevel)
  PrintStateVector(results) 

if ("proj" in gBackend) and ("qasm" in gBackend):
  printLog(logRunString + "[RESU] [Simulation]    Shots : " + str(results),   logLvlResult, gLogLevel)

if ("proj" not in gBackend)  and ("qasm" in gBackend):
  shotCounts = results.get_counts(gQuantumCircuit)
  printLog(logRunString + "[RESU] [Simulation]    Shots : " + str(shotCounts),
           logLvlResult,
           gLogLevel)

if ("proj" not in gBackend) and ("state" in gBackend):
  stateVector = results.get_statevector(gQuantumCircuit)
  printLog(logRunString + "[RESU] [Simulation]    State : ",   logLvlResult, gLogLevel)
  PrintStateVector(stateVector)

if ("proj" not in gBackend) and ("unitary" in gBackend):
  unitaryMatrix = results.get_unitary(gQuantumCircuit)
  printLog(logRunString + "[RESU] [Simulation]   Matrix : \n" + str(unitaryMatrix),   logLvlResult, gLogLevel)


#==================================================================================================#
# Print resources used.                                                                            #
#==================================================================================================#


if ( gTestMode == "memo" ):
   gMaxMemoryUsage = max([gMaxSimulationMemory, gMaxCreationMemory])
   printLog(logRunString + "[info] [Resource  ]   Memory : " + str(gMaxMemoryUsage) + " MiB",
            logLvlInfo,
            gLogLevel)

gTotalRunTime = gSimulationTime + gCreationTime
printLog(logRunString + "[info] [Resource  ]     Time : " + str(gTotalRunTime) + " sec",
         logLvlInfo,
         gLogLevel)


#==================================================================================================#
# Print benchmark summary                                                                          #
#==================================================================================================#

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










