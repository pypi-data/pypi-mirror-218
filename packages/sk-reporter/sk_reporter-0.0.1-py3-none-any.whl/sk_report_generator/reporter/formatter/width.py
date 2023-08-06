import regex as re
from ..base import IFormatHandler


class WidthHandler(IFormatHandler):

    def __init__(self):
        self.successor = None

    def handle(self, value, condition, format_specs, format_pattern):
        if 'width' in format_specs:
            format_pattern = re.sub(r'\{width\}', str(format_specs['width']), format_pattern)
            del format_specs['width']
        else:
            format_pattern = re.sub(r'\{width\}', '', format_pattern)

        return self.successor.handle(value, condition, format_specs, format_pattern)

    def set_successor(self, successor):
        self.successor = successor
