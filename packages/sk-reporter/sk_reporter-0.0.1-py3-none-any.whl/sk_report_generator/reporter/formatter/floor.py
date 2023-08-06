from ..base import IFormatter

class Floor(IFormatter):
    def __init__(self):
        self.value = None



    def format(self,value,condition,format_sepec):
        if 'floor-precision' in format_sepec:
            if condition == None:
                precision = float(format_sepec['floor-precision'])
                value = float(value)
                mod = value%precision

                if mod ==0:
                    value = str(value)
                else:
                    value = str(value-mod)




        return self.successor.format(value,condition,format_sepec)

    def set_successor(self,successor):
        self.successor= successor