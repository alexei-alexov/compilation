#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Лабораторна робота № 6-7
Формування проміжного коду.

Розробити програму формування проміжного коду та послідовності тріад
відповідно до сформованого дерева операцій. Порядок розробки програми та
вимоги до неї:
1. На вхід подається вираз, що містить арифметичні операції та оператор
присвоєння, операнди.
2. Відповідно до введеного виразу програма формує обернений польський
запис. Вивести його.
3. За сформованим польським записом виразу створити в оперативній
пам'яті дерево операцій та вивести його на екран.
4. Сформувати проміжний код виразу з допомогою команд Асемблера.
Вивести всі проміжні етапи та остаточний результат.
5. Сформувати послідовність тріад. Виявити в ній тотожні ділянки та
виключити їх (провести оптимізацію). Вивести початкову та
оптимізовану послідовність тріад.
"""
import re
from operator import truediv, mul, add, sub
from collections import deque


TOKENS = (NUM, VAR, OPERATOR) = range(3)

OPERATOR_PATTERN = re.compile(r'[*/\-+=]')
VAR_PATTERN = re.compile(r'[a-zA-Z][\w_]*')
NUM_PATTERN = re.compile(r'\d+')

STRUCT = (TOKEN, TYPE) = range(2)

OPERATORS = {
    '/': truediv,
    '*': mul,
    '-': sub,
    '+': add,
}

OP_PRIORITIES = {
    '*': 5,
    '/': 5,
    '+': 3,
    '-': 3,
    '=': 1
}


def get_op_priority(operator):
    return OP_PRIORITIES[operator]


def parse_expression():

    var_pool = {}

    def assign(key, value):
        var_pool[key] = value
    OPERATORS['='] = assign


    _id = 0
    def get_obj_id():
        """Generate unique id nodes and triades."""
        nonlocal _id
        _id += 1
        return _id

    node_cache = {}
    class Node(object):
        """Single token class"""

        def __init__(self, token, t_type):
            self.token = token
            self.t_type = t_type
            self._id = get_obj_id()
            node_cache[(token, t_type)] = self

        def tree(self, depth=0):
            return "\n" + ("    " * depth) + str(self.token)

        def result(self):
            if self.t_type == VAR:
                if not var_pool[self.token]:
                    var_pool[self.token] = int(input("Enter value for %s: " % (self.token, )))
                return var_pool[self.token]
            else:
                return self.token

        def __str__(self):
            return " [Node #%s (%s)] " % (self._id, self.token, )


    def get_node(token, t_type):
        if (token, t_type) in node_cache:
            return node_cache[(token, t_type)]
        else:
            return Node(token, t_type)

    triada_cache = {}
    class Triada(object):
        """This class represents trade of (a, b, operator)"""

        FORMAT = "(%s, %s, %s)"


        def __init__(self, a, b, operator):
            self.a = a
            self.b = b
            self.operator = operator
            self._id = get_obj_id()
            triada_cache[(a, b, operator)] = self

        def to_polish(self, r=False):
            """Return string of polish representation."""
            if r:
                return Triada.FORMAT % (
                    self.operator,
                    self.a.to_polish(True) if isinstance(self.a, Triada) else self.a,
                    self.b.to_polish(True) if isinstance(self.b, Triada) else self.b, )
            else:
                return Triada.FORMAT % (
                    self.operator,
                    ("^" + str(self.a._id)) if isinstance(self.a, Triada) else self.a,
                    ("^" + str(self.b._id)) if isinstance(self.b, Triada) else self.b, )

        def to_reverse_polish(self, r=False):
            """Return string of reverse polish representation."""
            if r:
                return Triada.FORMAT % (
                    self.a.to_reverse_polish(True) if isinstance(self.a, Triada) else self.a,
                    self.b.to_reverse_polish(True) if isinstance(self.b, Triada) else self.b,
                    self.operator, )
            else:
                return Triada.FORMAT % (
                    ("^" + str(self.a._id)) if isinstance(self.a, Triada) else self.a,
                    ("^" + str(self.b._id)) if isinstance(self.b, Triada) else self.b,
                    self.operator, )

        def tree(self, depth=0):
            """Return reccursive tree representation."""
            ret = ""
            if self.a != None:
                ret += self.a.tree(depth + 1)
            ret += "\n" + ("    "*depth) + str(self.operator)
            if self.b != None:
                ret += self.b.tree(depth + 1)
            return ret

        def result(self):
            return OPERATORS[self.operator](self.a.result(), self.b.result())

        def __str__(self):
            return " [Triada #%s (%s %s %s)] " % (
                self._id,
                ("^" + str(self.a._id)) if isinstance(self.a, Triada) else self.a,
                self.operator,
                ("^" + str(self.b._id)) if isinstance(self.b, Triada) else self.b, )

    def get_triada(a, b, operator):
        if (a, b , operator) in triada_cache:
            return triada_cache[(a, b , operator)]
        else:
            return Triada(a, b, operator)

    def parse_triade(tokens):
        if len(tokens) == 1:
            return get_node(*tokens[0])

        stack = deque()

        for n, token in enumerate(tokens):
            if token[TYPE] == NUM or token[TYPE] == VAR:
                stack.append(get_node(*token))
            elif token[TYPE] == OPERATOR:
                b = stack.pop()
                a = stack.pop()
                stack.append(get_triada(a, b, token[TOKEN]))
        print("stack: ", stack)
        return stack[0]

    expression = input('Enter expression: ')
    stack = deque()
    polish_stack = deque()
    polish = []

    tokens = (token.strip() for token in expression.split(' '))

    for token in tokens:
        if OPERATOR_PATTERN.match(token):
            while (stack and
                   get_op_priority(stack[-1][TOKEN]) >= get_op_priority(token)):
                polish_stack.append(stack.pop())
            stack.append((token, OPERATOR))
        elif VAR_PATTERN.match(token):
            if token not in var_pool:
                var_pool[token] = None
            polish_stack.append((token, VAR))
        elif NUM_PATTERN.match(token):
            polish_stack.append((int(token), NUM))

    while stack:
        polish_stack.append(stack.pop())

    print("HELLO: %s" % (list(polish_stack), ))
    root_triada = parse_triade(list(polish_stack))
    print("1: ", root_triada.to_reverse_polish(True))
    print("2: ", root_triada.tree())
    print("result: %s" % (root_triada.result(), ))
    print("tokens:\n%s" % ("\n".join(map(str, triada_cache.values()), )))


if __name__ == "__main__":
    parse_expression()