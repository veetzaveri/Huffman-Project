# Node Class to represent the nodes in Huffman Encoding Tree
class Node:
    # Default Constructor method of the Node Class
    def __init__(self, label, data, child=None):
        self.label = label
        self.data = data
        self.child = child

    # Object to String method of the Node Class
    def __str__(self):
        return self.label + "(" + str(self.data) + ")"


# ___End of Node Class___


# Method for printing Pre-order traversal of the Tree, this method receive Root Node of the Tree as parameter.
def pre_order_traverse(root):
    print(root, end=" --> ")  # Print current node.
    if root.child is None:  # True when root node has No child nodes. (Termination Condition for Recursive Call)
        return
    else:
        pre_order_traverse(root.child[0])  # Recursive Call with Left Child as parameter.
        pre_order_traverse(root.child[1])  # Recursive Call with Right Child as parameter.


# ___End of pre_order_traverse method ___


# Optional Method (In case: In-order traversal is required)
# Method for printing In-order traversal of the Tree, this method receive Root Node of the Tree as parameter.
def in_order_traverse(root):
    if root.child is None:  # True when root node has No child nodes. (Termination Condition for Recursive Call)
        print(root, end=" --> ")  # Print current node.
    else:
        in_order_traverse(root.child[0])  # Recursive Call with Left Child as parameter.
        print(root, end=" --> ")  # Print current node.
        in_order_traverse(root.child[1])  # Recursive Call with Right Child as parameter.


# ___End of in_order_traverse method ___


# Optional Method (In case: Post-order traversal is required)
# Method for printing Post-order traversal of the Tree, this method receive Root Node of the Tree as parameter.
def post_order_traverse(root):
    if root.child is None:  # True when root node has No child nodes. (Termination Condition for Recursive Call)
        return
    else:
        in_order_traverse(root.child[0])  # Recursive Call with Left Child as parameter.
        in_order_traverse(root.child[1])  # Recursive Call with Right Child as parameter.
        print(root, end=" --> ")  # Print current node.

# ___End of post_order_traverse method ___


# Method for converting dictionary (that represent the list of children nodes of each node) into a Binary Tree of nodes.
# This method take two parameters, a starting node (root) for the tree and dictionary of nodes.
def generate_binary_tree(root, tree_nodes):
    if len(tree_nodes.get(root.label)) == 2:  # True when root node has 2 child nodes in dictionary.
        root.child = tree_nodes.get(root.label)  # get list of child nodes from dic and assign to root.child
        generate_binary_tree(root.child[0], tree_nodes)  # Recursive Call with Left Child as parameter.
        generate_binary_tree(root.child[1], tree_nodes)  # Recursive Call with Right Child as parameter.
    return root

# ___End of generateBinaryTree method ___


# This method assign codes (0,1) to each node in given dictionary
def assign_code(nodes, label, result, prefix=''):
    child_nodes = nodes[label]  # get child nodes from nodes dictionary of given label.
    codes_tree = {}
    if len(child_nodes) == 2:  # True when there are 2 child nodes

        # Recursive Call with Left node as parameter, add 0 to code for left side node.
        codes_tree['0'] = assign_code(nodes, child_nodes[0].label, result, prefix + '0')

        # Recursive Call with Right node as parameter, add 1 to code for right side node.
        codes_tree['1'] = assign_code(nodes, child_nodes[1].label, result, prefix + '1')

        # Return the dictionary with 'code as Key' and  'dict of Tree branch as Value'
        # (Will be used while Decoding)
        return codes_tree
    else:  # When node do not have 2 node
        result[label] = prefix  # Assigning Huffman code to given node.
        return label  # Return just label (Name) of the node.

# ___End of assign_code method ___


# This method takes frequency table as dictionary parameter, and perform Huffman Coding
def huffman_code(freq_values):
    frequencies = {}

    # This loop assign Node Objects at all 'k' index in frequencies.
    for k, v in freq_values.items():
        frequencies[k] = Node(k, v)

    tree_nodes = {}  # empty dictionary that will have list of child nodes of each node.

    # This loop assign the list of Child Node(s) at all 'key' index in tree_nodes.
    for key, node in frequencies.items():
        tree_nodes[key] = [node]

    # This While-loop will perform merging of nodes
    while len(frequencies) > 1:   # Loop until frequencies has more than 1 items.
        # sort frequencies dictionary in Ascending order
        sorted_freq = sorted(frequencies.items(), key=lambda x: x[1].data)

        # getting info of 1st node (will be used to create merged node)
        k1 = sorted_freq[0][1].label
        v1 = sorted_freq[0][1].data
        node1 = Node(k1, v1)

        # getting info of 2nd node (will be used to create merged node)
        k2 = sorted_freq[1][1].label
        v2 = sorted_freq[1][1].data
        node2 = Node(k2, v2)

        merged_key = k1 + k2  # label of merged node (will be the parent of 1st & 2nd node)
        merged_val = v1 + v2  # data of merged node (will be the parent of 1st & 2nd node)

        child_nodes = [node1, node2]  # 1st and 2nd node as a list of child nodes

        # creating merged node that will 1st & 2nd node as child
        temp_node = Node(merged_key, merged_val, child_nodes)

        # removing 1st & 2nd node from frequencies dictionary
        frequencies.pop(k1)
        frequencies.pop(k2)

        # adding merged node into the frequencies dictionary
        frequencies[temp_node.label] = temp_node

        # adding merged node entry into the tree_nodes dictionary
        tree_nodes[merged_key] = child_nodes

    # ___End of While-Loop___

    # last node info after merging is done
    last_label = k1 + k2
    last_val = v1 + v2
    top_node = Node(last_label, last_val)

    codes = {}  # empty dictionary that will contain Huffman Codes for each node.

    # getting codes for each nodes in tree_nodes dictionary.
    # This method call will return a dictionary with 'code as Key' and  'dict of Tree branch as Value'
    coded_tree = assign_code(tree_nodes, last_label, codes)
    # coded_tree (Will be used while Decoding)

    # generating node based Binary Tree from tree_nodes dictionary (contains list of child nodes for each node)
    # method will return root node of the generated Binary tree.
    tree_root = generate_binary_tree(top_node, tree_nodes)

    # pre-order traversal of the Binary Tree
    print("\nPre-Order Traversal of the Tree:")
    pre_order_traverse(tree_root)

    return codes, coded_tree

# ___ End of huffman_code method ___

# freq = {
#     "X": 3,
#     "Y": 1,
#     "Z": 2
# }

freq = {
    "A": 19, "B": 16, "C": 17,
    "D": 11, "E": 42, "F": 12,
    "G": 14, "H": 17, "I": 16,
    "J": 5, "K": 10, "L": 20,
    "M": 19, "N": 24, "O": 18,
    "P": 13, "Q": 1, "R": 25,
    "S": 35, "T": 25, "U": 15,
    "V": 5, "W": 21, "X": 2,
    "Y": 8, "Z": 3
}

code, tree = huffman_code(freq)

# Traversing code dictionary to display code of each node.
print("\n\nCode is:")
for k, v in code.items():
    print(k + " : " + str(v))


# This method performs encoding on a string of text and print encoded binary.
def encode(text):
    print("\nOriginal Text: ", text)

    text = text.upper()  # converting to uppercase text
    text = text.replace(" ", "")  # removing while-spaces from text
    text = ''.join(char for char in text if char.isalpha())  # removing special-characters and numbers

    print("Before Encoding: ", text)

    # getting code for each character in text and joining the codes in 'encoded' variable.
    encoded = ''.join([code[t] for t in text])
    print('Encoded Text : ', encoded)


# This method perform decoding on an already encoded string.
def decode(encoded):
    print("\nText To Decode: ", encoded)
    decoded = []
    i = 0

    while i < len(encoded):  # loop will iterate till the length of encoded string.
        ch = encoded[i]
        branch = tree[ch]
        while not isinstance(branch, str):  # loop until a str is found
            i += 1
            ch = encoded[i]
            branch = branch[ch]

        decoded.append(branch)  # append found str in the 'decoded'
        i += 1
    print('Decoded Text : ', ''.join(decoded))


# Encoding Examples as mentioned in the manual and several others.
encode("Sally sells seashells by the seashore.")
encode("Peter Piper picked a peck of pickled peppers a peck of pickled peppers Peter Piper picked.")
encode("Houston, the Eagle has landed.")
encode("I nailed this task.")
encode("Huffman Encoding is good.")

# Decoding Examples as mentioned in the manual and several others.
decode("01011001010110011111011011")
decode("10110000101010011011101101100010110010101100010111000110111")
decode("11111110001000111111101011111011001111111000100011111000001010000001110010111")
decode("10011111111100010011010111100000101000001010100101001100")
decode("01001111101011110011001100101111010111001111001101101110111")
