from json import load, dump, loads

class ParseTree:
    def __init__(self, value):
        self.value = value
        self.childs = []

    def add_child(self, child):
        self.childs.append(child)

    def __str__(self, filename='myprint.json'):
        elementar_filds = ["Mul_type_op", "Relationship_type_op",  "Const", "Id", "Add_type_op", "Sign", "Factor_type_3", "Factor_type_4"]
        
        def tree_decoder(tree: ParseTree):
            data_json = {}
            data_json[tree.value] = []
            if tree.childs:
                for child in tree.childs:
                    new_dict = tree_decoder(child)
                    data_json[tree.value].append(new_dict)
            else:
                data_json = tree.value # just value

            return data_json

        with open(filename, 'w') as outfile:  
            data_json = tree_decoder(self)
            print (data_json)
            dump(data_json, outfile, ensure_ascii=False, indent=2, separators=(', ', ': ') )    # do not sor key!

        return ("="*35)

def print_tree(tree: ParseTree, indent=0):
    indent_str = "    " * indent + " "
    if tree.childs:
        print(indent_str + f"{tree.value}")
        for child in tree.childs:
            print_tree(child, indent + 1)
    else:
        print(indent_str + f"'{tree.value}'")