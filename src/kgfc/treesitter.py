# Reference: https://github.com/sankalp1999/code_qa/blob/main/treesitter.py
from abc import ABC
from tree_sitter import Language, Parser
from enum import Enum
from tree_sitter_languages import get_language, get_parser
from tree_sitter import Language, Parser
import tree_sitter_python as tspython
from typing import Optional
import logging 

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class LanguageEnum(Enum):
    JAVA = "java"
    PYTHON = "python" 
    RUST = "rust"
    JAVASCRIPT = "javascript"
    UNKWOWN = "unknown"


LANGUAGE_QUERIES = {
    LanguageEnum.PYTHON: {
        'class_query': """
            (class_definition
                name: (identifier) @class.name)
        """,
        'method_query': """
            (function_definition
                name: (identifier) @function.name)
        """,
        'doc_query': """
            (expression_statement
                (string) @comment)
        """
    }
}

LANGUAGEOBJ = {
    'python': Language(tspython.language())
}


class TreesitterMethodNode:
    def __init__(
            self,
            name: str,
            doc_comment: str,
            method_source_code: str,
            node, 
            class_name: str = None
    ):
        self.name = name
        self.doc_comment = doc_comment 
        self.method_source_code = method_source_code
        self.node = node 
        self.class_name = class_name

class TreesitterClassNode:
    def __init__(
            self,
            name: str,
            method_declarations: list,
            node,
    ):
        self.name = name
        self.source_code = node.text.decode()
        self.method_declarations = method_declarations
        self.node = node

class Treesitter(ABC):
    def __init__(self):
        self.language_obj = Language(tspython.language())
        self.parser = Parser(self.language_obj)
        self.query_config = LANGUAGE_QUERIES[LanguageEnum.PYTHON]
        if not self.query_config:
            raise ValueError(f"Unsupported languag")
        
        # Corrected query instantiation
        self.class_query = self.language_obj.query(self.query_config['class_query'])
        self.method_query = self.language_obj.query(self.query_config['method_query'])
        self.doc_query = self.language_obj.query(self.query_config['doc_query'])
        
    @staticmethod
    def create_treesitter():
        """Allows to initiate for different languages."""
        return Treesitter()
    
    def parse(self, file_bytes: bytes) -> tuple[list[TreesitterClassNode], list[TreesitterMethodNode]]:
        tree = self.parser.parse(file_bytes)
        root_node = tree.root_node

        class_results = []
        method_results = []

        class_name_by_node = {}
        class_captures = self.class_query.captures(root_node)
        breakpoint()
        class_nodes = []
        for node, capture_name in class_captures:
            if capture_name == node.text.decode():
                class_name = node.text.decode()
                class_node = node.parent
                logging.info(f"Found class: {class_name}")
                class_name_by_node[class_node.id] = class_name 
                method_declarations = self._extract_methods_in_class(class_node)
                class_results.append(TreesitterClassNode(class_name, method_declarations, class_node))
                class_nodes.append(class_node)

        method_captures = self.method_query.captures(root_node)
        for node, capture_name in method_captures:
            if capture_name in ['method.name', 'function.name']:
                method_name = node.text.decode()
                method_node = node.parent 
                method_source_code = method_node.text.decode()
                doc_comment = self._extract_doc_comment(method_node)
                parent_class_name = None
                for class_node in class_node:
                    if self._is_descendant_of(method_node, class_nodes):
                        parent_class_name = class_name_by_node[class_node.id]
                        break

                method_results.append(TreesitterMethodNode(
                    name=method_name,
                    doc_comment=doc_comment,
                    method_source_code=method_source_code,
                    node=method_node,
                    class_name=parent_class_name
                ))

    def _extract_methods_in_class(self, class_nodes):
        method_declarations = []
        # Apply method query to the class_node
        method_captures = self.method_query.captures(class_nodes)
        for node, capture_name in method_captures:
            if capture_name in ['method.name', 'function.name']:
                method_declarations = node.parent.text.decode()
                method_declarations.append(method_declarations)
            
        return method_declarations
    
    def _extract_doc_comment(self, node):
        # Search for the doc comments prededing the node
        doc_comment = ""
        current_node = node.prev_sibling
        while current_node:
            captures = self.doc_query.captures(current_node)
            if captures:
                for cap_node, cap_name in captures:
                    if cap_name == "comment":
                        doc_comment = cap_node.text.decode() + '\n' + doc_comment
            elif current_node.type not in ['comment', 'block_comment', 'line_comment', 'expression_statement']:
                # Stop if we reach a node that's not a comment
                break
            current_node = current_node.prev_sibling
        return doc_comment.strip()
            
    def _is_descendant_of(self, node, ancestor):
        # Check if 'node' is a descendant of 'ancestor'
        current = node.parent
        while current:
            if current == ancestor:
                return True
            current = current.parent
        return False