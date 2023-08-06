import regex as re
from ..base import IFormatHandler


class PrecisionHandler(IFormatHandler):

    def __init__(self):
        self.successor = None

    def handle(self, value, condition, format_specs, format_pattern):
        if 'precision' in format_specs:
            format_pattern = re.sub(r'\{precision\}', str(format_specs['precision']), format_pattern)
            del format_specs['precision']
        else:
            format_pattern = re.sub(r'\{precision\}', '', format_pattern)

        return self.successor.handle(value, condition, format_specs, format_pattern)

    def set_successor(self, successor):
        self.successor = successor
