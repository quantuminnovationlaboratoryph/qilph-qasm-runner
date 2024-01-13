# QASM Runner

A python script for simulating a quantum circuit, given as a QASM file, using MQT DDSim quantum circuit simulator.

## Prerequisites 

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


Installation Command:
```
:pip3 install cotengra kahypar memory_profiler mqt.ddsim opt-einsum projectq qiskit qiskit-aer qiskit-terra quimb
```



## How to Use `run-qasm.py`


### Basic Usage

Format:
```
python3 run-qasm.py <QASM filepath>
```

Example:
```
python3 run-qasm.py MQTBench/ghz_indep_qiskit_050.qasm 
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

### Backend Simulator Option (`-back=<backend>`)

You can run simulation by provide the script a QASM file parameter. For example:

```
python3 run-ddsim.py MQTBench/ghz_indep_qiskit_050.qasm 
```


### Instructions Option (`--help`)

```
jmk
```



## How to Use `run-mqt-bench.py`

The `run-mqt-bench.py` script is used for running 

```
python3 run-mqt-ddsim.py list="all-test.test"
```

