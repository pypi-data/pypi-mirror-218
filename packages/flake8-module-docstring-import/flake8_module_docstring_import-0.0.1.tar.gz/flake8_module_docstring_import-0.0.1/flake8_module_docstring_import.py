import ast
from typing import Any, Generator, List, Tuple, Type
import importlib.metadata

MSG = 'MDL001 There have to be a one new line between module docstring and imports'


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.problems: List[Tuple[int, int]] = []

    def visit_Module(self, node: ast.Call) -> None:
        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and (
                isinstance(node.body[1], ast.Import)
                or isinstance(node.body[1], ast.ImportFrom)
            )
            and node.body[1].lineno - node.body[0].end_lineno != 2
        ):
            self.problems.append(
                (node.body[0].lineno, node.body[0].col_offset)
            )
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib.metadata.version(__name__)

    def __init__(self, tree: ast.AST) -> None:
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)
        for line, col in visitor.problems:
            yield line, col, MSG, type(self)
