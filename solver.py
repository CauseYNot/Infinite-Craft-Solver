
from binary_tree_display import BinaryTreeNode
import json

with open('./nodes.json') as nodes_file, open('./id.json') as id_file:
    nodes = json.load(nodes_file)
    label_to_id = json.load(id_file)

def solver(target):
    root = BinaryTreeNode(target)
    # Simple depth-first search - depth-first will produce a thinner tree, 
    # but will be easier to read, going from left to right (or top to bottom 
    # if the tree is rotated).
    paths_to_go = [root]
    logged = ['Water', 'Fire', 'Earth', 'Wind']
    while paths_to_go:
        node = paths_to_go.pop()
        # We log every node we pass - if we have already found the recipe 
        # for a node, there's no need to search further
        if node.key in logged:
            continue
        
        logged.append(node.key)
        # Get two ingredients from dictionary
        node_dict = nodes[label_to_id['ids'][node.key]]
        ingredient_one = node_dict['ingredient_one']
        ingredient_two = node_dict['ingredient_two']
        # Set them to the left and right of the node
        node.left = BinaryTreeNode(key=ingredient_one)
        node.right = BinaryTreeNode(key=ingredient_two)
        # Set them to be visited later
        paths_to_go.append(node.right)
        paths_to_go.append(node.left)
        
    return root
