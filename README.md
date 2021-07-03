# Basic MIPS Assembler
Generates machine code from MIPS assembly code. Only supports a small subset of the MIPS32 ISA. Currently working to add more instructions (j, jr, jal, etc).

## Usage:
Run MIPS_assembler.py. At the prompt, input name of file containing MIPS assembly code. Provide file path if it's not in the same folder. The following limitations apply:
* Currently supported instructions: add, sub, addi, and, or, slt, bne, beq, lw, and sw
* MIPS instructions must have spaces between commas, e.g add $s0, $s1, $s2 instead of  add $s0,\$s1,$s2 
* Branch target labels should be on a line by themselves 
* Branch target labels should be labelled earlier than they are referenced in a branch instruction

## Dependencies: 
* [Python 3.xx](https://www.python.org/downloads/)

## License
Licensed under MIT license.
