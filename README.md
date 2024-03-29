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
python3 run-qasm.py MQTBench/grover-noancilla_indep_qiskit_010.qasm back=projq-qasm
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

Example 1: (`sequential` mode for the `dd-unitary` backend): 
```
python3 run-qasm.py MQTBench/grover-noancilla_indep_qiskit_010.qasm back=dd-unitary mode=sequential
```

Example 2: (`amplitude` mode for the `dd-state-hybrid` backend):
```
python3 run-qasm.py MQTBench/grover-noancilla_indep_qiskit_010.qasm back=dd-state-hybrid mode=amplitude
```

List of backends and their possible modes:
| Backend           | Mode                 |
|-------------------|----------------------|
| `dd-unitary`      | `sequential`         |
| `dd-unitary`      | `recursive`          |
| `dd-state-hybrid` | `dd`                 |
| `dd-state-hybrid` | `amplitude`          |
| `dd-qasm-hybrid`  | `dd`                 |
| `dd-qasm-hybrid`  | `amplitude`          |
| `dd-qasm-path`    | `sequential`         |
| `dd-qasm-path`    | `pairwise_recursive` |
| `dd-qasm-path`    | `bracket`            |
| `dd-qasm-path`    | `alternating`        |
| `dd-qasm-path`    | `cotengra`           |


### Shot Count Option (`shot=<no. of shots>`)

For MQT DDSim and Qiskit Aer qasm simulators (e.g. `dd-qasm`, `aer-qasm`), the number of shots can be specified using the `shot=<no. of shots>` option. The default shot count is 1.

Command Format:
```
python3 run-qasm.py <QASM file> back=<some qasm backend> shot=<no. of shots>
```

Example: (simulation uses `dd-qasm` backend with 1024 shots): 
```
python3 run-qasm.py MQTBench/grover-noancilla_indep_qiskit_010.qasm back=dd-qasm shot=1024
```


### Testing Option (`test=<test type>`)

By default, the memory usage of the simulation is being measured. This testing option can be explicitly specified using the option `test=memo`. To turn off memory measurement during simulation, use the option `test=run`.

Command Format:
```
python3 run-qasm.py <QASM file> test=<test type>
```

Example 1: (explicitly specifying to measure memory usage [default]):
```
python3 run-qasm.py MQTBench/grover-noancilla_indep_qiskit_010.qasm test=memo
``` 

Example 2: (specifying to not measure memory usage):
```
python3 run-qasm.py MQTBench/grover-noancilla_indep_qiskit_010.qasm test=run
``` 

### Log Option (`logs=<log no.>`)

In the sample logs above, you can see log labels like `[RESU]`, `[benc]`, `[info]`, etc. There are different log categories (log number) which you can set individually to activate specific set of logs.

Log Categories/Number:
| Log No. | Log No. (Binary) | Description        |
|---------|------------------|--------------------|
| 1       | 0000001          | Prints `[benc]` logs |
| 2       | 0000010          | Prints `[err ]` logs |
| 4       | 0000100          | Prints `[info]` logs |
| 8       | 0001000          | Prints banner logs |
| 16      | 0010000          | Prints `[RESU]` logs |
| 32      | 0100000          | Prints `[visu]` logs |
| 64      | 1000000          | Prints `[xtra]` logs |

The default log number is 31 = 1 + 2 + 4 + 8 + 16 which means the follow log categories will be shown:
- 1  (00000001) - `[benc]` logs
- 2  (00000010) - `[err ]` logs
- 4  (00000100) - `[info]` logs
- 8  (00001000) - banner logs
- 16 (00010000) - `[RESU]` logs

*Example 1:* If you want to add the `[visu]` logs (log no = 32) to the default log number 31, simply add 32 and 31 and use the log number 63 = 32 + 31. The `[visu]` log shows the visual representation of the circuit being simulated so adding 32 (`[visu]` log number) to the default 31 log number will include the visual circuit to the logs.

*Example 2:* If you want to remove the following banner logs from the default set of logs,
```
+---------------------------+                                                                        
| 581382 | QASM Run | START |                                                                        
+---------------------------+
...
+---------------------------+                                                                        
| 581382 | QASM Run | END |                                                                        
+---------------------------+
```

subtract the banner log number 8 from the default log number 31. i.e. Log number without the banner 23 = 31 - 8.

### Instructions Option (`--help`)

Use the `--help` option to show the instructions for using `run-qasm.py`.

Command Format:
```
python3 run-qasm.py --help
```


## How to Use `run-mqt-bench.py`

The `run-mqt-bench.py` script is used for simulating the MQT Bench set of quantum circuits. It uses the `run-qasm.py` to run the simulation. The `run-mqt-bench.py` takes a text file that specifies the list of circuits to run.

### List of Circuits: File Format

First, we look at the convention used for naming the QASM circuit files.

MQT Bench circuit naming convention:
```
<circuit_name_prefix>_<3-digit qubit count>.qasm
```

Examples of MQT Bench circuit names:
- `qaoa_indep_qiskit_003.qasm`
- `grover-noancilla_indep_qiskit_010.qasm`
- `dj_indep_qiskit_101.qasm`
- `qft_indep_qiskit_005.qasm`
- `realamprandom_indep_qiskit_020.qasm`

Sample file that specifies a list of circuits to test:
```
                    qaoa_indep_qiskit_ : 3-15
                     ghz_indep_qiskit_ : 2-129
                     vqe_indep_qiskit_ : 3-4
           portfolioqaoa_indep_qiskit_ : 3-4
            portfoliovqe_indep_qiskit_ : 3-4
        grover-noancilla_indep_qiskit_ : 2-10
          grover-v-chain_indep_qiskit_ : 2,3,4,5
         qwalk-noancilla_indep_qiskit_ : 3-5
           qwalk-v-chain_indep_qiskit_ : 3-9+2
              graphstate_indep_qiskit_ : 3-5
                     qft_indep_qiskit_ : 2-5
                      dj_indep_qiskit_ : 2-5
                qpeexact_indep_qiskit_ : 2-5
              qpeinexact_indep_qiskit_ : 2-5
                      ae_indep_qiskit_ : 2-5
           realamprandom_indep_qiskit_ : 2-5
       groundstate_small_indep_qiskit_ : 4,12,14
```

Each line of the file can specify a (sub)list of circuits to run. The first part of the line specifies the circuit prefix name. e.g. `qwalk-noancilla_indep_qiskit_`, `qaoa_indep_qiskit_`, `realamprandom_indep_qiskit_`. The second part specifies the set of qubit counts. e.g. `2,3,4,5`, `2-129`, `3-9+2`. The circuit prefix name (first part) and the qubit counts (second part) are separated by a colon `:`. The line means you want to run circuits of the type specified by the prefix name (first part) and only the circuits of certain qubit counts specified by the set of qubit counts (second part).

There are 3 ways to specify the qubit counts.
1. List all qubit counts.  i.e. `2,3,4,5`
2. Give the minimum and maximum qubit counts. i.e. `2-129` is equivalent to  `2,3,4,5,...,128,129`
3. Give the min and max qubit counts plus increment value i.e. `3-9+2` is equivalent to `3,5,7,9`

You can use a combination of these 3 ways to specify qubit counts. For example, `2,3,4,10-20,50-60+2,90-120+5` is equivalent to `2,3,4,10,11,12,...,20,50,52,54,...,60,90,95,100,105,110,115,120`.

*Example: 1* The line `qwalk-v-chain_indep_qiskit_ : 3-9+2` means the following QASM files will be simulated
- `qwalk-v-chain_indep_qiskit_003.qasm`
- `qwalk-v-chain_indep_qiskit_005.qasm`
- `qwalk-v-chain_indep_qiskit_007.qasm`
- `qwalk-v-chain_indep_qiskit_009.qasm`

Note that script will follow the order in which you listed the lines. For example, if you listed the line `qaoa_indep_qiskit_ : 3-15` before `ghz_indep_qiskit_ : 2-129`, then all `qaoa_indep_qiskit_` circuits will be simulated first before any `ghz_indep_qiskit_` circuits. But you can have multiple lines with the same circuit prefix name so you can control the order of execution.

*Example 2:*
```
qaoa_indep_qiskit_ : 3-10
 ghz_indep_qiskit_ : 2-50 
qaoa_indep_qiskit_ : 11-15
 ghz_indep_qiskit_ : 51-129 
```

In the example above, the script will first run the `qaoa_indep_qiskit_` circuits with qubit count `3-10` then the `ghz_indep_qiskit_` circuits with qubit count `2-50`. The script will then return simulating `qaoa_indep_qiskit_` circuits with qubit count `11-15` followed by the simulation of `ghz_indep_qiskit_` circuits with qubit count `51-129`. 

You can use the list to control the order of simulation. This is particularly useful, for example, if you want to order the simulation in such a way that the circuits that you think can be simulated quickly will be simulated first.

### Running the `run-mqt-bench.py` Script

The following are the 4 options that you can specify when running the script:
- `list=<list file>` - the file that contains the list of circuits to run
- `back=<backend>` - the backend that `run-qasm.py` will use
- `qasm=<directory of QASM files>` - the folder that contains the MQT bench circuits
- `logs=<directory for logs files>` - the folder that will contain the output logs of the simulation

Command Format:
```
python3 run-mqt-bench.py back=<backend> list=<list file> qasm=<mqt bench directory> logs=<logs directory>
```

When running the `run-mqt-bench.py` make sure that the `run-qasm.py` script is in the same directory.

The following are the default values of the options if they are not specified in the command:
- `back=dd-qasm` - Default backend is `dd-qasm`
- `logs=logs` - Default `logs` directory is `logs`.
- `list=<default list>` - The default list is the one sample listed above.
- `qasm=MQTBench` - Default QASM directory is `MQTBench`.


Example 1: (uses all default values, it assumes `MQTBench` directory exists with the QASM files):
```
python3 run-mqt-bench.py
```

Example 2: (uses backend `aer-qasm` with other options having the default values):
```
python3 run-mqt-bench.py back=aer-qasm
```

## Additional Information

1. Note: The `misc` and `tools` directories contain some helpful script and files that you can use when benchmarking.
- The `MQTBench.zip` file (in `misc`) is a zip file containing the QASM files of the MQT Bench test set.
- The `mqt-bench-all.list` file (in `misc`) is a list file that can be used by the `run-mqt-bench.py` script. It list all test circuits from the `MQTBench.zip`.
- The `mqt-bench-sample.list` file (in `misc`)  is a list file that list a small set of test circuits from th `MQTBench.zip`. This list file can be useful when you are initially testing the `run-mqt-bench.py`. When you use this list to run a sample benchmarking, all simulations should be done within minutes.
- The `test-circuits` directory (in `misc`) contains QASM circuits that are helpful for debugging. It contains small circuits that test the functionality of different valid QASM gates.
- The `install-required-packages.sh` script (in `tools`) can be used to install all Python packages dependencies needed by `run-qasm.py`.
- The `test-run-mqt-bench.sh` (in `tools`) is a script that is used for testing if the `run-mqt-bench.py` works. It will run the default list of circuits three times using the `run-mqt-bench.py` but will use the following different backends: `dd-qasm`, `aer-qasm`, and `projq-qasm`.
- The `projectq-basic.py` (in `tools`) is a script that shows the basics of ProjectQ.
- The `qiskit-basic.py` (in `tools`) is script that shows the basics of Qiskit.

2. Tip: The output of the `run-mqt-bench.py` is a set of logs produced by the `run-qasm.py` simulation. To collate the benchmarking results from these logs, you can use the `cat` command to output all contents of the logs and use `grep` to filter out only the lines that summarizes the benchmark results, then save the resulting lines in a CSV (.csv) file.

Command Format:
```
cat <logs directory>/* | grep SUMMARY > <benchmark_result>.csv
```

Example:
```
cat logs/* | grep SUMMARY > benchmark_result.csv
```

An output log produced by `run-qasm.py` has the line that contains the `SUMMARY` tag. There is only one such line in an output log and it contains all relevant benchmarking information. For example. the line `[run-qasm.py:581382] [benc] [SUMMARY   ]     Info , 2024-01-13 15:28:20.622652, dd-qasm, grover-noancilla_in    dep_qiskit_010, 10, 26326, 26029, 251.07421875, 1.0900640487670898` contains the circuit name and details, the backend used, and the memory and time consumed. By outputing all these `SUMMARY` logs in an single `.csv` file, you can open the collated result using any spreadsheet program like MS Excel.



