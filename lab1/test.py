from expression_converter import ExpressionConverter
from expression_converter import InvalidExpressionError

if __name__ == "__main__":
    infix_to_prefix = [
        "a+b*c",          # simple precedence
        "(a+b)*c",        # parentheses
        "a^b^c",          # right-assoc exponent
        "a+b*(c^d-e)^(f+g*h)-i",  # complex
        "a+b-d+12",
        "a+-b"
    ]

    prefix_to_postfix_tests = [
        "*+AB-CD",
        "*+A",
        "^a^bc",
        "+a*bc",
        "-+a*b^-^cde+f*ghi"   
    ]

    postfix_to_prefix_tests = [
        "AB+C*",       # should become *+ABC
        "AB+CD-*",     # should become *+AB-CD
        "abc^^",       # right-associative exponent → ^a^bc
        "abc*+",       # should become +a*bc
        "abcd^e-fgh*+^*+i-",  # long complex one
        "AB+",         # simple addition → +AB
        "AB",          # invalid (no operator)
        "A+B"          # invalid (operators in wrong place for postfix)
    ]

    prefix_to_infix_tests = [
        "*+abc",                     # should become ((a+b)*c)
        "^a^bc",                     # right-assoc exponent → (a^(b^c))
        "+a*bc",                     # (a+(b*c))
        "-+a*b^-^cde+f*ghi",         # complex → ((a+(b*(((c^d)-e)^(f+(g*h)))))-i)

        "*+A",                       # invalid: not enough operands for '+'
        "+a",                        # invalid: not enough operands for '+'
        "*+ab",                      # invalid: leftover operator at end
        "+A1",                       # invalid: digits not allowed by validator
    ]

    postfix_to_infix_tests = [
        "AB+",             # should become (A+B)
        "AB*C+",           # should become ((A*B)+C)
        "ABC*+",           # should become (A+(B*C))
        "abc^^",           # should become (a^(b^c))
        "abcd^e-fgh*+^*+i-",  # long complex one

        "A+",              # invalid: not enough operands
        "AB",              # invalid: no operator
        "A1B+",            # invalid: digits not allowed
        "AB+C*+",          # invalid: leftover operators
    ]

    for exp in infix_to_prefix:
        print(f"Infix: {exp}")
        try:
            print(f"Prefix: {ExpressionConverter.infix_to_prefix(exp)}\n")
        except InvalidExpressionError as e:
            print(f"Error: {e}\n")
    
    for exp in prefix_to_postfix_tests:
        print(f"Prefix: {exp}")
        try:
            print(f"Postfix: {ExpressionConverter.prefix_to_postfix(exp)}\n")
        except InvalidExpressionError as e:
            print(f"Error: {e}\n")
    
    for exp in postfix_to_prefix_tests:
        print(f"Postfix: {exp}")
        try:
            print(f"Prefix: {ExpressionConverter.postfix_to_prefix(exp)}\n")
        except InvalidExpressionError as e:
            print(f"Error: {e}\n")

    for exp in prefix_to_infix_tests:
        print(f"Prefix: {exp}")
        try:
            print(f"Infix:  {ExpressionConverter.prefix_to_infix(exp)}\n")
        except InvalidExpressionError as e:
            print(f"Error:  {e}\n")
    
    for exp in postfix_to_infix_tests:
        print(f"Postfix: {exp}")
        try:
            print(f"Infix:   {ExpressionConverter.postfix_to_infix(exp)}\n")
        except InvalidExpressionError as e:
            print(f"Error:   {e}\n")