#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""This script contains."""
import sys
import os
import re
from enum import Enum


def main():
    """Main script part"""
    source_path = (input("Enter, please path to source files: ") or "src")

    # with open(os.path.join(source_path, "source.py")) as source_file:
    #     for line in source_file:


PASCAL_O = [
    '+', '-', '*', '/', '%',                   # Arithmetic Operators
    '=', '<>', '>', '<', '>=', '<=', '><',           # Relational Operators
    '&', '|', '!', '~', '<<', '>>',            # Bit Operators
    ':='
]
PASCAL_BO = ['and', 'and then', 'or', 'or else', 'not', ] # Boolean Operators


def get_consts():
    source_filename = input("Enter `pascal` source file name: ")
    result_filename = input("Enter result file name or leaver empty for default: ")
    if not result_filename:
        result_filename = "result.consts"

    c_pattern = r"""\w+\ *=\ *((".*?")|('.')|(\#))()?"""

    with open(source_filename) as source_file, open(result_filename, 'w') as result_file:
        for line in source_filename:
            # check if const part is ended.
            if re.match(r"(var)|(begin)", line, flags=re.I):
                break
            if re.search(r'(?<!:)=', line):
                result_file.write(line)


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
