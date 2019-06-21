def make_relations(tokens, variables, constants, prefix, precedence):
    right_associative = {' '}

    relations = {t: {t: None for t in tokens} for t in tokens}

    relations['('][')'] = '='

    relations['$']['('] = relations['(']['('] = '<' # Last Lpare will be in process First
    relations[')']['$'] = relations[')'][')'] = '>' # First Rpare will be in process First

    for thing in variables | constants:
        relations['$'][thing] = relations['('][thing] = '<' # Inside pare will be in process First
        relations[thing]['$'] = relations[thing][')'] = '>'

    for op in precedence:
        relations[op]['$'] = '>'
        relations['$'][op] = '<'

        relations[op]['('] = relations['('][op] = '<'       # Inside pare will be in process First
        relations[op][')'] = relations[')'][op] = '>'

        for thing in variables | constants:
            relations[op][thing] = '<'                      # Var will process First
            relations[thing][op] = '>'

        if op in prefix:
            for op2 in precedence:
                relations[op2][op] = '<'                # any prefix will high process then others in precedence
                if precedence[op] > precedence[op2]:     
                    relations[op][op2] = '>'
                else:
                    relations[op][op2] = '<'            # but we will wait process if we catch prefix rather then precedent with high level
        else:
            for op2 in precedence:
                if precedence[op] < precedence[op2] or precedence[op] == precedence[op2] and op in right_associative and op2 in right_associative:
                    relations[op][op2] = '<'
                    continue
                if precedence[op] > precedence[op2] or precedence[op] == precedence[op2] and op not in right_associative and op2 not in right_associative:
                    relations[op][op2] = '>'
                    continue

    return relations

def print_relations(relations):
    indent = '     '
    row = indent
    for key in relations.keys():
        column = "  " + str(key)
        while (len(column) < len(indent)):
            column += ' '
        column += ' ' 
        row += column
    print (row)

    for key, value in relations.items():
        indent = '    |'
        row = "  " + str(key)
        while (len(row) < len(indent)):
            row += ' '
        row += '|'
        for precedent in value.values():
            if precedent is None:
                column = " err"
            else:
                column = "  " + str(precedent)
            while (len(column) < len(indent)):
                column += ' '
            column += '|' 
            row += column
        print (row)
    

            