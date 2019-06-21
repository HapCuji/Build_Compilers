from parse_tree import print_tree
from parser import Parser
import sys

if __name__ == "__main__":
    # sys.setrecursionlimit(11000) 
    # WRITE ONLY BIG IDENTIFER because i can't distinguish between operator and name of variable
    # string = "not(A+B)*1 = not B mod (2 and D)"
    string = "( A mod B ) and C <> not A"
    print("Input:\n", string)
    print ("="*35)
    p = Parser(string)
    
    if p.accept_string():
        print(p.get_tree())
        print_tree(p.get_tree())
        print ("="*35)
    else:
        print("parse error")
