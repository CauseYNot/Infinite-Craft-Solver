
class BinaryTreeNode:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        # ID is for graphviz
        self._id = None

    def to_dot(self, dot_filepath, rankdir="BT"):
        # The 'lines' to write to the file - one section for nodes and one for edges
        nodes_lines = f'\t"{self.key}" [label={self.key}, fontname="Roboto", shape="rectangle", style="rounded", root=true]\n'
        edges_lines = ''
        # Simple breadth-first search - there basically is no difference 
        # between depth-first and breadth-first, I think the latter is just 
        # easier to understand.
        to_visit = [self]
        self._id = self.key
        # We don't want any ID repeats
        used_ids = [self._id]
        while to_visit:
            node = to_visit.pop()
            left = node.left
            right = node.right
            if left:
                # Adding underscores to the left node's key until it is unique from any other
                left_id = left.key
                while left_id in used_ids:
                    left_id += '_'
                
                left._id = left_id
                used_ids.append(left._id)
                # Add to nodes_lines and edges_lines to write to file
                nodes_lines += f'\t"{left._id}" [label="{left.key}", fontname="Roboto", shape="rectangle", style="rounded"]\n'
                edges_lines += f'\t"{node._id}" -> "{left._id}" [dir="back"]\n'
                # Visit this node later
                to_visit.insert(0, left)
                
            if right:
                # Same here, add underscores until unique
                right_id = right.key
                while right_id in used_ids:
                    right_id += '_'
                
                right._id = right_id
                used_ids.append(right._id)
                # Add to write
                nodes_lines += f'\t"{right._id}" [label="{right.key}", fontname="Roboto", shape="rectangle", style="rounded"]\n'
                edges_lines += f'\t"{node._id}" -> "{right._id}" [dir="back"]\n'
                # Visit later
                to_visit.insert(0, right)
        
        # Write lines to file
        with open(dot_filepath, 'w') as writefile:
            writefile.write('digraph tree {\n')
            writefile.write(f'\trankdir={rankdir}\n')
            writefile.write(nodes_lines)
            writefile.write('\n')
            writefile.write(edges_lines)
            writefile.write('}')
