from ..base import IFormatter


class Ceil(IFormatter):
    def __init__(self):
        self.successor = None
        self.value = None

    def format(self, value, condition, format_sepec):
        if 'ceil-precision' in format_sepec:
            if condition is None:
                precision = float(format_sepec['ceil-precision'])
                value = float(value)
                mod = value % precision

                if mod == 0:
                    value = str(value)
                else:
                    value = str(value + precision - mod)

        return self.successor.format(value, condition, format_sepec)

    def set_successor(self, successor):
        self.successor = successor
