import regex as re
from .function import Function

class FunctionSolver:
    def __init__(self):
        self.obj = None
        self.obj_name = None
        self.data = None
        self.function = Function()

    def solve(self, function_calling):

        result  = self.call_function(function_calling)

        return str(result)

    def set_data(self, data):
        self.data = data


    @staticmethod
    def get_obj_name(function_calling):
        function_calling = function_calling.replace(' ', '')

        pattern = r'^\$\w+'

        name = re.search(pattern, function_calling)

        return name[0]

    def get_obj(self, name):


        return self.data[name]


    def call_function(self, function_calling):
        row_function_calling = function_calling
        processed_function_calling = self.process_function_calling(function_calling)
        single_object_pattern = r'((\$\w+)((?:\.\w+(\(((?:[^()])|(?4))*\)))|(?:(?:\[\W?\w+\W?\])+))*)'

        single_boject_list = re.findall(single_object_pattern,processed_function_calling)
        value = processed_function_calling

        for s_obj in single_boject_list:
            self.function.set_data(self.get_obj(s_obj[1]))
            single_function = re.sub(r'^'+re.escape(s_obj[1]),'',s_obj[0])


            pattern =r'(\.\w+(\((?:(?:[^()])|(?2))*\)))|((?:\[[\w\"]+\])+)'
            matches = re.findall(pattern,single_function)
            for match in matches:
                if match[0] != '':

                    eval(f"self.function{match[0]}")

                if match[2]!= '':

                    eval(f" self.function.update_data(self.function.data{match[2]})")

            value = re.sub(re.escape(s_obj[0])+r'(?=\s|\b|$)',str(self.function.data),value)


        return value


    def process_function_calling(self,function_calling):
            # change .name into ["name"]
            pattern =r'(?:(?<!:)(?:\.([^\W\d][\w]*))\b(?!\())'
            function_calling = re.sub(pattern,lambda match: f'["{match.group(1)}"]',function_calling)

            pattern =r'(\.\w+(\((?:(?:[^()])|(?2))*\)))'

            matches = re.findall(pattern,function_calling)
            value = ''

            for match in matches:
                value = match[0]

                value1= '("'+match[1][1:-1]+'")'
                value = value.replace(match[1],value1)

                function_calling = re.sub(re.escape(match[0]),value,function_calling)

            return function_calling









