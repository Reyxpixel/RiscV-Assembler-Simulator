# RiscV-Assembler-Simulator
[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/Reyxpixel/RiscV-Assembler-Simulator)

This project provides a command-line toolset for assembling and simulating a subset of the 32-bit RISC-V instruction set architecture. It consists of two main Python scripts: an assembler that converts RISC-V assembly code into binary machine code, and a simulator that executes this machine code.

## Features

*   **Two-Stage Process**: Assemble your RISC-V code first, then run it on the simulator.
*   **Label Support**: The assembler resolves labels for branch and jump instructions.
*   **Register and Memory Simulation**: The simulator maintains the state of 32 general-purpose registers and a simple data/stack memory model.
*   **Execution Trace**: The simulator generates a detailed trace file showing the state of the Program Counter (PC) and all registers after each instruction is executed.
*   **Error Handling**: Basic error checking for invalid instructions, incorrect number of arguments, and unknown registers.

## File Descriptions

*   `Assembler.py`: A Python script that takes a RISC-V assembly file as input and outputs a file containing the corresponding 32-bit binary machine code.
*   `Simulator.py`: A Python script that reads a machine code file and simulates its execution on a RISC-V processor. It outputs a trace file with register states and the final memory state.

## Supported Instructions

The assembler and simulator support the following instructions:

| Type    | Instructions                                    |
|:--------|:------------------------------------------------|
| **R-type**  | `add`, `sub`, `slt`, `srl`, `or`, `and`       |
| **I-type**  | `lw`, `addi`, `jalr`                            |
| **S-type**  | `sw`                                            |
| **B-type**  | `beq`, `bne`                                    |
| **J-type**  | `jal`                                           |
| **Custom**  | `rst` (reset registers), `halt` (stop execution)|

## Usage

To use the toolset, you need Python 3 installed. Follow the two steps below.

### Step 1: Assemble the Assembly Code

Create an assembly file (e.g., `input.asm`) with supported RISC-V instructions. Then, run the assembler from your terminal to generate the machine code.

**Command:**
```bash
python Assembler.py <input_assembly_file> <output_machine_code_file>
```

**Example:**
```bash
python Assembler.py input.asm machine_code.txt
```
This will read the assembly code from `input.asm` and write the resulting 32-bit binary instructions to `machine_code.txt`, with one instruction per line.

### Step 2: Simulate the Machine Code

Use the machine code file generated in the previous step as input for the simulator.

**Command:**
```bash
python Simulator.py <input_machine_code_file> <output_trace_file>
```

**Example:**
```bash
python Simulator.py machine_code.txt trace.txt
```
This will execute the instructions from `machine_code.txt` and produce `trace.txt`. The trace file will contain:
1.  A line-by-line log of the program counter and the values of all 32 registers after each instruction's execution.
2.  The final state of all data memory locations at the end of the simulation.

## Assembly Code Syntax

Instructions should follow standard RISC-V syntax.

*   **Labels:** End a label name with a colon.
    ```assembly
    my_label: add t0, t1, t2
    ```
*   **R-type:** `op rd, rs1, rs2`
    ```assembly
    add t0, t1, t2
    ```
*   **I-type:** `op rd, rs1, immediate`
    ```assembly
    addi a0, a1, -20
    ```
*   **Load/Store:** Use the `offset(base)` syntax. The assembler automatically handles this format.
    ```assembly
    lw t0, 16(sp)
    sw t1, 0(s0)
    ```
*   **B-type:** `op rs1, rs2, label`
    ```assembly
    beq s0, s1, my_label
    ```
*   **J-type:** `op rd, label`
    ```assembly
    jal ra, my_label
