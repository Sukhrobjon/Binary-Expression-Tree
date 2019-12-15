#!python
import sys
import queue
from collections import deque
lower_string = "abcdefghijklmnopqrstuvwxyz"


class BinaryTreeNode(object):
    def __init__(self, data):
        """
        Initialize the tree with user expression(algebraic expression)
    
        Args:
            data(str): string representation of math expression
        """
        self.data = data
        self.right = None
        self.left = None
        # flag for operators to distinguish from operands
        self.operator = False
    

    def __repr__(self) -> str:
        """Return a string representation of this parse tree node."""
        return 'ParseTreeNode({!r})'.format(self.data)

    def is_leaf(self) -> bool:
        """Return True if this node is a leaf(that is operand)."""
        return self.left is None and self.right is None


class BinaryExpressionTree(object):
    def __init__(self, expression: str = None):
        """
        Initialize the tree with user expression(math expression)
        
        Args:
            expression(str): string representation of algebraic expression
        """
        self.root = None
        self.size = 0

        if expression is not None:
            self.insert(expression)

    def __repr__(self) -> str:
        """Return a string representation of this binary search tree."""
        return 'BinarySearchTree({} nodes)'.format(self.size)

    def is_empty(self) -> bool:
        """Return True if this binary search tree is empty (has no nodes)."""
        return self.root is None

    def insert(self, expression: str):
        """
        Insert the postfix expression into the tree using stack
        """
        postfix_exp = self.infix_to_postfix(expression)
        print(f"postfix: {postfix_exp}")
        # if max size is 0, then it is infinite
        stack = deque()
        char = postfix_exp[0]
        # create a node for the first element of the expression
        node = BinaryTreeNode(char)
        # push it to stack
        stack.appendleft(node)

        # iterator for expression
        i = 1
        while len(stack) != 0:
            char = postfix_exp[i]
            # if char is float or int
            if '.' in char or char.isdigit():
                # create a node and push the node into the stack
                node = BinaryTreeNode(char)
                stack.appendleft(node)
            else:
                # create a parent(operator) node for operands
                operator_node = BinaryTreeNode(char)
                operator_node.operator = True
                # pop the last pushed item and create right_child
                right_child = stack.popleft()
                # pop item one before the last item and create left_child
                left_child = stack.popleft()
                # assign those as a child of the (parent)operator
                operator_node.right = right_child
                operator_node.left = left_child
                # push back the operator node(subtree) to the stack
                stack.appendleft(operator_node)

                # check if we reach last element in the expression
                # so we can define the root of the tree
                if len(stack) == 1 and i == len(postfix_exp) - 1:
                    self.root = stack.popleft()
                    print(f"root: {self.root}")
                    print(f"right: {self.root.right}, left: {self.root.left}")
                    

            # increment i
            i += 1
            self.size += 1
        print(f"i is {i} in insert ")
    
    def items_in_order(self) -> list:
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

    def evaluate(self, node=None) -> float:
        """
        Calculate this tree expression recursively

        Args:
            node(BinaryTreeNode): starts at the root node
        """
        # initialize
        
        if node is None:
            node = self.root
        
        # empty tree
        if node is None:
            return 0

        # check if we are at the leaf, it means it is a operand
        if node.is_leaf():
            node.value = float(node.data)
            val = float(node.data)
            
            return val
        
        left_value = self.evaluate(node.left)
        right_value = self.evaluate(node.right)

        # addition
        if node.data == "+":
            
            return left_value + right_value
        # subtraction
        elif node.data == "-":
        
            print(f"node value: {node.value}")
            return left_value - right_value
        # division
        elif node.data == "/":
            return left_value / right_value
        # multiplication
        elif node.data == "*":
            return left_value * right_value
        # power
        else:
            return left_value ** right_value

    def infix_to_postfix(self, infix_input: list) -> list:
        """
        Converts infix expression to postfix.

        Args:
            infix_input(list): infix expression user entered
        """

        # precedence order and associativity helps to determine which
        # expression is needs to be calculated first
        precedence_order = {'+': 0, '-': 0, '*': 1, '/': 1, '^': 2}
        associativity = {'+': "LR", '-': "LR", '*': "LR", '/': "LR", '^': "RL"}
        # clean the infix expression
        clean_infix = self._clean_input(infix_input)
        
        i = 0
        postfix = []
        operators = "+-/*^"
        stack = deque()
        while i < len(clean_infix):
            
            char = clean_infix[i]
            # print(f"char: {char}")
            # check if char is operator
            if char in operators:
                # check if the stack is empty or the top element is '('
                if len(stack) == 0 or stack[0] == '(':
                    # just push the operator into stack
                    stack.appendleft(char)
                    i += 1
                # otherwise compare the curr char with top of the element
                else:
                    # peek the top element
                    top_element = stack[0]
                    # check for precedence
                    # if they have equal precedence
                    if precedence_order[char] == precedence_order[top_element]:
                        # check for associativity
                        if associativity[char] == "LR":
                            # pop the top of the stack and add to the postfix
                            popped_element = stack.popleft()
                            postfix.append(popped_element)
                        # if associativity of char is Right to left
                        elif associativity[char] == "RL":
                            # push the new operator to the stack
                            stack.appendleft(char)
                            i += 1
                    elif precedence_order[char] > precedence_order[top_element]:
                        # push the char into stack
                        stack.appendleft(char)
                        i += 1
                    elif precedence_order[char] < precedence_order[top_element]:
                        # pop the top element
                        popped_element = stack.popleft()
                        postfix.append(popped_element)
            elif char == '(':
                # add it to the stack
                stack.appendleft(char)
                i += 1
            elif char == ')':
                top_element = stack[0]
                while top_element != '(':
                    popped_element = stack.popleft()
                    postfix.append(popped_element)
                    # update the top element
                    top_element = stack[0]
                # now we pop opening parenthases and discard it
                stack.popleft()
                i += 1
            # char is operand
            else:
                postfix.append(char)
                i += 1
            #     print(postfix)
            # print(f"stack: {stack}")
        
        # empty the stack
        if len(stack) > 0:
            for i in range(len(stack)):
                postfix.append(stack.popleft())
        # while len(stack) > 0:
        #     postfix.append(stack.popleft())

        return postfix
        
    def _clean_input(self, infix_exp: str) -> list:
        """
        Clean and determine if the input expression user provided can be
        calculated.

        Args:
            infix_exp(str): raw infix expression from user
        
        Return:
            clean_format(list): cleaned expression in a list form. Using list
            helps to support more than 1 digit numbers in the tree.
        """
        operators = "+-*/^()"
        # remove all whitespaces
        clean_exp = "".join(infix_exp.split())
        print(f"clean_exp: {clean_exp}")
        clean_format = []
        i = 0

        while i < len(clean_exp):
            char = clean_exp[i]
            print(f"char: {char}")
            if char in operators:
                clean_format.append(char)
                i += 1
            else:
                num = ""
                # if we see num, extract the full number not just 1 digit
                while char not in operators:
                    char = clean_exp[i]
                    num += char
                    i += 1
                # just the number part
                clean_format.append(num[:-1])
                # operator
                clean_format.append(num[-1])
        return clean_format


if __name__ == "__main__":
    # user_input = "((2+5)+(7-3))*((9-1)/(4-2))"
    # expr = "(((10+2.2) + (5.4))^2)   "
    # user_input = "8-2*3"
    
    # ignore the script and grab the user expression
    # user_input = sys.argv[1:]
    tree_obj = BinaryExpressionTree(user_input)
    
    print(f"Tree: {tree_obj}")
    print(tree_obj.items_in_order())
    print(tree_obj.evaluate())
    
    
    #===============Test postfix conversion====================#
    # infix = "((2+5)+(7-3))*((9-1)/(4-2))"
    # # expected = "kl+mn*-op^w*u/v/t*+q+"
    # postfix = infix_to_postfix(expr)
    # print(f"postfix: {postfix}")

    # dirty = "((10^2) + (300/20))   "
    # clean = _clean_input(dirty)
    # print(f"dirty: {dirty}, clean: {clean}")
