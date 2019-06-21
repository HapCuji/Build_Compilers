from relation import make_relations, print_relations
from parse import parse
from set_grammar import all_tokens, variables, constants, precedence, prefix


if __name__ == "__main__":
    relations = make_relations(all_tokens, variables, constants, prefix, precedence)
    
    string = "( a mod b ) and c * C <> not a" # manual
    # tokens = input('Input separate by 'space' (in end - '$'): \n').strip().split()
    tokens = string.strip().split()
    
    print ("Relations: \n")
    print_relations(relations)
    print ("All possible tokens: \n", all_tokens)
    print ("Current tokens: \n", tokens)
    
    print(parse(tokens, all_tokens, relations))
