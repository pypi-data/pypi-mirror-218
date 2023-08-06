import clang
from .colortext import *
support = ["PARM_DECL"]

class NodeVisitor:
    def __init__(self):
        self.script = ""
        
    def TRANSLATION_UNIT(self, node):
        self.scriptname = node.spelling

        for child in node.get_children():
            self.visit_node(child)
            
    def FUNCTION_DECL(self, node):
        self.script += "function " + node.spelling + "("
        for child in node.get_children():
            if child.kind.name == "PARM_DECL":
                self.script += child.spelling + ", "
        self.script = self.script[:-2] + ")\n"
        
        for child in node.get_children():
            if child.kind.name == "COMPOUND_STMT":
                self.visit_node(child)
            
    def RETURN_STMT(self, node):
        self.script += "return "
        
        for child in node.get_children():
            if child.kind.name == "UNEXPOSED_EXPR":
                self.visit_node(child)
            elif child.kind.name == "INTEGER_LITERAL":
                self.script += child.spelling
            elif child.kind.name == "BINARY_OPERATOR":
                self.script += child.spelling
        self.script += "\n"
    
    def BINARY_OPERATOR(self, node):
        self.script += node.spelling
        
        for child in node.get_children():
            if child.kind.name == "INTEGER_LITERAL":
                self.script += child.spelling
            elif child.kind.name == "UNEXPOSED_EXPR":
                self.visit_node(child)
                
            
    # Node visitor:
    def visit_node(self, node):
        """Visit a node"""
        # Get the function name
        name = node.kind.name
        if name in self.__dir__():
            self[name](node) 
        elif name not in support:
            print(red("Unsupported node type: {}".format(name)))
        
