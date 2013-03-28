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

class Operand(object):
    def __init__(self, o):
        self.dir  = None
        self.base = None
        self.val  = None
        o = o.strip()
        if o.find('+') != -1:
            # indexed
            self.dir = 'indexed'
            regs   = ['X', 'Y', 'SP', 'PC']
            reg    = None
            offset = None
            subOps = o.split('+')
            if len(subOps) != 2:
                raise Exception('Indexed mode expects two sub operands, like X + #0xA015')
            a = subOps[0].strip()
            b = subOps[1].strip()
            if a in regs:
                reg = a
            if b in regs:
                reg = b
            pass
        elif o.startswith("*"):
            # indirect
            self.dir = 'indirect'
            pass
        elif o.startswith("#"):
            # immediate
            self.dir = 'imm'
            pass
        else:
            # direct
            self.dir = 'direct'
            pass
    def __str__(self):
        return 'Operand mode: ' + self.dir + ' value: ' + str(self.val) + ' index: ' + str(self.base)

def parse_operand(o):
    o = o.lower()
    if o.endswith('b'):
        # binary
        pass
    elif o.endswith('d'):
        # decimal
        pass
    else:
        pass
    pass

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
            err(l.file + ':' + str(l.line) + ' ' + str(e))

def ass(f):
    out = preprocess(f)
    if g_args.E:
        sys.stdout.writelines(out['result'])
        return 0
    asm(out['result'])

main();