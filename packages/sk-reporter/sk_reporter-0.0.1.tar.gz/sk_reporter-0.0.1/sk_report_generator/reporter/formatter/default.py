from ..base import IFormatter
import regex as re


class Default(IFormatter):
    def __init__(self):
        self.value = None

    def format(self, value, condition, format_sepec, format_pattern=''):
        return value

    def handle(self, value, condition, format_sepec, format_pattern):
        format_pattern = re.sub(r'\{value\}', str(value), format_pattern)

        return eval(f"f'{format_pattern}'"), format_sepec

    def set_successor(self, successor):
        pass
