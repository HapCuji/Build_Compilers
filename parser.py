from parse_tree import ParseTree
from parse_tree import print_tree # just check

'''
    Чтобы не уходить в бесконечную рекурсию (совмещены оба варианта):
        1 - ограничение на кол-во входов (MAX_DEPTH_RECURSION = 10)
            + сейчас делаю общюю для всех функций, но по идее для каждой дб свой
        2 - проверять если уже открыт экземпляр функции, то ждать пока он кончится
            - далее если не получается разобрать выражение, то увеличить возможную рекурсию на 1 
            - и повторить разбор, и так до максимальной грубины ( MAX_DEPTH_RECURSION = 10)
    Делема верной обработки простого выражения :
        - смотри _expression()
'''
MAX_DEPTH_RECURSION = 10

class Parser:

    def __init__(self, string):
        self.string = string.replace(" ", "")
        self.identifiers = list(chr(i) for i in range(65, 91)) #  + list(chr(i) for i in range(97, 123))
        self.index = 0
        self.tree = None
        
        # self.choosed_type = {"_just_expr": 1,  "_term": 1, "_factor": 1}    # если не получается первым переходм к следующему
        self.depth_recursion = {"_just_expr": 0,  "_term": 0, "_factor": 0} 
        self.current_max_depth = 0 # {"_just_expr": 0,  "_term": 0, "_factor": 0}  # 

    def get_tree(self):
        return self.tree

    def accept_string(self):
        tree = self._expression()
        if tree is not None and self._string_is_end():
            self.tree = tree
            return True
        else:
            # try set more depth and repeat detail
            while (self.current_max_depth < MAX_DEPTH_RECURSION):
                self.current_max_depth += 1
                # set default
                self.depth_recursion = {"_just_expr": 0,  "_term": 0, "_factor": 0}
                self.index = 0
                tree = self._expression()
                if tree is not None and self._string_is_end():
                    self.tree = tree
                    return True     # catch success
            #  for self.current_max_depth["_just_expr"] in range(1, MAX_DEPTH_RECURSION):
            #     for self.current_max_depth["_term"] in range(1, MAX_DEPTH_RECURSION):
            #         for self.current_max_depth["_factor"] in range(1, MAX_DEPTH_RECURSION):
            #             #  пытаемся найти решене для всех возможных комбинаций
            #             self.depth_recursion = {"_just_expr": 0,  "_term": 0, "_factor": 0}
            #             self.index = 0
            #             tree = self._expression()
            #             if tree is not None and self._string_is_end():
            #                 self.tree = tree
            #                 return True     # catch success
      
        return False                # any attempts was lost

    def _expression(self):
        tree = ParseTree("Expr ")

        expr_node = self._just_expr()
        if expr_node is not None:
            tree.add_child(expr_node)
            # print (':iteration\n', '='*35)
            # print_tree(tree)
            expr_node = self._relationship_op()
            if expr_node is not None:
                tree.add_child(expr_node)
                tree.value = "Expr_type_2"
                # expr_node = self._just_expr()
                
                self.current_max_depth = 0
                start_index = self.index
                # чтобы правильно разобрать правую часть 
                # 1 вариант - следует сбросить глубину рекурсии (реализовано)
                # 2 вариант - разрешить частично разбирать выражение (не пробовал)
                # (конкретно, 174 строка - терм 2го типа! не завершен,
                #  но имеет право на существование т.к. имеет наибольшую длину индекса разбора)
                while (self.current_max_depth < MAX_DEPTH_RECURSION):
                    self.current_max_depth += 1
                    # set default
                    self.depth_recursion = {"_just_expr": 0,  "_term": 0, "_factor": 0}
                    self.index = start_index

                    expr_node = self._just_expr()
                    if expr_node is not None and self._string_is_end():
                        break

                # print ("expr_node=",  '='*35)
                # print_tree(expr_node)

                if expr_node is not None:
                    tree.add_child(expr_node)
                else:
                    return None         # error 2 type element 3
            else:
                tree.value = "Expr_1_type "

            return tree
        else:  
            return None

    def _just_expr(self):
        name_func = "_just_expr"
        end_index1 = end_index2 = end_index3 = -1
        start_index = self.index
        if self._recurs_control_begin(name_func):
            # print ("_just_expr none was!")
            return None

        just_node = self._term()
        if just_node is not None :
            tree1 = ParseTree("Just_expr_1_type")
            tree1.add_child(just_node)
            end_index1 = self.index         # ok 1 type
        
        self.index = start_index
        just_node_2 = self._sign()
        if just_node_2 is not None :
            tree2 = ParseTree("Just_expr_2_type")
            tree2.add_child(just_node_2)
            just_node_2 = self._term()
            if just_node_2 is not None:
                tree2.add_child(just_node_2)
                end_index2 = self.index         # ok 2 type
            else:
                tree2 = None         # error 2 type (element 2)``
        
        self.index = start_index
        just_node_3 = self._just_expr()
        if just_node_3 is not None: #  and self.choosed_type[name_func] == 3 -> This is definitely and so (must be)
            tree3 = ParseTree("Just_expr_3_type")
            tree3.add_child(just_node_3)
            just_node_3 = self._add_op()
            if just_node_3 is not None:
                tree3.add_child(just_node_3)
                just_node_3 = self._term()
                if just_node_3 is not None:
                    tree3.add_child(just_node_3)
                    end_index3 = self.index         # ok 3 type
                else:
                    tree3 = None # error 3 type (element 3)
            else:
                tree3 = None     # error 3 type (element 2)``
        
        self._recurs_control_end(name_func)
        # choosed tree with more index!
        max_end_index = max(end_index1, end_index2, end_index3, start_index)
        self.index  = max_end_index
        if (max_end_index is not start_index and max_end_index > -1):
            if max_end_index == end_index1:
                return tree1
            elif max_end_index == end_index2:
                return tree2
            elif max_end_index == end_index3:
                return tree3
        
        return None             # any other case <- if max_end_index - start_index <= 0:

    def _term(self):
        name_func = "_term"
        end_index1 = end_index2 = -1
        start_index = self.index
        if self._recurs_control_begin(name_func):
            # print ("_term none was!")
            return None

        term_node = self._factor()
        if term_node :
            tree1 = ParseTree("term_1_type")
            tree1.add_child(term_node)
            end_index1 = self.index         # ok 1 type

        self.index = start_index
        term_node = self._term()
        if term_node is not None :  # and self.choosed_type[name_func] == 2 -> This is definitely and so (must be)
            tree2 = ParseTree("term_2_type")
            tree2.add_child(term_node)
            term_node = self._mul_op()
            if term_node is not None:
                tree2.add_child(term_node)
                term_node = self._factor()
                if term_node is not None:
                    tree2.add_child(term_node)
                    end_index2 = self.index         # ok 2 type
                else:
                    tree2 = None     # error term 2 type (in element 3)
            else:
                tree2 = None         # error term 2 type (in element 2)

        self._recurs_control_end(name_func)
        # choosed tree with more index!
        max_end_index = max(end_index1, end_index2, start_index)
        self.index = max_end_index
        if (max_end_index is not start_index and max_end_index > -1):
            if max_end_index == end_index1:
                return tree1
            elif max_end_index == end_index2:
                return tree2
      
        return None

    def _factor(self):
        name_func = "_factor"
        start_index = self.index
        end_index1 = end_index2 = end_index3 = end_index4 = -1
        if self._recurs_control_begin(name_func):
            # print ("_factor none was!")
            return None

        factor_node = self._identifier()    
        if factor_node is not None :
            tree1 = ParseTree("Factor_type_1")
            tree1.add_child(factor_node)
            end_index1 = self.index             # ok 1 type
        
        self.index = start_index
        factor_node = self._const()
        if factor_node is not None :
            tree2 = ParseTree("Factor_type_2")
            tree2.add_child(factor_node)
            end_index2 = self.index             # ok 2 type
            
                                                # check "(""just expr"")"
        self.index = start_index
        tree3 = ParseTree("Factor_type_3")
        if self._check_sequence(tree3, "("):     #  and self.choosed_type[name_func] == 3 -> This is definitely and so (must be)
            factor_node = self._just_expr()
            if factor_node is not None:
                tree3.add_child(factor_node)
                if self._check_sequence(tree3, ")"): # self.string[self.index] == ")":
                    end_index3 = self.index         # ok 3 type
                else:
                    tree3 = None                # error factor 3 type (in ")")
            else:
                tree3 = None                    # error factor 3 type (in just expr)
       
        self.index = start_index
        tree4 = ParseTree("Factor_type_4")
        if self._check_sequence(tree4, "not"):   # and self.choosed_type[name_func] == 1 -> This is definitely and so (must be)
            factor_node = self._factor()
            if factor_node is not None:
                tree4.add_child(factor_node)
                end_index4 = self.index         # ok 4 type
            else:
                tree4 = None                    # error factor 4 type (in 2 element)
        else:
            tree4 = None                        # not 4 type

        self._recurs_control_end(name_func)
        max_end_index = max(end_index1, end_index2, end_index3, end_index4, start_index)
        self.index = max_end_index
        if (max_end_index is not start_index and max_end_index > -1):
            if max_end_index == end_index1:
                return tree1
            elif max_end_index == end_index2:
                return tree2
            elif max_end_index == end_index3:
                return tree3
            elif max_end_index == end_index4:
                return tree4
            
        return None                             # nothing result type

    def _sign(self):
        tree = ParseTree("Sign")

        if self._check_sequence(tree, "+"): # ппроверить изменяетсся ли дерево (по идее да, т.к. это указатель)
            return tree
        elif self._check_sequence(tree, "-"):
            return tree
        
        return None

    def _add_op(self):
        tree = ParseTree("Add_type_op")

        if self._check_sequence(tree, "+"): # ппроверить изменяетсся ли дерево (по идее да, т.к. это указатель)
            return tree
        elif self._check_sequence(tree, "-"):
            return tree

        return None

    def _mul_op(self):
        tree = ParseTree("Mul_type_op")

        if self._check_sequence(tree, "*"): # ппроверить изменяетсся ли дерево (по идее да, т.к. это указатель)
            return tree
        elif self._check_sequence(tree, "/"):
            return tree
        elif self._check_sequence(tree, "div"):
            return tree
        elif self._check_sequence(tree, "mod"):
            return tree
        elif self._check_sequence(tree, "and"):
            return tree

        return None

    def _relationship_op(self):
        tree = ParseTree("Relationship_type_op")

        if self._check_sequence(tree, "="): # ппроверить изменяетсся ли дерево (по идее да, т.к. это указатель)
            return tree
        elif self._check_sequence(tree, "<>"):
            return tree
        elif self._check_sequence(tree, "<"):
            return tree
        elif self._check_sequence(tree, "<="):
            return tree
        elif self._check_sequence(tree, ">"):
            return tree
        elif self._check_sequence(tree, ">="):
            return tree

        return None

    def _check_sequence(self, tree, compare_string):
        increment_index = len(compare_string)
        if self.string[self.index: self.index + increment_index] == compare_string:
            # print ("sequence", self.string[self.index: self.index + increment_index], " on index=", self.index)
            self.index += increment_index
            tree.add_child(ParseTree(compare_string))
            return tree
        else:
            return None

    
    def _const(self):

        tree = ParseTree("Const")
        count_sim = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        count = 0
        while True:
            if self._out_of_range():
                break
            if self.string[self.index] in count_sim:
                self.index += 1
                count += 1
            else:
                break

        if count:
            tree.add_child(ParseTree(self.string[self.index-count: self.index]))
            return tree

        return None

    def _identifier(self):

        tree = ParseTree("Id")
        count = 0
        while True:
            if self._out_of_range():
                break
            if self.string[self.index] in self.identifiers:
                # print (self.string[self.index], " on index=", self.index)
                self.index += 1
                count += 1
            else:
                break

        if count:
            tree.add_child(ParseTree(self.string[self.index-count: self.index]))
            return tree

        return None

    def _recurs_control_begin(self, num_func):
        self.depth_recursion[num_func] += 1 
        if self.depth_recursion[num_func] > self.current_max_depth: # self.current_max_depth[num_func]: # 
            # print (self.depth_recursion, self.current_max_depth)
            self.depth_recursion[num_func] -= 1
            return True             # <- go back. 
        return False                # continius go insert ->

    def _recurs_control_end(self, num_func):
        self.depth_recursion[num_func] -= 1

    def _out_of_range(self):
        return self.index > (len(self.string) - 1)

    def _string_is_end(self):
        return self.index == len(self.string)

    def __repr__(self):
        return f"{self.index}"
