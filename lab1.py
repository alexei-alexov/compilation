#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""This script contains."""
import sys
import os
import re
from enum import Enum


PASCAL_O = [
    '+', '-', '*', '/', '%',                   # Arithmetic Operators
    '=', '<>', '>', '<', '>=', '<=', '><',           # Relational Operators
    '&', '|', '!', '~', '<<', '>>',            # Bit Operators
    ':='
]
PASCAL_BO = ['and', 'and then', 'or', 'or else', 'not', ] # Boolean Operators

PASCAL_HASH_CHAR = r'\#\d+'
PASCAL_SINGLE_CHAR = r"'.'"
PASCAL_STRING = r'".*"'

PSC_VAR = r'\w+'
PSC_ASSIGN = r' := '
PSC_STRING_PART = r'(?:%s)' % ("|".join(map(lambda x: "(%s)" % (x, ), [PASCAL_HASH_CHAR, PASCAL_SINGLE_CHAR, PASCAL_STRING])))

PSC_LEFT_PART = PSC_VAR + PSC_ASSIGN
PSC_RIGHT_PART = r"(%s(?: \+ %s)*)\ *;" % (PSC_STRING_PART, PSC_STRING_PART, )
PSC_STRING_CONST = PSC_LEFT_PART + PSC_RIGHT_PART

RE_PSC_STRING_CONST = re.compile(PSC_STRING_CONST, re.I)


def get_consts():
    source_filename = input("Enter `pascal` source file name: ")
    result_filename = input("Enter result file name or leaver empty for default: ")
    if not result_filename:
        result_filename = "result.consts"

    ASSIGN_PATTERN = re.compile(r'(\w+ := .*?);')
    PS_HASH_PAT = re.compile(PASCAL_HASH_CHAR)
    PS_SINGLE_CHAR_PAT = re.compile(PASCAL_SINGLE_CHAR)
    PS_STR_PAT = re.compile(PASCAL_STRING)

    with open(source_filename) as source_file, open(result_filename, 'w', encoding='utf-8') as result_file:
        for line in source_file:
            print('---')
            line = line.strip()
            print(line)
            match = ASSIGN_PATTERN.match(line)
            if match:
                print(match.groups())
                match = match.group(1)
                left, right = match.split(' := ', 1)
                result = []
                for part in right.split('+'):
                    part = part.strip()
                    print('part: ', part)
                    if PS_HASH_PAT.match(part):
                        try:
                            result.append(chr(int(part[1:])))
                        except:
                            result.append('?')
                    elif PS_SINGLE_CHAR_PAT.match(part):
                        result.append(part[1])
                    elif PS_STR_PAT.match(part):
                        result.append(part[1:-1])
                result_file.write('%s = %s\n' % (left, ''.join(result)))


def split_pascal():
    source_filename = input("Enter `pascal` source file name: ")
    result_filename = input("Enter result file name or leaver empty for default: ")
    if not result_filename:
        result_filename = "result." + source_filename.split('.')[-1]

    o_str_pattern = "|".join(map(re.escape, sorted(PASCAL_O, key=len, reverse=True)))
    bo_str_pattern = "|".join(map(re.escape, sorted(PASCAL_BO, key=len, reverse=True)))
    pattern = re.compile(
        r"(\s*((%s)|((?<!\w)(%s)(?!\w)))\s*)" % (o_str_pattern, bo_str_pattern, ),
        re.I)

    SEP = os.linesep
    subber = SEP + r"\2" + SEP
    splitter = re.compile(r'(?:;)[^%s]' % (SEP, ))

    with open(source_filename) as source_file, open(result_filename, 'w') as result_file:
        for full_line in source_file:
            for line in splitter.split(full_line):
                result_file.write(pattern.sub(subber, line))

class ECState(Enum):
    OUT, SLASH, MLC, LC, MLCSTAR = range(5)


def extract_comments():
    source_filename = input("Enter `c` source file name: ")
    result_filename = input("Enter result file name or leaver empty for default: ")
    if not result_filename:
        result_filename = "result." + source_filename.split('.')[-1]

    with open(source_filename) as source_file, open(result_filename, 'w') as result_file:

        state = ECState.OUT
        buffer = []

        def reset():
            buffer.clear()

        def flush():
            result_file.write("".join(buffer))
            reset()

        while True:
            c = source_file.read(1)
            if not c: break
            buffer.append(c)

            # ------------------
            if state == ECState.OUT:
                if c == '/':
                    state = ECState.SLASH
                else:
                    flush()
            # ------------------
            elif state == ECState.SLASH:
                if c == '/':
                    state = ECState.LC
                elif c == '*':
                    state = ECState.MLC
                else:
                    state = ECState.OUT
                    flush()
            # ------------------
            elif state == ECState.MLC:
                if c == '*':
                    state = ECState.MLCSTAR
            # ------------------
            elif state == ECState.MLCSTAR:
                if c == '/':
                    state = ECState.OUT
                    reset()
                else:
                    state == ECState.MLC
            # ------------------
            elif state == ECState.LC:
                if c == '\n':
                    state = ECState.OUT
                    reset()
                    result_file.write('\n')



if __name__ == "__main__":
    n = int(input("Enter lab1 task number: "))
    {1: split_pascal,
     2: extract_comments,
     3: get_consts}.get(n, lambda: print("Wrong task number"))()
