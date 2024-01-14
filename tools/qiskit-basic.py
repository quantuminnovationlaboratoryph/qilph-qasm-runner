#================================================#
#                 Qiskit Basics                  #
#================================================#


from math import pi
import math
import numpy as np
import sys
import os
from qiskit import QuantumCircuit, Aer, transpile, QuantumRegister, IBMQ, ClassicalRegister, execute
import matplotlib


#================================================#
#                Helper Functions                #
#================================================#


def HadamardWall(n):
   quantumCircuit = QuantumCircuit(n)
   for i in range(n):
      quantumCircuit.h(i)
   return quantumCircuit


def PrintBanner(myString):
   borderString  = "+-------------------------------------------------+" 
   a = math.floor( float(len(borderString) - len(myString) -2 )/2.0)
   b = len(borderString) - (len(myString) + 2 + a)
   bannerString  = "\n"
   bannerString += borderString + "\n"
   bannerString += "|" + (a * " ") + myString + (b * " ") + "|\n"
   bannerString += borderString
   bannerString += "\n"
   print(bannerString)


def PrintBanner2(bannerTitle, printItem):
  print("\n---------- " + bannerTitle + ": START ----------\n")
  print(printItem) 
  print("\n---------- " + bannerTitle + ": END   ----------\n")


def PrintOperator(qiskitOperator):
   nonZeroThreshold = 0.00001
   operatorArray  = qiskitOperator.data
   for row in operatorArray:
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


def StringOperator(qiskitOperator):
   nonZeroThreshold = 0.00001
   operatorArray  = qiskitOperator.data
   operatorString = ""
   for row in operatorArray:
      rowString = ""
      for item in row:
         realString = "{:+2.3f}".format(np.real(item))
         if ( abs(np.real(item)) < nonZeroThreshold):
            realString = "      "
         imagString = "{:+2.3f}".format(np.imag(item))
         if ( abs(np.imag(item)) < nonZeroThreshold):
            imagString = "      "
         rowString +=  "(" + realString + "," + imagString + ") "
      operatorString += rowString + "\n"
   return operatorString


def PrintStateVector(qiskitStateVector):
   nonZeroThreshold = 0.00001
   stateVectorArray = qiskitStateVector.data
   for item in stateVectorArray:
      realString = "{:+2.3f}".format(np.real(item))
      if ( np.real(item) < nonZeroThreshold):
         realString = "      "
      imagString = "{:+2.3f}".format(np.imag(item))
      if ( np.imag(item) < nonZeroThreshold):
         imagString = "      "
      print("(" + realString + "," + imagString + ") ")


def StringStateVector(qiskitStateVector):
   nonZeroThreshold = 0.00001
   stateVectorArray = qiskitStateVector.data
   stateVectorString = ""
   for item in stateVectorArray:
      realString = "{:+2.3f}".format(np.real(item))
      if ( np.real(item) < nonZeroThreshold):
         realString = "      "
      imagString = "{:+2.3f}".format(np.imag(item))
      if ( np.imag(item) < nonZeroThreshold):
         imagString = "      "
      stateVectorString += "(" + realString + "," + ")\n"
   return stateVectorString


def PrintCounts(qiskitCount):
   for stateKey in qiskitCount:
      countString = stateKey + ": " + str(qiskitCount[stateKey])
      print(countString)


def StringCounts(qiskitCount):
   countString = ""
   for stateKey in qiskitCount:
      countString += stateKey + ": " + str(qiskitCount[stateKey]) + "\n"
   return countString


#================================================#
#                     Basic                      #
#================================================#


PrintBanner("Quantum Circuit 1")
quantumCircuit1 = QuantumCircuit(3)
quantumCircuit1.h(0)
quantumCircuit1.cx(0,1)
quantumCircuit1.cx(0,2)
print(quantumCircuit1)

#================================================#

PrintBanner("State Vector Simulation")
backendSimulator = Aer.get_backend('statevector_simulator')
myExperiment     = backendSimulator.run(quantumCircuit1)
myResult         = myExperiment.result()
resultState      = myResult.get_statevector(quantumCircuit1)
PrintBanner2("Full Simulation Result", myResult)
PrintBanner2("State Vector Result"   , StringStateVector(resultState))

#================================================#

PrintBanner("Unitary Simulation")
backendSimulator = Aer.get_backend('unitary_simulator')
myExperiment     = backendSimulator.run(quantumCircuit1)
myResult         = myExperiment.result()
resultUnitary    = myResult.get_unitary(quantumCircuit1)
PrintBanner2("Full Simulation Result", myResult)
PrintBanner2("Unitary Matrix Result" , StringOperator(resultUnitary))

#================================================#

PrintBanner("Measurement")
measureCircuit = QuantumCircuit(3,3)
measureCircuit.barrier(range(3))
measureCircuit.measure(range(3),range(3))
print(measureCircuit)

PrintBanner("Circuit + Measurement")
quantumCircuit1.add_register(measureCircuit.cregs[0])
quantumCircuit2 = quantumCircuit1.compose(measureCircuit)
print(quantumCircuit2)

PrintBanner("QASM Simulation")
backendSimulator = Aer.get_backend('qasm_simulator')
myExperiment     = backendSimulator.run(transpile(quantumCircuit2,backendSimulator), shots=1024)
myResult         = myExperiment.result()
myCounts         = myResult.get_counts(quantumCircuit2)
PrintBanner2("Full Simulation Result", myResult)
PrintBanner2("Counts Result", StringCounts(myCounts))

#================================================#
#                     Gates                      #
#================================================#

PrintBanner("Identity Gate")
qc = QuantumCircuit(1)
qc.id(0)
print(qc)

backendSimulator = Aer.get_backend('unitary_simulator')
myExperiment     = backendSimulator.run(qc)
myResult         = myExperiment.result()
resultUnitary    = myResult.get_unitary(qc)
PrintBanner2("Unitary Matrix Result" , StringOperator(resultUnitary))

#================================================#

PrintBanner("Pauli X / NOT Gate")
qc = QuantumCircuit(1)
qc.x(0)
print(qc)

backendSimulator = Aer.get_backend('unitary_simulator')
myExperiment     = backendSimulator.run(qc)
myResult         = myExperiment.result()
resultUnitary    = myResult.get_unitary(qc)
PrintBanner2("Unitary Matrix Result" , StringOperator(resultUnitary))

#================================================#

PrintBanner("Pauli Y Gate")
qc = QuantumCircuit(1)
qc.y(0)
print(qc)

backendSimulator = Aer.get_backend('unitary_simulator')
myExperiment     = backendSimulator.run(qc)
myResult         = myExperiment.result()
resultUnitary    = myResult.get_unitary(qc)
PrintBanner2("Unitary Matrix Result" , StringOperator(resultUnitary))

#================================================#

PrintBanner("Pauli Z Gate")
qc = QuantumCircuit(1)
qc.z(0)
print(qc)

backendSimulator = Aer.get_backend('unitary_simulator')
myExperiment     = backendSimulator.run(qc)
myResult         = myExperiment.result()
resultUnitary    = myResult.get_unitary(qc)
PrintBanner2("Unitary Matrix Result" , StringOperator(resultUnitary))

#================================================#

PrintBanner("Hadamard Gate")
qc = QuantumCircuit(1)
qc.h(0)
print(qc)

backendSimulator = Aer.get_backend('unitary_simulator')
myExperiment     = backendSimulator.run(qc)
myResult         = myExperiment.result()
resultUnitary    = myResult.get_unitary(qc)
PrintBanner2("Unitary Matrix Result" , StringOperator(resultUnitary))

#================================================#

PrintBanner("General 1-qubit Unitary Operator")
qc = QuantumCircuit(1)
qc.u(pi/2,pi/4,pi/8,0)
print(qc)

PrintBanner("Unitary Simulation")
backendSimulator = Aer.get_backend('unitary_simulator')
myExperiment     = backendSimulator.run(qc)
myResult         = myExperiment.result()
resultUnitary    = myResult.get_unitary(qc)
PrintBanner2("Unitary Matrix Result" , StringOperator(resultUnitary))

#================================================#

PrintBanner("P Gate")
qc = QuantumCircuit(1)
qc.p(pi/2,0)
print(qc)

PrintBanner("Unitary Simulation")
backendSimulator = Aer.get_backend('unitary_simulator')
myExperiment     = backendSimulator.run(qc)
myResult         = myExperiment.result()
resultUnitary    = myResult.get_unitary(qc)
PrintBanner2("Unitary Matrix Result" , StringOperator(resultUnitary))

#================================================#


PrintBanner("Some Gates")
qc = QuantumCircuit(3)
qc.x(0)
qc.id(0)
qc.id(1)
qc.y(1)
qc.z(2)
qc.id(2)
print(qc)

PrintBanner("Unitary Simulation")
backendSimulator = Aer.get_backend('unitary_simulator')
myExperiment     = backendSimulator.run(qc)
myResult         = myExperiment.result()
resultUnitary    = myResult.get_unitary(qc)
PrintBanner2("Unitary Matrix Result" , StringOperator(resultUnitary))

#================================================#

PrintBanner("Some Gates")
qc = QuantumCircuit(3)
qc.id(0)
qc.x(0)
qc.y(1)
qc.id(1)
qc.id(2)
qc.z(2)
print(qc)

PrintBanner("Unitary Simulation")
backendSimulator = Aer.get_backend('unitary_simulator')
myExperiment     = backendSimulator.run(qc)
myResult         = myExperiment.result()
resultUnitary    = myResult.get_unitary(qc)
PrintBanner2("Unitary Matrix Result" , StringOperator(resultUnitary))

#================================================#

PrintBanner("Some Gates")
qc = QuantumCircuit(3)
qc.x(0)
qc.y(1)
qc.z(2)
print(qc)

PrintBanner("Unitary Simulation")
backendSimulator = Aer.get_backend('unitary_simulator')
myExperiment     = backendSimulator.run(qc)
myResult         = myExperiment.result()
resultUnitary    = myResult.get_unitary(qc)
PrintBanner2("Unitary Matrix Result" , StringOperator(resultUnitary))

#================================================#

PrintBanner("CNOT Gate")
qc = QuantumCircuit(2)
qc.cx(0,1)
print(qc)

PrintBanner("Unitary Simulation")
backendSimulator = Aer.get_backend('unitary_simulator')
myExperiment     = backendSimulator.run(qc)
myResult         = myExperiment.result()
resultUnitary    = myResult.get_unitary(qc)
PrintBanner2("Unitary Matrix Result" , StringOperator(resultUnitary))

#================================================#

PrintBanner("SWAP Gate")
qc = QuantumCircuit(2)
qc.swap(0,1)
print(qc)

PrintBanner("Unitary Simulation")
backendSimulator = Aer.get_backend('unitary_simulator')
myExperiment     = backendSimulator.run(qc)
myResult         = myExperiment.result()
resultUnitary    = myResult.get_unitary(qc)
PrintBanner2("Unitary Matrix Result" , StringOperator(resultUnitary))

#================================================#

PrintBanner("Controlled U Gate")
qc = QuantumCircuit(2)
qc.cu(pi/2,pi/2,pi/2, 0, 0, 1)
print(qc)

PrintBanner("Unitary Simulation")
backendSimulator = Aer.get_backend('unitary_simulator')
myExperiment     = backendSimulator.run(qc)
myResult         = myExperiment.result()
resultUnitary    = myResult.get_unitary(qc)
PrintBanner2("Unitary Matrix Result" , StringOperator(resultUnitary))

#================================================#

PrintBanner("Toffoli / CCNOT / CCX Gate")
qc = QuantumCircuit(3)
qc.ccx(0,1,2)
print(qc)

PrintBanner("Unitary Simulation")
backendSimulator = Aer.get_backend('unitary_simulator')
myExperiment     = backendSimulator.run(qc)
myResult         = myExperiment.result()
resultUnitary    = myResult.get_unitary(qc)
PrintBanner2("Unitary Matrix Result" , StringOperator(resultUnitary))


#================================================#
#                  Transpiling                   #
#================================================#


PrintBanner("Original Swap Circuit")
qc = QuantumCircuit(2)
qc.swap(0,1)
print(qc)

PrintBanner("Decomposed Swap Circuit")
print(qc.decompose())

#================================================#

PrintBanner("Toffoli Circuit")
qc = QuantumCircuit(3)
qc.ccx(0,1,2)
print(qc)

PrintBanner("Decomposed Toffoli Circuit")
print(qc.decompose())

#================================================#

PrintBanner("Toffoli Circuit")
qc = QuantumCircuit(3)
qc.ccx(0,1,2)
print(qc)

PrintBanner("Transpiled: Basis = {u, cx}")
tqc = transpile(qc, basis_gates=['u','cx'], optimization_level=1)
print(tqc)

#================================================#

PrintBanner("Original Swap Circuit")
qc = QuantumCircuit(2)
qc.cx(1,0)
print(qc)

#PrintBanner("Transpiled Swap Circuit")
#tqc = transpile(qc, basis_gates=['cx'], optimization_level=2)
#print(tqc)

PrintBanner("Unitary Simulation")
backendSimulator = Aer.get_backend('unitary_simulator')
myExperiment     = backendSimulator.run(qc)
myResult         = myExperiment.result()
resultUnitary    = myResult.get_unitary(qc)
#print(resultUnitary)
PrintBanner2("Unitary Matrix Result" , StringOperator(resultUnitary))


PrintBanner("State Vector Simulation")
backendSimulator = Aer.get_backend('statevector_simulator')
myExperiment     = backendSimulator.run(qc)
myResult         = myExperiment.result()
resultState      = myResult.get_statevector(qc)
#PrintBanner2("Full Simulation Result", myResult)

print(resultState)
PrintBanner2("State Vector Result"   , StringStateVector(resultState))

#tqc.draw('mpl').savefig("circuit.png", dpi=500)

#PrintBanner("Latex Picture")
#latexDiagram = tqc.draw('latex_source')

#print(latexDiagram)

#latexFile = open('diagram.tex','w')
#latexFile.write(latexDiagram)
#latexFile.close()

#================================================#


PrintBanner("Circuit")
qc = QuantumCircuit(1)
qc.rx(pi/4,0)
print(qc)

PrintBanner("RX as U")
tqc = transpile(qc, basis_gates=['u'])
print(tqc)




q2 = QuantumRegister(3,"qreg")
c2 = ClassicalRegister(3,"creg")
qc2 = QuantumCircuit(q2,c2)


qc2.h(q2[1])

qc2.measure(q2,c2)
job = execute(qc2,Aer.get_backend('qasm_simulator'),shots=1000)
counts = job.result().get_counts(qc2)
print("HERE")
print(counts) # counts is a dictionary

print("======================")
#================================================#

PrintBanner("Quantum Circuit 1")
quantumCircuit1 = QuantumCircuit(2)
quantumCircuit1.h(0)
quantumCircuit1.cz(1,0)
print(quantumCircuit1)

PrintBanner("Measurement")
measureCircuit = QuantumCircuit(2,2)
measureCircuit.barrier(range(2))
measureCircuit.measure(range(2),range(2))
print(measureCircuit)

PrintBanner("Circuit + Measurement")
quantumCircuit1.add_register(measureCircuit.cregs[0])
quantumCircuit2 = quantumCircuit1.compose(measureCircuit)
print(quantumCircuit2)

PrintBanner("QASM Simulation")
backendSimulator = Aer.get_backend('qasm_simulator')
myExperiment     = backendSimulator.run(transpile(quantumCircuit2,backendSimulator), shots=1000)
myResult         = myExperiment.result()
myCounts         = myResult.get_counts(quantumCircuit2)
PrintBanner2("Full Simulation Result", myResult)
PrintBanner2("Counts Result", StringCounts(myCounts))

