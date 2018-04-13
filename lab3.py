

SUPPORTED = set('/*-+')
OPERATORS = {
        '/': lambda a, b: a / b,
        '*': lambda a, b: a * b,
        '-': lambda a, b: a - b,
        '+': lambda a, b: a + b,
}

class Node(object):
    """Tree node"""

    def __init__(self, data):
        self.l = None
        self.r = None
        self.data = data

    def insert(self, node):
        if self.l is None:
            self.l = node
        elif self.r is None:
            self.r = node
        else:
            lw = self.l.get_weight()
            rw = self.r.get_weight()
            if lw < rw:
                self.l.insert(node)
            else:
                self.r.insert(node)

    def get_weight(self):
        w = 1
        if self.l: w += self.l.get_weight()
        if self.r: w += self.r.get_weight()
        return w

    def __str__(self, depth=0):
        ret = ""
        if self.r != None:
            ret += self.r.__str__(depth + 1)
        ret += "\n" + ("    "*depth) + str(self.data)
        if self.l != None:
            ret += self.l.__str__(depth + 1)
        return ret

    def result(self):
        if self.data in SUPPORTED:
            return OPERATORS[self.data](self.l.result(), self.r.result())
        else:
            return self.data


if __name__ == "__main__":

    root = Node(input("Enter root element operator (%s):" % (", ".join(SUPPORTED), )))
    current = root
    allowed = False
    while True:
        current = Node("*?*")
        root.insert(current)
        print(root)
        data = input('Enter node.\n? - to skip.\n! - to stop.\nsupported operators: +, -, *, /\n?: ')
        if data == "!" or (not allowed and data == "?"):
            break

        if data in SUPPORTED:
            current
            continue
        data = int(data)
        current.data = data
        allowed = True

    print("Tree:\n%s\nResult: %s" % (root, root.result(), ))
