#!python

from binarytree_expression import BinaryTreeExpression, BinaryTreeNode
import unittest


class BinaryTreeNodeTest(unittest.TestCase):

    def test_init(self):
        data = 123
        node = BinaryTreeNode(data)
        assert node.data is data
        assert node.left is None
        assert node.right is None

    def test_is_leaf(self):
        # Create node with no children
        node = BinaryTreeNode(2)
        assert node.is_leaf() is True
        # Attach left child node
        node.left = BinaryTreeNode(1)
        assert node.is_leaf() is False
        # Attach right child node
        node.right = BinaryTreeNode(3)
        assert node.is_leaf() is False
        # Detach left child node
        node.left = None
        assert node.is_leaf() is False
        # Detach right child node
        node.right = None
        assert node.is_leaf() is True
