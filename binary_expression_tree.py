#!python
import queue
lower_string = "abcdefghijklmnopqrstuvwxyz"


class BinaryTreeNode(object):
    def __init__(self, data):
        """
        Initialize the tree with user expression(math expression)
        
        Args:
            expression(str): string representation of math expression
        """
        self.data = data
        self.right = None
        self.left = None

    def __repr__(self):
        """Return a string representation of this parse tree node."""
        return 'ParseTreeNode({!r})'.format(self.data)

    def is_leaf(self):
        """Return True if this node is a leaf (that is operands)."""
        return self.left is None and self.right is None


class BinaryExpressionTree(object):
    def __init__(self, expression):
        """
        Initialize the tree with user expression(math expression)
        
        Args:
            expression(str): string representation of math expression
        """
        self.root = None
        self.size = 0

        # if expression is not None:
        self.insert(expression)

    def __repr__(self):
        """Return a string representation of this binary search tree."""
        return 'BinarySearchTree({} nodes)'.format(self.size)

    def is_empty(self):
        """Return True if this binary search tree is empty (has no nodes)."""
        return self.root is None

    def insert(self, expression):
        """
        Insert the postfix expression into the tree using stack
        """

        # if max size is 0, then it is infinite
        stack = queue.LifoQueue(maxsize=1000)
        char = expression[0]
        node = BinaryTreeNode(char)
        stack.put(node)
        i = 1
        while not stack.empty():
            char = expression[i]
            # if char is operand
            if char in lower_string:
                # create a node and push the node into the stack
                node = BinaryTreeNode(char)
                stack.put(node)
            else:
                # create a parent(operator) node for operands
                operator = BinaryTreeNode(char)
                # pop the last pushed item and create right_child
                right_child = stack.get()
                # pop item one before the last item and create left_child
                left_child = stack.get()
                # assign those as a child of the operand
                operator.right = right_child
                operator.left = left_child
                # push back the operand node to the stack
                stack.put(operator)
                

                # check if we reach last element in the expression
                # so we can define the root of the tree
                if stack.qsize() == 1 and i == len(expression) - 1:
                    self.root = stack.get()
                    print(f"root: {self.root}")
                    print(f"right: {self.root.right}, left: {self.root.left}")
                    

            # increment i
            i += 1
            self.size += 1
        print(f"i is {i} in insert ")
    
    def items_in_order(self):
        """Return an in-order list of all items in this binary search tree."""
        items = []
        if not self.is_empty():
            # Traverse tree in-order from root, appending each node's item
            # item.append is uncalled function
            self._traverse_in_order_recursive(self.root, items.append)

            # self._traverse_in_order_iterative(self.root, items.append)
        # Return in-order list of all items in tree
        return items

    def _traverse_in_order_recursive(self, node, visit):
        """
        Traverse this binary tree with recursive in-order traversal (DFS).
        Start at the given node and visit each node with the given function.
        Running time: O(n) we are visiting each node
        Memory usage: O(n) when node is visited we are adding new item to list
        """

        if(node):
            # Traverse left subtree, if it exists
            self._traverse_in_order_recursive(node.left, visit)
            # Visit this node's data with given function
            visit(node.data)
            # Traverse right subtree, if it exists
            self._traverse_in_order_recursive(node.right, visit)


if __name__ == "__main__":

    user_input = "ab*c/ef/g*+k+xy*-"
    tree_obj = BinaryExpressionTree(expression=user_input)

    print(tree_obj)
    print(tree_obj.items_in_order())
    
