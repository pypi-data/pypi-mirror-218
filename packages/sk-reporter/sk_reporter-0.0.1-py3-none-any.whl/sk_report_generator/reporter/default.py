from .base import IReporter
import regex as re


class Default(IReporter):
    def __init__(self):
        self.successor = None
        self.data = None

    def report(self, template):
        pattern = r'\{(\{((?:[^{}]|(?1))*)\})\}'
        template = re.sub(pattern, lambda match: match[2], template)

        return template

    def set_successor(self, successor):
        self.successor = successor

    def set_data(self, data):
        self.data = data
