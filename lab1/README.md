# Expression Converter

## Overview
This program converts **arithmetic expressions** between different notations:  

- **Infix → Prefix**  
- **Prefix → Infix & Postfix**  
- **Postfix → Infix & Prefix**  

The program validates each input expression for correctness (valid tokens, balanced parentheses, at least one operator). If an expression is invalid, an error message is printed instead of a conversion result. Spaces are ignored so "A   +   B" is still considered a valid expression.  

All conversions assume **binary operators only** (`+`, `-`, `*`, `/`, `^`) and **single-letter operands** (`a`, `b`, `c`, …).  

This program was written using python 3.11

---

## Input Format
The program reads expressions from a plain text file, one expression per line.  
Expressions are grouped into categories using headings:  

- `[INFIX]`  
- `[PREFIX]`  
- `[POSTFIX]`  

### Example `input.txt`:
[INFIX]

a+b*c

(a+b)*c

a^b^c

[PREFIX]

*+abc

^a^bc

[POSTFIX]

ab+c*

abc^^


---

## Output Format
The program writes results to a specified output file. Each category is echoed with results for each expression, separated by blank lines.  

### Example `output.txt`:
[INFIX]

Infix: a+bc
Prefix: +abc

Infix: (a+b)*c
Prefix: *+abc

Infix: a^b^c
Prefix: ^a^bc

[PREFIX]

Prefix: *+abc

Infix: ((a+b)c)

Postfix: ab+c

Prefix: ^a^bc

Infix: (a^(b^c))

Postfix: abc^^

[POSTFIX]

Postfix: ab+c*

Infix: ((a+b)*c)

Prefix: *+abc

Postfix: abc^^

Infix: (a^(b^c))

Prefix: ^a^bc


---

## How to Run

From the command line, if input file is in same directory as main.py, run:

```bash
python main.py input.txt output.txt
```

* input.txt → required, path to your input file.

* output.txt → optional, name of the output file (default: output.txt).

* If no output file is specified, results are written to output.txt by default.