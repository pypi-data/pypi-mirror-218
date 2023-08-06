import regex as re
from ..base import IFormatHandler


class FillHandler(IFormatHandler):

    def __init__(self):
        self.successor = None

    def handle(self, value, condition, format_specs, format_pattern):
        if 'fill' in format_specs:
            format_pattern = re.sub(r'\{fill\}', str(format_specs['fill']), format_pattern)
            del format_specs['fill']
        else:
            format_pattern = re.sub(r'\{fill\}', '', format_pattern)

        return self.successor.handle(value, condition, format_specs, format_pattern)

    def set_successor(self, successor):
        self.successor = successor
