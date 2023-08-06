# Latinisation API

The APU to latinise non latin strings. For now, it only supports Armenian, but it will soon expand to other langugages too.

## Instructions

1. Install:

```bash
pip install latinisation
```

2. Latinise Armenian text:

```python
from latinisation import armenian

armenian.armenian_latinisation(some_input)
```

## Example of a program that uses the latinisation API:

```python
from latinisation import armenian

# Ask the user to input a sting of Armenian letters
some_input = input("Input some Armenian letters: ")

# Convert the user inputed sting to a string of latin letters using the API
armenian.armenian_latinisation(some_input)

# Print out the latinised version of the inputed string 
print(some_input)
```