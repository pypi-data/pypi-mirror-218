import regex as re
from ..base import IFormatHandler


class TypeHandler(IFormatHandler):

    def __init__(self):
        self.successor = None

    def handle(self, value, condition, format_specs, format_pattern):
        if 'type' in format_specs:
            format_pattern = re.sub(r'\{type\}', str(format_specs['type']), format_pattern)
            del format_specs['type']
        else:
            format_pattern = re.sub(r'\{type\}', '', format_pattern)

        return self.successor.handle(value, condition, format_specs, format_pattern)

    def set_successor(self, successor):
        self.successor = successor
