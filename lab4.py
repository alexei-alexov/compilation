import re
import operator as O
from collections import deque


VAR_STATE = {}
VAR_PATTERN = re.compile(r'[a-zA-Z][\w_]*')
NUM_PATTERN = re.compile(r'\d+')

def assign(name, value):
    VAR_STATE[name] = value

OPERATORS = {
    '/': O.truediv,
    '*': O.mul,
    '-': O.sub,
    '+': O.add,
    '=': assign,
}
O_SET = set(OPERATORS.keys())
TNUM, TOP, TVAR = range(3)


def build_polish(data):
    tokens = (token for token in data.split(' '))
    stack = deque()
    types = deque()

    def check():
        if len(stack) < 3:
            return False
        if types[-1] != TOP and types[-2] != TOP:
            return True

    for n, token in enumerate(tokens, start=1):
        if VAR_PATTERN.match(token):
            types.append(TVAR)
        elif NUM_PATTERN.match(token):
            types.append(TNUM)
            token = int(token)
        elif token in O_SET:
            types.append(TOP)
        else:
            raise Exception("Compile error! Wrong token: %s. Number: %s" % (token, n))

        stack.append(token)
        while check():
            b, bt = stack.pop(), types.pop()
            a, at = stack.pop(), types.pop()
            op, _ = stack.pop(), types.pop()
            if at == TVAR:
                if a not in VAR_STATE:
                    VAR_STATE[a] = int(input("Enter value of %s: " % (a, )))
                a = VAR_STATE[a]
            if bt == TVAR:
                if b not in VAR_STATE:
                    VAR_STATE[b] = int(input("Enter value of %s: " % (b, )))
                b = VAR_STATE[b]
            stack.append(OPERATORS[op](a,b))
            types.append(TNUM)

    print("Result: %s" % (stack[0], ))

def build_rpolish(data):
    tokens = (token for token in data.split(' '))
    stack = deque()
    types = deque()

    def check():
        if len(stack) < 3:
            return False
        if types[-1] == TOP:
            return True

    for n, token in enumerate(tokens, start=1):
        if VAR_PATTERN.match(token):
            types.append(TVAR)
        elif NUM_PATTERN.match(token):
            types.append(TNUM)
            token = int(token)
        elif token in O_SET:
            types.append(TOP)
        else:
            raise Exception("Compile error! Wrong token: %s. Number: %s" % (token, n))

        stack.append(token)
        while check():
            op, _ = stack.pop(), types.pop()
            b, bt = stack.pop(), types.pop()
            a, at = stack.pop(), types.pop()
            if at == TVAR:
                if a not in VAR_STATE:
                    VAR_STATE[a] = int(input("Enter value of %s: " % (a, )))
                a = VAR_STATE[a]
            if bt == TVAR:
                if b not in VAR_STATE:
                    VAR_STATE[b] = int(input("Enter value of %s: " % (b, )))
                b = VAR_STATE[b]
            stack.append(OPERATORS[op](a,b))
            types.append(TNUM)

    print("Result: %s" % (stack[0], ))


if __name__ == "__main__":
    v = input("Polish (1) or Reverse polish (2) ? ").strip()
    if v == '1':
        with open('exp.txt', 'r') as input_file:
            build_polish(input_file.read().strip())
    elif v == '2':
        with open('rexp.txt', 'r') as input_file:
            build_rpolish(input_file.read().strip())
    else:
        print("Wrong!")
