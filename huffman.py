class Node:
    def __init__(self, left_child, right_child):
        self.left_child = left_child
        self.right_child = right_child


dataset = 'MR BEAST GIVES ME MONEY, ' + \
        'HELLO EVERYNYAN, I WISH I WERE A BIRD, ' + \
        'GOD IN HIS HEAD, YOU CANT SEE ME, RICK ASHLEY'

# count character frequency
dict = {}
for c in dataset:
    if c not in dict:
        dict[c] = 1
    else:
        dict[c] += 1

# append to reverse order priority queue
queue = sorted(
        [(c, freq) for c, freq in dict.items()],
        key = lambda tuple: tuple[1]
    )

while len(queue) > 1:
    # dequeue
    (left_child, right_child) = queue[:2]
    queue = queue[2:]

    # create new node
    node = Node(left_child, right_child)

    # enqueue
    queue.append( (node, left_child[1]+right_child[1]) )
    queue = sorted(queue, key = lambda tuple: tuple[1])

# huffman tree -> lookup table
lookup_table = {}

def huffman2lookup(node, code):
    (val, freq) = node
    if isinstance(val, str):
        lookup_table[val] = code
        return
    huffman2lookup(val.left_child, code+'0')
    huffman2lookup(val.right_child, code+'1')

huffman2lookup(queue[0], '')

print('<< Lookup Table >>')
for char, code in lookup_table.items():
    print(f'{char} | {code}')

print('\nNumber of bits to send the data')
print('OLD: number of bits :', len(dataset)*8)
print('NEW: number of bits :', sum([len(lookup_table[c]) for c in dataset]))