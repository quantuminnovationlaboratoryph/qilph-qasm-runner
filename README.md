# QASM Runner

A python script for simulating a quantum circuit, given as a QASM file, using MQT DDSim quantum circuit simulator.

## Required Python Packages 
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

Install the Python packages using `pip`:

```
pip3 install cotengra kahypar memory_profiler mqt.ddsim opt-einsum projectq qiskit qiskit-aer qiskit-terra quimb
```

## How to Use `run-qasm.py`


Format:
```
python3 run-qasm.py <QASM file>
```

Example:
```
python3 run-qasm.py <QASM file>
```



You can run simulation by provide the script a QASM file parameter. For example:

```
python3 run-ddsim.py MQTBench/ghz_indep_qiskit_050.qasm 
```

## How to Use `run-mqt-bench.py`

The `run-mqt-bench.py` script is used for running 

```
python3 run-mqt-ddsim.py list="all-test.test"
```

## Advanced Usage

For more detailed information use the help option `--help`:

```
python3 run-ddsim.py --help
```

## Tools

The directory `tools` contains addtional scripts were be used along with the `run-ddsim.py` script we benchmarked the MQT DDSim quantum circuit simulator.

1. `run-mqt-ddsim.py`


2. `install-required-packages.sh`

```
chmod +x install-required-packages.sh
./install-required-packages.sh
```

3. `run-tasks.py` 
