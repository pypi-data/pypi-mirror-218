import regex as re
from .function_solver.function_solver import FunctionSolver
from .base import IReporter


class FunctionEvaluator(IReporter):
    def __init__(self):
        self.successor = None
        self.data = None
        self.function_solver = FunctionSolver()

    def report(self, template):

        pattern = r'(\{\{(?:((?:[^{}]|(?1))*?))(?:(?:\:[^{}\[\]]+)|((?:\:\:)(.*)))?\}\})'

        matches = re.findall(pattern, template)

        changed_value = ''

        for match in matches:
            changed_value = match[0]
            result = self.function_solver.solve(match[1])
            changed_value = re.sub(re.escape(match[1]), result, changed_value)
            template = re.sub(re.escape(match[0]),changed_value,template)

        return self.successor.report(template)

    def set_successor(self, successor):
        self.successor = successor

    def set_data(self, data):
        self.data = data
        self.function_solver.set_data(self.data)
