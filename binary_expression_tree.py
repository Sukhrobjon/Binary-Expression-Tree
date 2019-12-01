#!python
import queue


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
    def __init__(self, expression=None):
        """
        Initialize the tree with user expression(math expression)
        
        Args:
            expression(str): string representation of math expression
        """
        self.root = None
        self.size = 0

        if expression is not None:
            for exp in expression:
                self.insert(exp)

    def __repr__(self):
        """Return a string representation of this binary search tree."""
        return 'BinarySearchTree({} nodes)'.format(self.size)

    def is_empty(self):
        """Return True if this binary search tree is empty (has no nodes)."""
        return self.root is None

    def insert(self, expression=None):
        """
        Insert the postfix expression into the tree using stack
        """

        # if max size is 0, then it is infinite
        stack = queue.LifoQueue(maxsize=0)



