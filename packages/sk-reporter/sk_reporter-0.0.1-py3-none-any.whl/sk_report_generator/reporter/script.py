import regex as re
import io
import sys
from .base import IReporter


class ScriptEvaluator(IReporter):
    def __init__(self):
        self.successor = None
        self.data = None

    def report(self, template):
        pattern = r'(\<\>([\s\S]*?)\<\/\>)'
        matches = re.findall(pattern, template)
        scripts = self.process(matches)

        results = self.run_scripts(scripts)

        template = self.update_template(template, results)


        return self.successor.report(template)

    def process(self,scripts):

        temp = []
        for template_script,row_script in scripts:
            value  = self.successor.report(row_script)
            pattern = r'(<<(.*?)>>)'
            matches = re.findall(pattern,value)
            for match in matches:
                code = self.process_code(match[1])
                printf = "print(f'"+code+"')"
                value = re.sub(re.escape(match[0]),printf,value)

            temp.append((template_script,value))

        scripts = temp

        return scripts


    def run_scripts(self,scripts):
        temp = []
        for template_script,row_script in scripts:

            code_string = row_script
            output_stream = io.StringIO()
            sys.stdout = output_stream
            exec(code_string)
            sys.stdout = sys.__stdout__
            captured_output = output_stream.getvalue().strip()

            temp.append((template_script,captured_output))
        scripts = temp
        return scripts

    def update_template(self, template, script_results):

        for scripts,results in script_results:

            template = re.sub(re.escape(scripts,results),results,template)

        return template
    def process_code(self,code):
        format_pattern = '{[^{}]+}'
        matches = re.findall(format_pattern,code)
        for match in matches:

            pattern =r'(?:(?<!:)(?:\.([^\W\d][\w]*))\b(?!\())'
            format_value = re.sub(pattern,lambda match: f'["{match.group(1)}"]',match)
            code = re.sub(re.escape(match),format_value,code)
        return code

    def set_successor(self, successor):
        self.successor = successor

    def set_data(self, data):
        self.data = data
