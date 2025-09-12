from stack import Stack

# Program Name: expression_converter.py
# Author: Alfredo Ormeno Zuniga
# Date: 09/11/2025
# Purpose:
#   This module provides a class for converting arithmetic expressions
#   between infix, prefix, and postfix notations using stack-based algorithms.
#
# Description:
#   - The ExpressionConverter class implements all required translation functions:
#       * Infix to Prefix
#       * Prefix to Infix
#       * Prefix to Postfix
#       * Postfix to Prefix
#       * Postfix to Infix
#   - The class also includes helper methods for input validation:
#       * _validate_tokens – ensures only valid characters are present.
#       * _require_operator_present – ensures each expression has at least one operator.
#       * _check_infix_operator_sequence – ensures no two operators appear consecutively.
#       * _check_parentheses – verifies balanced parentheses for infix expressions.
#   - Operator precedence and associativity are stored in a class-level dictionary
#     (_precedence) for O(1) lookup during conversion.
#
# Functions:
#   - infix_to_prefix:      Converts a valid infix expression to prefix notation.
#   - prefix_to_infix:      Converts a valid prefix expression to infix notation.
#   - prefix_to_postfix:    Converts a valid prefix expression to postfix notation.
#   - postfix_to_prefix:    Converts a valid postfix expression to prefix notation.
#   - postfix_to_infix:     Converts a valid postfix expression to infix notation.
#   - validate_expression:  Performs initial validation on any expression type.
#   - _validate_tokens, _require_operator_present, _check_infix_operator_sequence,
#     _check_parentheses:   Internal helpers to ensure input correctness before conversion.
#
class ExpressionConverter:
    # Function: infix_to_prefix
    # Purpose: Convert a given infix expression into its equivalent prefix expression.
    # Input: expr (str) - a string containing a valid infix expression with operands, 
    #          operators (+, -, *, /, ^), and parentheses.
    # Precondition: 
    #    - The input string is a syntactically correct infix expression.
    #    - Operands are single-character alphanumeric values.
    #    - Parentheses are balanced.
    # Postcondition: 
    #    - The expression is converted into prefix form.
    #    - Operator precedence and associativity are preserved to ensure correctness.
    # Output: (str) - the corresponding prefix expression
    @staticmethod
    def infix_to_prefix(expr: str) -> str:
        # Initialize empty output string and stack
        output = ""
        stack = Stack()

        # Validate Expression
        ExpressionConverter._validate_expression(expr, True)

        # Scan expression from right to left
        for char in expr[::-1]:
            if char.isspace():
                continue
            elif char.isalpha():
                output += char  # Operands go directly to output
            elif char == ")":
                stack.push(char) # Push closing parenthesis onto the stack
            elif char == "(":
                # Pop operators until closing parenthesis is found
                while not stack.isEmpty() and stack.peek() != ')':
                    output += stack.pop()
                stack.pop() # Discard the '('
            elif char in ExpressionConverter._precedence:
                # Handle operator precedence and associativity
                while not stack.isEmpty():
                    stack_precedence = ExpressionConverter._get_precedence(stack.peek())
                    char_precedence = ExpressionConverter._get_precedence(char)
                    char_associativity = ExpressionConverter._get_associativity(char)

                    # Pop higher-precedence operators, or equal-precedence if right associative
                    if stack_precedence > char_precedence:
                        output += stack.pop()
                    elif stack_precedence == char_precedence and char_associativity == "right":
                        output += stack.pop()
                    else:
                        break
                
                # Push the current operator
                stack.push(char)
    
        # End of string is reached, pop remaining operators
        while not stack.isEmpty():
            output += stack.pop()
        
        # Reverse the string to get the prefix expression and return
        return output[::-1]
    # END infix_to_prefix

    @staticmethod
    def prefix_to_postfix(expr: str) -> str:
        # Validate expression tokens and syntax
        ExpressionConverter._validate_expression(expr)

        # Initialize empty stack
        stack = Stack()

        # Scan string from left to right
        for char in expr[::-1]:
            if char.isalpha():
                stack.push(char) # Push operands directly to the stack
            elif char in ExpressionConverter._precedence:
                if stack.size() < 2:
                    raise InvalidExpressionError(
                        f"Invalid prefix expression: not enough operands for operator '{char}'"
                    )

                # Pop two operands from the stack 
                # Form new string and push string back onto the stack
                output = stack.pop() + stack.pop() + char
                stack.push(output)
        
        # Expression has been scanned
        # Stack contains single element (postfix expression)
        if stack.size() > 1:
            raise InvalidExpressionError("Invalid prefix expression: leftover tokens")
        
        return stack.pop()
    # END prefix_to_postfix

    # Function: postfix_to_prefix
    # Purpose: Convert a given postfix expression into its equivalent prefix expression.
    # Input: expr (str) - a string containing a valid postfix expression with operands 
    #          and operators (+, -, *, /, ^).
    # Precondition:
    #    - The input string is a syntactically correct postfix expression.
    #    - Operands are single-character alphabetical values.
    #    - The expression contains sufficient operands for each operator.
    # Postcondition:
    #    - The expression is converted into prefix form.
    #    - Operator precedence and associativity are preserved implicitly by the postfix structure.
    #    - If there are insufficient operands for an operator, an InvalidExpressionError is raised.
    # Output: (str) - the corresponding prefix expression
    @staticmethod
    def postfix_to_prefix(expr: str) -> str:
        # Validate expression tokens and syntax
        ExpressionConverter._validate_expression(expr)

        # Initialize empty stack
        stack = Stack()

        # Scan string from left to right
        for char in expr:
            if char.isalpha():
                stack.push(char)
            elif char in ExpressionConverter._precedence:
                if stack.size() < 2:
                    raise InvalidExpressionError(
                        f"Invalid prefix expression: not enough operands for operator '{char}'"
                    )
                
                # Pop two operands from the stack
                op2 = stack.pop()
                op1 = stack.pop()

                # Form new string (<operator><op1><op2>)
                output = char + op1 + op2
                
                # Push string to the stack
                stack.push(output)
            
        # Expression has been scanned
        # Stack should contain a single element (prefix expression)
        if stack.size() > 1:
            raise InvalidExpressionError("Invalid prefix expression: leftover tokens")
        
        return stack.pop()
    # END postfix_to_prefix

    # Function: prefix_to_infix
    # Purpose: Convert a given prefix expression into its equivalent infix expression.
    # Input: expr (str) - a string containing a valid prefix expression with operands 
    #          and operators (+, -, *, /, ^).
    # Precondition:
    #    - The input string is a syntactically correct prefix expression.
    #    - Operands are single-character alphabetical values.
    #    - The expression contains sufficient operands for each operator.
    # Postcondition:
    #    - The expression is converted into infix form.
    #    - Parentheses are inserted to preserve the intended order of operations.
    #    - If there are insufficient operands or leftover tokens, 
    #      an InvalidExpressionError is raised.
    # Output: (str) - the corresponding infix expression
    @staticmethod
    def prefix_to_infix(expr: str) -> str:
        # Validate expression tokens and syntax
        ExpressionConverter._validate_expression(expr)

        # Initialize empty stack
        stack = Stack()

        # Scan string from right to left
        for char in expr[::-1]:
            if char.isalpha():
                # Push operands directly to the stack
                stack.push(char)
            elif char in ExpressionConverter._precedence:
                # Each operator requires two operands form the stack
                if stack.size() < 2:
                    raise InvalidExpressionError(
                        f"Invalid prefix expression: not enough operands for operator '{char}'"
                    )
                op1 = stack.pop()
                op2 = stack.pop()
                # Reconstruct with parentheses to enforce evaluation order
                stack.push("("+ op1 + char + op2 + ")")
           
        
        # At this point the stack should contain exactly one valid infix expression
        result = stack.pop()
        if not stack.isEmpty():
            raise InvalidExpressionError("Invalid prefix expression: leftover operands")
        return result
    # END prefix_to_infix

    # Function: postfix_to_infix
    # Purpose: Convert a given postfix expression into its equivalent infix expression.
    # Input: expr (str) - a string containing a valid postfix expression with operands
    #          and operators (+, -, *, /, ^).
    # Precondition:
    #    - The input string is a syntactically correct postfix expression.
    #    - Operands are single-character alphabetical values.
    #    - The expression contains sufficient operands for each operator.
    # Postcondition:
    #    - The expression is converted into infix form.
    #    - Parentheses are inserted to preserve the intended order of operations.
    #    - If there are insufficient operands or leftover tokens,
    #      an InvalidExpressionError is raised.
    # Output: (str) - the corresponding infix expression
    @staticmethod
    def postfix_to_infix(expr: str) -> str:
        # Validate expression tokens and syntax
        ExpressionConverter._validate_expression(expr)

        # Initialize empty stack
        stack = Stack()

        # Scan string from left to right
        for char in expr:
            if char.isalpha():
                # Push operands directly to the stack
                stack.push(char)
            elif char in ExpressionConverter._precedence:
                # Each operator requires two operands from the stack
                if stack.size() < 2:
                    raise InvalidExpressionError(
                        f"Invalid prefix expression: not enough operands for operator '{char}'"
                    )
                op2 = stack.pop()
                op1 = stack.pop()
                # Reconstruct with parentheses to enforce evaluation order
                stack.push("("+ op1 + char + op2 + ")")
        
        # At this point the stack should contain exactly one valid infix expression
        result = stack.pop()
        if not stack.isEmpty():
            raise InvalidExpressionError("Invalid prefix expression: leftover operands")
        return result
    # END postfix_to_infix

    #--------------------Private Helper methods and variables ----------------------------#

    # This table will be used to get the precedence and the associativity of an operator. 
    # operator: (precedence, associativity)
    _precedence = {
        '^': (3, 'right'),
        '*': (2, 'left'), '/': (2, 'left'),
        '+': (1, 'left'), '-': (1, 'left')
    }

    @staticmethod
    def _get_precedence(op: str) -> int:
        # return (-1, None) if not an operator
        return ExpressionConverter._precedence.get(op, (-1, None))[0]
    
    # Associativity matters when two operators of the same precedence appear in sequence.
    # Example: a ^ b ^ c
    # - Common math rules have '^' as RIGHT-associative, this means a ^ (b ^ c),
    #   so we should NOT pop the previous '^' when we see another '^'.
    # - If operators are LEFT-associative (like +, -, *, /),
    #   we must pop the previous operator so the leftmost one is evaluated first.
    # Without checking associativity, we'd group operators incorrectly and get the wrong expression.
    @staticmethod
    def _get_associativity(op: str) -> str:
        return ExpressionConverter._precedence.get(op, (-1, None))[1]
    
    # Function: _validate_expression
    # Purpose: Validate an arithmetic expression before attempting conversion.
    # Input: expr (str) - a string containing an arithmetic expression with operands,
    #          operators (+, -, *, /, ^), and parentheses.
    # Precondition:
    #    - expr may contain whitespace.
    #    - expr may contain valid or invalid characters and may have balanced or unbalanced parentheses.
    # Postcondition:
    #    - Calls helper methods to ensure tokens are valid and parentheses are balanced.
    #    - Raises InvalidExpressionError if validation fails.
    # Output: none
    @staticmethod
    def _validate_expression(expr: str, infix: bool = False):
        ExpressionConverter._validate_tokens(expr)
        ExpressionConverter._check_parentheses(expr)
        ExpressionConverter._require_operator_present(expr)
        if infix:
            ExpressionConverter._check_infix_operator_sequence(expr)
    # END _validate_expression

    # Function: _validate_tokens
    # Purpose: Ensure that the expression contains only valid characters.
    # Input: expr (str) - the expression string to check.
    # Precondition:
    #    - expr may contain whitespace, letters, operators (+, -, *, /, ^), and parentheses.
    # Postcondition:
    #    - If expr contains any invalid characters (digits, symbols, etc.), 
    #      an InvalidExpressionError is raised.
    # Output: none
    @staticmethod
    def _validate_tokens(expr: str):
        for char in expr:
            if char.isspace():
                continue
            if char.isalpha():
                continue
            if char in ExpressionConverter._precedence:
                continue
            if char in "()":
                continue
            raise InvalidExpressionError(f"Invalid character in expression: '{char}'")
    # END _validate_tokens

    # Function: _check_parentheses
    # Purpose: Verify that all parentheses in the expression are properly balanced.
    # Input: expr (str) - the expression string to check.
    # Precondition:
    #    - expr may contain zero or more '(' and ')' characters.
    # Postcondition:
    #    - If parentheses are balanced, function completes normally.
    #    - If there are unmatched closing or opening parentheses, 
    #      an InvalidExpressionError is raised.
    # Output: none
    @staticmethod
    def _check_parentheses(expr: str):
        stack = Stack()
        for char in expr:
            if char == '(':
                stack.push(char)
            elif char == ')':
                if stack.isEmpty():
                    raise InvalidExpressionError("Unmatched closing parenthesis")
                stack.pop()
        if not stack.isEmpty():
            raise InvalidExpressionError("Unmatched opening parenthesis")
    # END _check_parentheses

    # Function: _require_operator_present
    # Purpose: Ensure that the expression contains at least one operator.
    # Input: expr (str) - the expression string to check.
    # Precondition:
    #    - Tokens have already been validated (only legal characters remain).
    # Postcondition:
    #    - Raises InvalidExpressionError if no operator is present.
    # Output: none
    @staticmethod
    def _require_operator_present(expr: str):
        for ch in expr:
            if ch in ExpressionConverter._precedence:
                return
        raise InvalidExpressionError("Expression must contain at least one operator")
    # END _require_operator_present

    # Function: _check_infix_operator_sequence
    # Purpose: Ensure that no two operators appear consecutively in an infix expression.
    # Input: expr (str) - the expression string to check.
    # Precondition:
    #    - expr is assumed to already contain only valid characters and balanced parentheses.
    # Postcondition:
    #    - If two operators are found next to each other (ignoring spaces),
    #      an InvalidExpressionError is raised.
    #    - Otherwise, function completes normally.
    # Output: none
    @staticmethod
    def _check_infix_operator_sequence(expr: str):
        prev_was_operator = False
        for char in expr:
            if char.isspace():
                continue
            if char in ExpressionConverter._precedence:  # current char is an operator
                if prev_was_operator:
                    raise InvalidExpressionError(
                        f"Invalid operator sequence: two operators in a row near '{char}'"
                    )
                prev_was_operator = True
            elif char.isalpha() or char in "()":
                prev_was_operator = False
    #END _check_infix_operator_sequence
# END ExpressionConverter
 
################ Custom Exception Classes ############################################

# Custom exception class for handling expression input errors
class InvalidExpressionError(Exception):
    """Invalid expression."""
    pass
