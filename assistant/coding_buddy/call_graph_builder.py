import ast
from collections import defaultdict

class CallGraphBuilder:
    def __init__(self, file_contents: dict[str, str]):
        self.file_contents = file_contents
        self.call_graph = defaultdict(lambda: defaultdict(list))

    def build(self) -> dict:
        formatted_graph = {}
        for file_name, content in self.file_contents.items():
            try:
                tree = ast.parse(content)
                visitor = _QualifiedCallVisitor(content)
                visitor.visit(tree)
                for func, calls in visitor.calls.items():
                    if file_name not in formatted_graph:
                        formatted_graph[file_name] = {}
                    formatted_graph[file_name][func] = sorted(calls)
            except SyntaxError:
                continue  # skip files with syntax errors
        return formatted_graph


class _QualifiedCallVisitor(ast.NodeVisitor):
    def __init__(self, content: str):
        self.content = content
        self.current_class = None
        self.current_function = None
        self.calls = defaultdict(set)
        self.classes_in_file = set()

    def visit_ClassDef(self, node):
        """Visit each class definition and add to the set of classes"""
        self.classes_in_file.add(node.name)
        self.current_class = node.name  # Set the current class when inside a class
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        prev_function = self.current_function
        func_name = node.name
        if self.current_class:
            func_name = f"{self.current_class}.{func_name}"
        self.current_function = func_name
        self.generic_visit(node)
        self.current_function = prev_function

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_Call(self, node):
        if self.current_function:
            qualified_name = self._resolve_name(node.func)
            if qualified_name:
                first_letter = qualified_name[0]
                if first_letter.upper() == first_letter:
                    qualified_name = f"{qualified_name}.__init__"
                if qualified_name == "__init__" and self.current_class:
                    # Prepend the current class name to __init__
                    qualified_name = f"{self.current_class}.__init__"
                self.calls[self.current_function].add(qualified_name)
        self.generic_visit(node)

    def _resolve_name(self, node):
        """Resolve names like Assistant.greeting or print"""
        if isinstance(node, ast.Attribute):
            value = self._resolve_name(node.value)
            if value:
                return f"{value}.{node.attr}"
            return node.attr
        elif isinstance(node, ast.Name):
            return node.id
        return None