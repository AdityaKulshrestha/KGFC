from collections import defaultdict
import glob
from typing import List
import os
import tree_sitter_python as tspython
from src.kgfc.tree_sitter import Language, Parser, Treesitter



class CodeTree():
    def __init__(self):
        PY_LANGUAGE = Language(tspython.language())
        # self.parser = Parser(PY_LANGUAGE)
        treesitter_parser = Treesitter.create_treesitter(PY_LANGUAGE)


    def parse_code_files(self, codebase_path: str):
        class_data = []
        method_data = []

        all_class_names = set()
        all_method_names = set()

        file_list = self._traverse_codebase(codebase_path)

        for file_path in file_list:
            subdir = os.path.dirname(file_path).replace(codebase_path, "")  # Extracing the subdirectories
            file_name = os.path.basename(file_path)  # File name part
            
            with open(file_path, "r", encoding="utf-8") as file:
                code = file.read()
                file_bytes = code.encode()
                class_nodes, method_nodes = self.parser.parse(file_bytes)

                for class_node in class_nodes:
                    class_name = class_node.name
                    all_class_names.add(class_name)

                    class_data.append({
                        "file_name": file_name,
                        "subdir": subdir,
                        "constructor_declarations": "",
                        "method_declarations": "\n----\n".join(class_node.method_declarations) if class_node.method_declarations else "",
                        "source_code": class_node.source_code,
                        "reference": []     # Additional Metadata
                    })

                for method_node in method_nodes:
                    method_name = method_name.name
                    all_method_names.add(method_name)
                    method_data.append({
                        "file_path": file_path, 
                        "subdir": subdir,
                        "class_name": method_node.class_name if method_node.class_name else "",
                        "name": method_name,
                        "doc_comment": method_node.doc_comment,
                        "source_code": method_node.method_source_code,
                        "references": []    # Additional Metadata
                    })

        return class_data, method_data, all_class_names, all_method_names

    
    def _traverse_codebase(self, codebase_path: str) -> List[str]:
        
        codebase_root_name = codebase_path.split('/')[-1]
        codebase_files = glob.glob(os.path.join(codebase_path, '**', '*.py'), recursive=True)
        return codebase_files
    

# Testing
if __name__ == "__main__":
    codetree = CodeTree()
    classes_data, method_data, all_classes, all_methods = codetree.parse_code_files('/root/kubernetes_files/Mooshak')
    print(classes_data)
