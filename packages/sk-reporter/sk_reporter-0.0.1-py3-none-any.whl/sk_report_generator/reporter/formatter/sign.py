import regex as re
from ..base import IFormatHandler


class SignHandler(IFormatHandler):

    def __init__(self):
        self.successor = None

    def handle(self, value, condition, format_specs, format_pattern):
        if 'sign' in format_specs:
            format_pattern = re.sub(r'\{sign\}', str(format_specs['sign']), format_pattern)
            del format_specs['sign']
        else:
            format_pattern = re.sub(r'\{sign\}', '', format_pattern)

        return self.successor.handle(value, condition, format_specs, format_pattern)

    def set_successor(self, successor):
        self.successor = successor
