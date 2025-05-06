class FileCollector:
    def __init__(self) -> None:
        self.call_graph: CallGraph | None = None
        self.tracer: DependencyTracer | None = None

    def get_needed_files(self, graph_data: dict, entry_points: list[str]) -> set[str]:
        self.call_graph = CallGraph(graph_data)
        self.tracer = DependencyTracer(self.call_graph)
        files = self.tracer.trace_from(entry_points)
        return files


class CallGraph:
    def __init__(self, graph_data: dict):
        self.graph = graph_data
        self.func_to_file = self._build_reverse_index()

    def _build_reverse_index(self):
        mapping = {}
        for file, functions in self.graph.items():
            for func in functions:
                mapping[func] = file
        return mapping

    def get_callees(self, func_name: str):
        file = self.func_to_file.get(func_name)
        if not file:
            return []
        return self.graph[file].get(func_name, [])

    def get_file(self, func_name: str):
        return self.func_to_file.get(func_name)


class DependencyTracer:
    def __init__(self, call_graph: CallGraph):
        self.call_graph = call_graph
        self.visited = set()
        self.required_files = set()

    def trace_from(self, entry_points: list[str]) -> set[str]:
        for entry in entry_points:
            self._visit(entry)
        return self.required_files

    def _visit(self, func_name: str):
        if func_name in self.visited:
            return
        self.visited.add(func_name)

        file = self.call_graph.get_file(func_name)
        if file:
            self.required_files.add(file)

        for callee in self.call_graph.get_callees(func_name):
            self._visit(callee)
