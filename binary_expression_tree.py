#!python
import queue
from collections import deque
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
        # flag for operators to distinguish from operands
        self.operator = False
        self.value = None

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
        print(f"inserting expression: {expression}")
        # if max size is 0, then it is infinite
        stack = queue.LifoQueue(maxsize=0)
        char = expression[0]
        # create a node for the first element of the expression
        node = BinaryTreeNode(char)
        # push it to stack
        stack.put(node)

        # iterator for expression
        i = 1
        while not stack.empty():
            char = expression[i]
            # if char is operand
            if char in lower_string or char.isdigit():
                # create a node and push the node into the stack
                node = BinaryTreeNode(char)
                stack.put(node)
            else:
                # create a parent(operator) node for operands
                operator_node = BinaryTreeNode(char)
                operator_node.operator = True
                # pop the last pushed item and create right_child
                right_child = stack.get()
                # pop item one before the last item and create left_child
                left_child = stack.get()
                # assign those as a child of the operand
                operator_node.right = right_child
                operator_node.left = left_child
                # push back the operand node to the stack
                stack.put(operator_node)
                

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

    def _calculate(self, node=None) -> float:
        """
        Calculate this tree expression recursively

        Args:
            node(BinaryTreeNode):  
        """
        # initialize
        
        if node is None:
            node = self.root
        
        # empty tree
        if node is None:
            return 0

        # check if we are at the leaf, it means it is a operand
        if node.is_leaf():
            node.value = int(node.data)
            return int(node.data)
        
        left_sum = self._calculate(node.left)
        right_sum = self._calculate(node.right)

        # addition
        if node.data == "+":
            # TODO: ask Alan if is there any meaning to have .value attribute
            node.value = left_sum + right_sum
            return left_sum + right_sum
        # subtraction
        elif node.data == "-":
            return left_sum - right_sum
        # division
        elif node.data == "/":
            return left_sum / right_sum
        # multiplication
        elif node.data == "*":
            return left_sum * right_sum
        # power
        else:
            return left_sum ** right_sum

    def calculate(self):
        return self._calculate(node=None)

def infix_to_postfix(infix_input: list) -> list:
    """
    Converts infix expression to postfix.

    Args:
        infix_input(list): infix expression user entered
    """
    precedence_order = {'+': 0, '-': 0, '*': 1, '/': 1, '^': 2}
    associativity = {'+': "LR", '-': "LR", '*': "LR", '/': "LR", '^': "RL"}
    
    i = 0
    postfix = []
    operators = "+-/*^"
    stack = deque()
    while i < len(infix_input):
        
        char = infix_input[i]
        print(f"char: {char}")
        # check if char is operator
        if char in operators:
            # check if the stack is empty
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
            print(postfix)
        print(f"stack: {stack}")
    if len(stack) > 0:
        for i in range(len(stack)):
            postfix.append(stack.popleft())

    return postfix
    
def _clean_input(infix_exp: str) -> list:
    """
    Clean and determine if the input expression user provided can be
    calculated.

    Args:
        infix_exp(str): raw infix expression from user
    
    Return:
        clean_exp(list): cleaned expression in a list form. Using list
        helps to support more than 1 digit numbers in the tree.
    """
    operators = "+-*/^()"
    # remove all whitespaces
    clean_exp = "".join(infix_exp.split())
    clean = []
    i = 0

    while i < len(clean_exp):
        char = clean_exp[i]
        if char in operators:
            clean.append(char)
            i += 1
            # i += 1
        else:
            num = ""
            while char not in operators:
                char = clean_exp[i]
                num += char
                i += 1
            # just the number part
            clean.append(num[:-1])
            # operator
            clean.append(num[-1])
    return clean

if __name__ == "__main__":

    user_input = "ab*c/ef/g*+k+xy*-"

    user_input = "52/3+79+-"
    expr = ['10', '2', '^', '300', '20', '/', '+']
    tree_obj = BinaryExpressionTree(expr)
    # tree_obj.infix_to_postfix(expr)
    print(tree_obj)
    print(tree_obj.items_in_order())
    print(tree_obj.calculate())
    # for i in range(tree_obj.size):
    #===============Test postfix conversion====================#
    # infix = "((2+5)+(7-3))*((9-1)/(4-2))"
    # # expected = "kl+mn*-op^w*u/v/t*+q+"
    # postfix = infix_to_postfix(expr)
    # print(f"postfix: {postfix}")

    # dirty = "((10^2) + (300/25))   "
    # clean = _clean_input(dirty)
    # print(f"dirty: {dirty}, clean: {clean}")
