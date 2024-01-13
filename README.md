# QASM Runner and MQT Bench Runner

The QASM runner, `run-qasm.py`, takes a quantum circuit in the QASM format as input and simulates the circuit (while measuring the memory consumption and run time) using any of the following backend simulators:
- Qiskit Aer
- MQT DDSim
- ProjectQ

The MQT Bench runner, `run-mqt-bench.py`, can take a list of test circuits from the MQT Bench set and simulate each quantum circuit in the list by using the QASM runner `run-qasm.py` script. The `run-mqt-bench.py` script was created specifically to perform benchmarking of the simulators:
- Qiskit Aer
- MQT DDSim
- ProjectQ



## Prerequisites 

To run the `run-qasm.py` and `run-mqt-bench.py` scripts, you need to install the scripts required Python package dependencies. We suggest you install these dependencies inside a separate environment like a Python virtual environment or a Conda environment.

### Required Packages

1. `cotengra`
1. `kahypar`
1. `memory_profiler`
1. `mqt.ddsim`
1. `opt-einsum`
1. `projectq`
1. `qiskit`
1. `qiskit-aer`
1. `qiskit-terra`
1. `quimb`
1. `sparse`

### Install Required Packages

To install all required packages, use the following command:
```
pip3 install cotengra kahypar memory_profiler mqt.ddsim opt-einsum projectq qiskit qiskit-aer qiskit-terra quimb
```



## How to Use `run-qasm.py`

### Basic Usage

As a default, the `run-qasm.py` only needs the QASM file path of the quantum circuit to run the simulation. 
The default simulator backend is MQT DDSim's `qasm_simulator`.

Command Format:
```
python3 run-qasm.py <QASM filepath>
```

Example:
```
python3 run-qasm.py MQTBench/grover-noancilla_indep_qiskit_010.qasm
```

Sample Out Logs:
```
+---------------------------+
| 581382 | QASM Run | START |
+---------------------------+
[run-qasm.py:581382] [info] [Start Time]     Date : 2024-01-13 15:28:20.622652
[run-qasm.py:581382] [info] [Hardware  ]      CPU :  12th Gen Intel(R) Core(TM) i3-12100
[run-qasm.py:581382] [info] [Hardware  ]   Memory : 46 GiB
[run-qasm.py:581382] [info] [Circuit   ]     QASM : MQTBench/grover-noancilla_indep_qiskit_010.qasm
[run-qasm.py:581382] [info] [Creation  ]   Status : STARTED
[run-qasm.py:581382] [info] [Creation  ]   Memory : 175.94921875 MiB
[run-qasm.py:581382] [info] [Creation  ]     Time : 0.26987576484680176 sec
[run-qasm.py:581382] [info] [QC Info   ]   Qubits : 10
[run-qasm.py:581382] [info] [QC Info   ]    Gates : 26326
[run-qasm.py:581382] [info] [QC Info   ]    Depth : 26029
[run-qasm.py:581382] [info] [Simulation]  Backend : dd-qasm
[run-qasm.py:581382] [info] [Simulation]   Status : STARTED
[run-qasm.py:581382] [info] [Simulation]  backend : dd-qasm
[run-qasm.py:581382] [info] [Simulation]    shots : 1
[run-qasm.py:581382] [info] [Simulation]   Memory : 251.07421875 MiB
[run-qasm.py:581382] [info] [Simulation]     Time : 0.8201882839202881 sec
[run-qasm.py:581382] [RESU] [Simulation]    Shots : {'1111111111': 1}
[run-qasm.py:581382] [info] [Resource  ]   Memory : 251.07421875 MiB
[run-qasm.py:581382] [info] [Resource  ]     Time : 1.0900640487670898 sec
[run-qasm.py:581382] [benc] [SUMMARY   ]     Info , 2024-01-13 15:28:20.622652, dd-qasm, grover-noancilla_indep_qiskit_010, 10, 26326, 26029, 251.07421875, 1.0900640487670898
+---------------------------+
| 581382 | QASM Run | END   |
+---------------------------+
```


### Backend Simulator Options (`back=<backend>`)

You can simulate the quantum circuit using different backend simulators by using the `back=<backend>` option of the `run-qasm.py`.

Command Format:
```
python3 run-qasm.py <QASM file> back=<backend>
```

If the `back=<backend>` option is not used, the `run-qasm.py` script will use the default `dd-qasm` option which is the MQT DDSim `qasm_simulator` backend. 

Example 1: (explicitly specifying the backend as `dd-qasm`):
```
python3 run-qasm.py MQTBench/grover-noancilla_indep_qiskit_010.qasm back=dd-qasm
```

Example 2: (specifying the backend as `projq-qasm`):
```
python3 run-qasm.py MQTBench/grover-noancilla_indep_qiskit_010.qasm back=dd-qasm
```

Note that you can put the `back=<backend>` option anywhere after the script name `run-qasm.py`. This means that the `<QASM file>` option can also be placed anywhere after the script name.

Example 3: (specifying the backend as `aer-state`):
```
python3 run-qasm.py back=aer-state MQTBench/grover-noancilla_indep_qiskit_010.qasm
```

| Backend          | Description                                       |
|------------------|---------------------------------------------------|
|`dd-qasm`         | MQT DDSim's `qasm_simulator`                      |
|`dd-qasm-path`    | MQT DDSim's `path_qasm_simulator`                 |
|`dd-qasm-hybrid`  | MQT DDSim's `hybrid_qasm_simulator`               |
|`dd-state`        | MQT DDSim's `statevector_simulator`               |
|`dd-state-hybrid` | MQT DDSim's `hybrid_statevector_simulator`        |
|`dd-unitary`      | MQT DDSim's `unitary_simulator`                   |
|`aer-qasm`        | Qiskit Aer's `qasm_simulator`                     |
|`aer-state`       | Qiskit Aer's `statevector_simulator`              |
|`projq-qasm`      | ProjectQ's simulator (without state vector output)|
|`projq-state`     | ProjectQ's simulator (with state vector output)   |


### Simulation Mode/Method Option (`mode=<mode>`)

The `mode` option is specific to MQT DDSim backends. They refer to particlular simulation methods used by some DDSim backends.

Command Format:
```
python3 run-qasm.py <QASM file> back=<backend> mode=<mode>
```

Example 1: 


### Instructions Option (`--help`)




## How to Use `run-mqt-bench.py`

The `run-mqt-bench.py` script is used for running 

```
python3 run-mqt-ddsim.py list="all-test.test"
```

