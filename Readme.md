What is this ?
==============
This is a stack of education tools that does cycle accurate simulation of a virtual 32-bit CPU, named JN, to demonstrate how aliasing, pipeline bubbles (fetch/decode stall) and branch flushes affect performance. CPU is based on Harvard Architecture and separates program and data memory busses, each has 32-bit width.

Add first only timer timer peripheral will be implemented but eventually, some DMA controllers, MMU and peripherals will be added.

Registers
=========
JN has 16 32-bit registers:

A, X, Y, SP, PC, SR, R0, R1, R2, R3, R4, R5, R6, R7, R8, R9

- A     : Accumulator which is often used as result of an operation.
- X, Y  : Intended to be used as index registers for indexed addressing modes.
- SP    : Stack pointer
- PC    : Program counter
- SR    : Status register
- R0-R9 : General purpose registers

Instruction Code Encoding
==========================
Opcodes consist of 3 condition bits and 5 opcode bits.

    8      5            0    
    +------+------------+
    + COND |   OPCODE   |
    +-------------+-----+

Condition bits
--------------------
Instructions will only be executed if conditions are met. This can be used to skip a small amount of instructions instead of branching to prevent pipeline flushes.

    C2 C1 C0  COND
     0  0  0  ALWAYS    Always (Default)
     0  0  1  Z         Zero (Equals)
     0  1  0  NZ        Not zero (Not equals)
     0  1  1  GT        Greater than
     1  0  0  GTE       Greater than or equel
     1  0  1  LT        Less than
     1  1  0  LTE       Less than or equal
     1  1  1  V         Overflow
    
Addressing modes
================
JN is based on a **load/store architecture**. Only load (LD) and store (ST) architectures support the following addressing modes. All other instructions can **only operate on registers.**

LD and ST instructions are followed by one byte addressing mode encoded as:

    8               4              0
    +---------------+---------------+
    |  SRC/DST Reg  |   Addr Mode   |
    +---------------+---------------+

LD instructions will **load** to **dst reg** from **following operand** with specified **addressing mode**.

ST instructions will **store** to **following operand** with specified **addressing mode** from **src reg**.

SRC/DST Reg encoding
--------------------

     0  0  0  0   A
     0  0  0  1   X
     0  0  1  0   Y
     0  0  1  1   SP
     0  1  0  0   PC
     0  1  0  1   SR
     0  1  1  0   R0
     0  1  1  1   R1
     1  0  0  0   R2
     1  0  0  1   R3
     1  0  1  0   R4
     1  0  1  1   R5
     1  1  0  0   R6
     1  1  0  1   R7
     1  1  1  0   R8
     1  1  1  1   R9

There are 4 addressing modes: Immediate, Direct, Indirect, Indexed with various operand sizes.

- IMM8, IMM16, IMM32: Immediate values. Syntax: #
                      i.e. `LD A, #0x09` stores 0x09 into register A.
                      Assembler picks the addressing mode automatically by the value. 0x15 is IMM8, 0x0015 is IMM16, 0x00000015 is IMM32.
- DIR32             : Direct value. Syntax: none
                      The value in the address will be stored into destionation location.
                      i.e. `LD A, 0xDEAD1615` will store the 32-bit value in the 32-bit address into A.
- IND32             : Indirect value. Syntax: *
                      The value in the address stored in operand  is stored into destination location.
                      i.e. `LD A, *0xDEAD1615` first fetches 32-bit address from 0xDEAD1615 and then fetches the value in that 32-bit location and stores it into register A.
- IDX8, IDX16       : Indexed addressing. Syntax OFFSET + BASE
                      Load the value in the effective address computed by OFFSET + BASE,
                      where BASE can be X, Y, SP or PC registers.
                      i.e. `LD A, 0x15 + X` will load the value in X + 0x15 into A.
                      Similarly 16-bit variant is also available
                      i.e. `LD A, 0x1415 + X`

Addressing Mode Encoding
------------------------
    A3 A2 A1 A0
     0  0  0  0   IMM8
     0  0  0  1   IMM16
     0  0  1  0   IMM32
     0  0  1  1   DIR32
     0  1  0  0   IND32
     0  1  0  1   IDX8_A
     0  1  1  0   IDX8_X
     0  1  1  1   IDX8_Y
     1  0  0  0   IDX8_SP
     1  0  0  1   IDX8_PC
     1  0  1  0   IDX16_A
     1  0  1  1   IDX16_X
     1  1  0  0   IDX16_Y
     1  1  0  1   IDX16_SP
     1  1  1  0   IDX16_PC
     1  1  1  1   RESERVED
    
Operands
========

Load/Store instructions
-----------------------
Load/Store instructions are followed by a byte encoding addressing mode and src/dst register information. Then it is followed by operand with size depending on the addressing mode.

A load/store instruction has a fixed 2 byte size which is [3 COND BITS + 5 OPCODE BITS] + [8-bit ADDR MODE]. Operands can be 1 to 4 bytes. So, this makes load/store instruction sizes 3 to 6 bytes.

Other instructions
------------------
All other instructions operate on registers. Each register is encoded in 4-bits. So, n operands will be encoded in ceil(n*4/8) bytes.

For example:

* 1 operand will be 4-bits and stored in 1 byte.
* 2 operands will be 8-bits and stored in 1 byte.
* 3 operands will be 12-bits and stored in 2 bytes.

     ADD.X R0, R1, R2 ; R0 = R1 + R2      1 byte instruction + 2 byte operands = 3 bytes
     ADD   R2, R3     ; R2 = R2 + R3      1 byte instruction + 1 byte opreand  = 2 bytes

Instruction Set Summary
=======================
Instruction sets suffixed with .X denotes extended instrcutions which expects 3 operands other instructions expect 0 to 2 operands.

?pseudo codes: CLR X -> LD X, #0x00000000?
Define constants: DCB, DCH, DCW
Each define supports lists by comma operator
DCB supports character arrays (not c-strings) with "" -- to create a string it should be used with comma operator
i.e. helloStr DCB "Hello", 0
DCB supports single characters ''

EQU is like define but only accepts numeric values? 

?pseudo codes?

- Misc (1)
  NOP
- Integer arithmetic (11)
  ADD[.X], SUB[.X], MUL[.X], DIV[.X] , MOD, INC, DEC
- Binary (6)
  AND, OR, XOR, NOT, SHL, SHR
- Transfer (3)
  LD, ST, MOV
- Calling (2)
  CALL, RET
- Comparision (1)
  CMP
- Branching (7)
  JMP, JE, JNE, JG, JGE, JL, JLE

Instruction Sets
================
    +-------+------------+-----------------+----------------+--------+------+
    |       |            |  Effects on SR  |   Description  | Cycles | Size |
    | Inst  |  Operands  +-+-+-+-+-+-+-+-+-+----------------+--------+------+
    |       |            |-|-|-|-|-|N|Z|C|V|                |               |
    +-------+------------+-+-+-+-+-+-+-+-+-+----------------+--------+------+
    |  ADD  | Ra, Rb     | | | | | |N|Z|C|V| Ra = Ra + Rb   |   1    |  2   |
    +-------+------------+-+-+-+-+-+-+-+-+-+----------------+--------+------+
    | ADD.X | Ra, Rb, Rc | | | | | |N|Z|C|V| Ra = Rb + Rc   |   1    |  3   |
    +-------+------------+-+-+-+-+-+-+-+-+-+----------------+--------+------+
    |       |            | | | | | | | | | |                |        |      |
    +-------+------------+-+-+-+-+-+-+-+-+-+----------------+--------+------+
    |       |            | | | | | | | | | |                |        |      |
    +-------+------------+-+-+-+-+-+-+-+-+-+----------------+--------+------+
    |       |            | | | | | | | | | |                |        |      |
    +-------+------------+-+-+-+-+-+-+-+-+-+----------------+--------+------+
    |       |            | | | | | | | | | |                |        |      |
    +-------+------------+-+-+-+-+-+-+-+-+-+----------------+--------+------+
    |       |            | | | | | | | | | |                |        |      |
    +-------+------------+-+-+-+-+-+-+-+-+-+----------------+--------+------+
    |       |            | | | | | | | | | |                |        |      |
    +-------+------------+-+-+-+-+-+-+-+-+-+----------------+--------+------+
    |       |            | | | | | | | | | |                |        |      |
    +-------+------------+-+-+-+-+-+-+-+-+-+----------------+--------+------+
    
Pipeline
========
JN has three-stage pipeline.

- Fetch
- Decode
- Execute

PC always show to the instruction being decoded.

Memory/register reading happens in decode stage.

Execute write the results back.

If decode stage of n+1-th instruction depends on execute's operands it will be stalled.

What is it good for ?
---------------------
Improving instruction execution throughput by doing each stage in parallel (as much as possible)

   |1|2|3|4|5|6|7|8
---+-+-+-+-+-+-+-+-+
n  |F|D|E|F|D|E|F|D
---+-+-+-+-+-+-+-+-+
n+1| |F|D|E|F|D|E|F
---+-+-+-+-+-+-+-+-+
n+2| | |F|D|E|F|D|E
---+-+-+-+-+-+-+-+-+

Hazards
-------
If n+1-th instruction operates on n-th instructions output there might be dependency issues.

- n+1-th instruction can operate on inconsistent (old) value
- pipeline can be stalled, waiting for n+1-th dependencies to complete execution
- pipeline can forward values updated in n-th instruction down to n+1-th instruction
- pipeline can fetch next independent instruction and execute it resulting in out-of-order execution

Branches
--------
- A branch will invalidate currently prefetched instructions as the control will soon be diverted.
- For unconditional branch such as above, CPUs can be smart enough to start pre-fetching from target location. But if the branches are conditional then it is more problematic.
  - CPUs can do branch prediction to further decrease chances of pipeline flush
  - Or CPUs can do speculative execution, where it pre-fetches both possibilities and flushes the useless one afterwards.