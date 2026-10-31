import math, queue
from collections import Counter

####### Problem 1 #######

class TreeNode(object):
    # we assume data is a tuple (frequency, character)
    def __init__(self, left=None, right=None, data=None):
        self.left = left
        self.right = right
        self.data = data
    def __lt__(self, other):
        return(self.data < other.data)
    def children(self):
        return((self.left, self.right))
    
def get_frequencies(fname):
    f=open(fname, 'r')
    C = Counter()
    for l in f.readlines():
        C.update(Counter(l))
    return(dict(C.most_common()))

# given a dictionary f mapping characters to frequencies, 
# create a prefix code tree using Huffman's algorithm
def make_huffman_tree(f):
    p = queue.PriorityQueue()
    # construct heap from frequencies, the initial items should be
    # the leaves of the final tree
    for c in f.keys():
        p.put(TreeNode(None,None,(f[c], c)))

    # greedily remove the two nodes x and y with lowest frequency,
    # create a new node z with x and y as children,
    # insert z into the priority queue (using an empty character "")
    while (p.qsize() > 1):
        x = p.get()
        y = p.get()
        p.put(TreeNode(x, y, (x.data[0] + y.data[0], "")))

    # return root of the tree
    return p.get()

# perform a traversal on the prefix code tree to collect all encodings
def get_code(node, prefix="", code=None):
    if code is None:
        code = {}
    if node.left is None and node.right is None:
        # leaf: "or 0" handles an alphabet with one character
        code[node.data[1]] = prefix or "0"
    else:
        get_code(node.left, prefix + "0", code)
        get_code(node.right, prefix + "1", code)
    return code

# given an alphabet and frequencies, compute the cost of a fixed length encoding
def fixed_length_cost(f):
    return max(1, math.ceil(math.log2(len(f)))) * sum(f.values())

# given a Huffman encoding and character frequencies, compute cost of a Huffman encoding
def huffman_cost(C, f):
    return sum(f[c] * len(C[c]) for c in f)

if __name__ == "__main__":
    for fname in ['f1.txt', 'alice29.txt', 'asyoulik.txt', 'grammar.lsp', 'fields.c']:
        f = get_frequencies(fname)
        fixed = fixed_length_cost(f)
        huff = huffman_cost(get_code(make_huffman_tree(f)), f)
        print("%s | %d | %d | %.3f" % (fname, fixed, huff, huff / fixed))
