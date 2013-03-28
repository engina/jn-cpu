#!/usr/bin/python
from pp import preprocess
# Sample .asm
#----------------------------------------
#
# #define FOO 0x5000
# #include "some.inc"
#
# ; some comments
# main
#     ; some indented comment
#     mov     X, 0x5000
#     mov     X, FOO
#     mov     X, *FOO
#     mov     X,#FOO ; inline comments
#     mov     X, FOO + SP
#     mov     X, INC_DEF
#     cmp     X, 0x5000
#     call    foo
#     nop
#     jmp     main

import sys
import argparse
from subprocess import call

g_args = None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=file, nargs='+')
    parser.add_argument('-o', '--out', type=argparse.FileType('wb', 0), default='a.out')
    parser.add_argument('-E', action='store_true', help='Stops after preprocessing')
    global g_args
    g_args = parser.parse_args()
    for i in g_args.input:
        ass(i)

def log(str, facility = 'ASS'):
    sys.stderr.write('[' + facility + '] ' + str + '\n')

def dbg(str):
    log(str, 'DBG')

def warn(str):
    log(str, 'WARN')

def err(str):
    log(str, 'ERR')
    sys.exit(1)

# keeping global symbols table so that if multiple assemble files are provided to the compiler
# they will be automatically linked -- pretty much like gcc.
g_symbols = []
def parse_symbol(l):
    l = l.data
    print "symbol: " + l
    if l.endswith(':'):
        warn("Trailing colon is not required for symbol names, ignoring.")
        l = l[:-1]
    global g_symbols
    g_symbols.append(l)

g_cur_section = 'code'
g_sections = dict()

ADDR_IMM8     = 0b0000
ADDR_IMM16    = 0b0001
ADDR_IMM32    = 0b0010
ADDR_DIR32    = 0b0011
ADDR_IND32    = 0b0100
ADDR_IDX8_X   = 0b1000
ADDR_IDX8_Y   = 0b1001
ADDR_IDX8_SP  = 0b1010
ADDR_IDX8_PC  = 0b1011
ADDR_IDX16_X  = 0b1100
ADDR_IDX16_Y  = 0b1101
ADDR_IDX16_SP = 0b1110
ADDR_IDX16_PC = 0b1111

ADDR_IDX_MASK      = 0b1000
ADDR_IDX_SIZE_MASK = 0b0100
ADDR_IDX_SIZE_8    = 0b0000
ADDR_IDX_SIZE_16   = 0b0100

class Operand(object):
    def __init__(self, o):
        self.mode  = 0
        self.base  = None
        self.val   = None
        o = o.strip()
        if o.find('+') != -1:
            # indexed
            self.mode |= ADDR_IDX_MASK
            regs      = ['X', 'Y', 'SP', 'PC']
            reg       = None
            offset    = None
            subOps    = o.split('+')
            if len(subOps) != 2:
                raise Exception('Indexed mode expects two sub operands, like X + #0xA015')
            a = subOps[0].strip()
            b = subOps[1].strip()
            if a in regs:
                self.base = a
                self.val = self.parseVal(b)
            elif b in regs:
                self.base = b
                self.val = self.parseVal(a)
            else:
                raise Exception('Invalid index register, you can only index using X, Y, SP, PC')
            pass
        elif o.startswith("*"):
            # indirect
            self.mode = ADDR_IND32
            self.val  = self.parseVal(o[1:])
            pass
        elif o.startswith("#"):
            # immediate
            self.val  = self.parseVal(o[1:])
            # calculate required bits to represent this value
            if self.val < 0:
                # value bits -- strip "-0b"
                b = len(bin(self.val)[3:])
            else:
                # strip "0b"
                b = len(bin(self.val)[2:])

            if b > 32:
                raise Exception('Target archtecture does not support values that cannot be represented in 32-bits')
            # IMM8, IMM16 and IMM32 is respectively 0, 1 and 2. So the following will do
            # a good job to assign addressing mode
            self.mode = (b - 1) / 8
        else:
            # direct
            self.mode = ADDR_DIR32
            self.val  = self.parseVal(o)
            pass

    # Value formats
    # regs        any of: A, X, Y, SP, PC, SR, R0, R1, R2, R3, R4, R5, R6, R7, R8, R9
    # hexadecimal 0xDEADBEAF
    # binary      0101010101010101010101010101010101010101b
    # octal       1230123012301230q
    # decimal     1234567890
    def parseVal(self, v):
        regs = ['a', 'x', 'y', 'sp', 'pc', 'sr', 'r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9']
        v = v.lower()
        if v in regs:
            return regs.index(v)
        elif v.startswith('0x'):
            # hexadecimal
            return int(v[2:], 16)
        elif v.endswith('b'):
            # binary
            return int(v[:-1], 2)
        elif v.endswith('q'):
            # octal
            return int(v[:-1], 8)
        else:
            # decimal
            return int(v)

    def __str__(self):
        return 'Operand mode: ' + str(self.mode) + ' value: ' + str(self.val) + ' index: ' + str(self.base)

def parse_instruction(l):
    l = l.data.strip()
    if l[0] == ';':
        # support for indented comments too, i like them.
        return
    l = " ".join(l.split())
    tokens   = l.split();
    opcode   = tokens.pop(0);
    operands = "".join(tokens)
    operands = operands.split(",");
    print "inst: ", l
    print opcode
    for o in operands:
        print '  ' + o + ' -> mode: ' + str(Operand(o))

def asm(lines):
    for l in  lines:
        try:
            if not l.data[0].isspace():
                parse_symbol(l)
            else:
                parse_instruction(l)
        except Exception, e:
            err(l.file.name + ':' + str(l.lineno) + ' ' + str(e))

def ass(f):
    out = preprocess(f)
    if g_args.E:
        sys.stdout.writelines(out['result'])
        return 0
    asm(out['result'])

if __name__ == '__main__':
    main();