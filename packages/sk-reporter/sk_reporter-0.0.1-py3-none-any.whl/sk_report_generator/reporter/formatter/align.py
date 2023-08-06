import regex as re
from ..base import IFormatHandler


class AlignHandler(IFormatHandler):
    def __init__(self):
        self.successor = None

    def handle(self, value, condition, format_specs, format_pattern):
        if 'align' in format_specs:
            align = format_specs['align']
            if align == 'left':
                align = '<'
            if align == 'right':
                align = '>'
            if align == 'center':
                align = '^'
            format_pattern = re.sub(r'\{align\}', align, format_pattern)
            del format_specs['align']
        else:
            format_pattern = re.sub(r'\{align\}', '', format_pattern)

        return self.successor.handle(value, condition, format_specs, format_pattern)

    def set_successor(self, successor):
        self.successor = successor
