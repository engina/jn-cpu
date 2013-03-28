#!/usr/bin/python

# Preprocessor
# supports
# 1) #define
#    Supports using other defines
# 2) #include
#    Supports relative and absolute paths

import sys
import argparse
import os.path
import utils

identifiers = {}

class PPException(Exception):
    pass

class SourceFile(object):
    def __init__(self, file):
        self.lines = []
        self.file  = file
        for line, data in enumerate(file.readlines()):
            self.lines.append(SourceLine(file, line + 1, data))

class SourceLine(object):
    def __init__(self, file, line, data):
        self.line = line
        self.data = data
        self.file = file

def preprocess(input):
    source = SourceFile(input)
    global identifiers
    toBeDeleted = []
    warnings    = []
    shifted     = 0
    incLog      = []
    def warn(file, line, msg):
        file = os.path.relpath(file.name, os.getcwd()) 
        warnings.append('PP warning: ' + file + ':' + str(line+1-shifted) + ' ' + msg + '\n')
    # iterate over a copy, because i'll delete the comments and macros right now!
    for i, line in enumerate(source.lines):
        l = line.data.strip()
        if len(l) == 0:
            toBeDeleted.append(i)
        elif l[0:1] == '#':
            if l[0:8] == '#define ':
                identifier = l[8:].split()[0]
                replacement = ''
                if len(l) > (8 + len(identifier)):
                    replacement = l[9 + len(identifier):]
                identifiers[identifier] = replacement;
                # remove from original list
            elif l[0:9] == '#include ':
                inc = l[8:].strip(' \t\n"')
                inc = os.path.abspath(os.path.join(os.path.dirname(input.name), inc))
                try:
                    with open(inc) as incf:
                        # out = {'result': [], 'warnings': []}
                        out = preprocess(incf)
                        source.lines[i+1:i+1] = out['result']
                        # keep track of how much lines are shifted so that we can subtract
                        # this offset later, when we are error reporting about a line
                        #
                        # One could think of keeping track of insertion positions and inserting later
                        # but those positions will be obsolote as soon as we start deleting lines we marked
                        # to be deleted.chr
                        shifted += len(out['result'])
                        incLog.append({'line': line, 'file': inc, 'output': out})
                        warnings.extend(out['warnings'])
                except IOError, e:
                    raise PPException('Include file "' + inc + '" could not be read [' + str(e) + ']')
            else:
                warn(input, i, ' Unknown directive "' + l.split()[0][1:] + '"')
            toBeDeleted.append(i)
        elif line.data.find(';') != -1:
            # gotta search again since python apparently does not support assign and compare
            commentIndex = line.data.find(';')
            # strip comment
            source.lines[i].data = line.data[0:commentIndex] + '\n' # \n is for normalizing preprocessor output
            # look anything is left
            if len(source.lines[i].data.strip()) == 0:
                toBeDeleted.append(i)

    for i in sorted(toBeDeleted, reverse=True):
        del source.lines[i]

    
    for i, line in enumerate(source.lines):
        for identifier in reversed(identifiers.keys()):
            replacement = identifiers[identifier]
            tokens = utils.tokenize(line.data)
            result = []
            for token in tokens:
                if token['type'] == utils.TOKEN_NORMAL:
                    token['token'] = token['token'].replace(identifier, replacement)
                result.append(token['token'])
            result = ''.join(result)
            source.lines[i].data = line.data = result

    return {'result': source.lines, 'warnings': warnings}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=file, nargs='+')
    parser.add_argument('-o', '--out', type=argparse.FileType('wb', 0), default='-')
    try:
        args = parser.parse_args()
        for i in args.input:
            out = preprocess(i)
            for line in out['result']:
                args.out.write(line.file.name + ':' + str(line.line) + ' -> ' + line.data)
            args.out.flush()
            # make sure errors are listed later so they are visible for sure
            sys.stderr.write('\nWarnings: ' + str(len(out['warnings'])) + '\n')
            sys.stderr.writelines(out['warnings'])
    except PPException, e:
        sys.stderr.write('error: ' + str(e))
        sys.exit(1)
    except Exception, e:
        raise
        sys.stderr.write('Unexpected problem: ' + str(e))
        sys.exit(1)