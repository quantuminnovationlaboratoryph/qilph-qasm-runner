from projectq          import MainEngine
from projectq.backends import Simulator
from projectq.ops      import *


#==================================================================================================#
# Example 1: Engine, circuit, and gate usage.
#==================================================================================================#

def Example_001(index):
  engine0 = MainEngine()              # MainEngine is called the compiler.
  qbit1   = engine0.allocate_qubit()  # Allocate a single qubit, called 'qbit1', to the compiler.
  H       | qbit1                     # Apply the 'H' gate to qubit 'qbit1'.
  Measure | qbit1                     # Apply the 'Measure' gate to qubit 'qbit1'.
  engine0.flush()                     # Flush means to send all the instruction to the compiler.

  print("")
  print("==================================================")
  print("Example 1, Run " + str(index))
  print("==================================================")
  print(f"qbit1  type: {type(qbit1)}")
  print(f"qbit1 value: {int(qbit1)}")  # Apply the 'int' function to a qubit type to get the value.

# End of Example_001


#==================================================================================================#
# Example 2: Flushing and getting qubit amplitudes.
#==================================================================================================#

def Example_002(index):
  engine0 = MainEngine()              # Compiler = Circuit + Simulator
  qbit1   = engine0.allocate_qubit()  # Add the qubit 'qbit1' to the circuit.
  H       | qbit1                     # Add the 'H' gate to 'qbit1'. 
  engine0.flush()                     # Flush. Send all instructions to the engine (simulator).

  ampl_h0 = engine0.backend.get_amplitude('0', qbit1) # Get the amplitude for qbit1's |0>.
  ampl_h1 = engine0.backend.get_amplitude('1', qbit1) # Get the amplitude for qbit1's |1>.

  Measure | qbit1 # Add the 'Measure' gate to 'qbit1'.
  engine0.flush() # Flush. Simulate up to this point.

  ampl_m0 = engine0.backend.get_amplitude('0', qbit1) # Get the amplitude for qbit1's |0>.
  ampl_m1 = engine0.backend.get_amplitude('1', qbit1) # Get the amplitude for qbit1's |1>.

  print("")
  print("==================================================")
  print("Example 2, Run " + str(index))
  print("==================================================")
  print(f"Amplitude for |0> (after H, before Measure) : {ampl_h0}")
  print(f"Amplitude for |1> (after H, before Measure) : {ampl_h1}")
  print(f"Amplitude for |0> (after Measure and flush) : {ampl_m0}")
  print(f"Amplitude for |1> (after Measure and flush) : {ampl_m1}")

# End of Example_002


#==================================================================================================#
# Example  3: Quantum register, Simulator, and the 'All' gate
#==================================================================================================#

def Example_003(index):
  sim0 = Simulator()              # A default simulator that uses default simulation properties.
  eng0 = MainEngine(backend=sim0) # Create the compiler with 'sim0' as simulator.
  qreg = eng0.allocate_qureg(5)   # Create the 'qreg' 3-qubit quantum register.

  All(H)       | qreg # Add the 'H' gate to all qubits in the 'qreg' register.
  All(Measure) | qreg # Add the 'Measure' gate to all qubits in the 'qreg' register.
  eng0.flush()        # Flush. Perform the simulation up to this point.

  print("")
  print("==================================================")
  print("Example 3, Run " + str(index))
  print("==================================================")
  for i in range(5):
    print(f"qreg[{i}] = " + str(int(qreg[i])) )
  
# End of Example_003


#==================================================================================================#
# Example  4: Simulator's random seed (rnd_seed)
#==================================================================================================#

def Example_004(index):
  sim1  = Simulator()              # 'sim1' rnd_seed is actually randomly generated.
  eng1  = MainEngine(backend=sim1) # 'eng1' will use 'sim1' with random seed.
  qreg1 = eng1.allocate_qureg(5)   # Allocate 5-qubit register to 'eng1'.
  All(H)       | qreg1             # Apply the 'H' gate to all qubits in 'qreg1'.
  All(Measure) | qreg1             # Apply the 'Measure' gate to all qubits in 'qreg1'.
  eng1.flush()                     # Flush.

  sim2  = Simulator(rnd_seed=10)   # 'sim2' rnd_seed is set to '10'.
  eng2  = MainEngine(backend=sim2) # 'eng2' will use 'sim2' with a fixed seed.
  qreg2 = eng2.allocate_qureg(5)   # Allocate 5-qubit register to 'eng2'.
  All(H)       | qreg2             # Apply the 'H' gate to all qubits in 'qreg2'.
  All(Measure) | qreg2             # Apply the 'Measure' gate to all qubits in 'qreg2'.
  eng2.flush()                     # Flush.

  print("")
  print("==================================================")
  print("Example 4, Run " + str(index))
  print("==================================================")
  qreg1Str = ""
  qreg2Str = ""
  for i in range(5):
    qreg1Str += "0" if ( int(qreg1[i]) == 0 ) else "1"
    qreg2Str += "0" if ( int(qreg2[i]) == 0 ) else "1"
  print("qreg1 = " + qreg1Str)
  print("qreg2 = " + qreg2Str)

# End of Example_004


#==================================================================================================#
# Example  5: Getting the entire state vector using cheat() function.
#==================================================================================================#

def Example_005(index):
  sim  = Simulator()                # 'sim' rnd_seed is actually randomly generated.
  eng  = MainEngine(backend=sim)    # 'eng' will use 'sim' with random seed.
  qreg = eng.allocate_qureg(3)      # Allocate 3-qubit register to 'eng'.
  All(H)       | qreg               # Apply the 'H' gate to all qubits in 'qreg'.
  eng.flush()                       # Flush.
  stateVector = eng.backend.cheat() # Get the current state vector using 'eng' backend cheat() func.
  All(Measure) | qreg               # Apply the 'Measure' gate to all qubits in 'qreg'.
  eng.flush()                       # Flush.

  print("")
  print("==================================================")
  print("Example 5, Run " + str(index))
  print("==================================================")
  print("State Vector : " + str(stateVector[1]))
  print(str(bin(10)))

# End of Example_005


#==================================================================================================#
# Run examples here
#==================================================================================================#

# Comment out the line of the example to not run the example function.
# Or, set the second parameter (after the example function) to set the number of times to run the
# example.

examplesToRun = [
#[Example_xyz, n], 
 [Example_001, 1],
 [Example_002, 1],
 [Example_003, 1],
 [Example_004, 1],
 [Example_005, 1],
]

for example in examplesToRun:
  example_function = example[0]
  example_repeat   = example[1]
  for i in range(example_repeat):
    example_function(i+1)

print()









