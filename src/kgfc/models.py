from enum import Enum
from typing import Any, List, Optional
from pydantic import BaseModel


# Replace it in the treesitter
class TreesitterMethodNode(BaseModel):
    name: str
    doc_comment: str
    method_source_code: str
    node: Any
    class_name: Optional[str]


class TreesitterClassNode(BaseModel):
    name: str
    source_code: str
    method_declarations: List[str]
    node: Any


class LanguageEnum(Enum):
    JAVA = "java"
    PYTHON = "python"
    RUST = "rust"
    JAVASCRIPT = "javascript"
    UNKWOWN = "unknown"


class FileClass(BaseModel):
    name: str
    path: str
    classes: List[TreesitterClassNode]
    methods: List[TreesitterMethodNode]