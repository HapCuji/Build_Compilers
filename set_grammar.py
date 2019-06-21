MARKER = '$'

precedence = {op: p for p, ops in enumerate(reversed([
    {'not'},                            # '+\'', '-\'' sign too?
    {'*', '/', 'mod', 'and', 'div'},    # mul op
    {'+', '-', 'or'},
    {'<', '<=', '=', '<>', '>', '>='},
])) for op in ops}
# print (precedence)
prefix = {'not'} #  '+\'', '-\'' sign too?

variables = {'C', 'a', 'b', 'c'} # { chr(i) for i in range(65, 91) } | { chr(i) for i in range(97, 123)}
# print (variables)
constants = {'1'} # , '2', '3', '4', '5', '6', '7', '8', '9', '0'

all_tokens = frozenset(set(precedence) | variables | constants | {'(', ')', MARKER})
