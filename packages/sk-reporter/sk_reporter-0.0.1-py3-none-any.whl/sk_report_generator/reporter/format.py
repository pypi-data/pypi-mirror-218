from .base import IReporter
from .formatter.floor import Floor
from .formatter.ceil import Ceil
from .formatter.width import WidthHandler
from .formatter.align import AlignHandler
from .formatter.fill import FillHandler
from .formatter.grouping_option import GroupingOptionHandler
from .formatter.pad import PadHandler
from .formatter.precision import PrecisionHandler
from .formatter.sign import SignHandler
from .formatter.type import TypeHandler
from .formatter.default import Default
import regex as re


class Formatter(IReporter):
    def __init__(self):
        self.successor = None
        self.floor = Floor()
        self.ceil = Ceil()
        self.default = Default()
        self.width_handler = WidthHandler()
        self.align = AlignHandler()
        self.fill = FillHandler()
        self.grouping_option = GroupingOptionHandler()
        self.pad = PadHandler()
        self.precision = PrecisionHandler()
        self.sign = SignHandler()
        self.type = TypeHandler()

    def report(self, template):

        format_pattern = r'(?![}])(\{(\{((?:[^{}]|(?2))*)\:([^{}]*)\})\})(?![}])'
        template = self.process_template(template)
        template, format_class_list = self.get_format_list(template)
        matches = re.findall(format_pattern, template)

        for match in matches:
            value = match[2]
            format_spec = match[3]

            if re.sub(r'[\s\-\.]', '', value).isdigit():
                value = int(value) if value.endswith('.0') or '.' not in value else float(value)

            try:
                replacement = format(value, format_spec)
            except ValueError:


                condition, format_specs = self.process(format_spec, format_class_list)
                format_pattern = '{{value}:{fill}{align}{sign}{pad}{width}{grouping_option}{precision}{type}}'

                default_format_value, format_specs = self.width_handler.handle(value, condition, format_specs,format_pattern)

                result = self.floor.format(default_format_value, condition, format_specs)

                replacement = result

            pattern = r'({)\s*' + re.escape(match[1]) + r'\s*(})'
            template = re.sub(pattern, replacement, template)

        return self.successor.report(template)

    def set_successor(self, successor):
        self.successor = successor
        self.floor.set_successor(self.ceil)
        self.ceil.set_successor(self.default)

        self.width_handler.set_successor(self.align)
        self.align.set_successor(self.fill)
        self.fill.set_successor(self.grouping_option)
        self.grouping_option.set_successor(self.pad)
        self.pad.set_successor(self.precision)
        self.precision.set_successor(self.sign)
        self.sign.set_successor(self.type)
        self.type.set_successor(self.default)

    def set_data(self, data):
        pass

    def process(self, format_spec, format_class_list):

        matches = re.split(',', format_spec)
        condition = re.search(r'c(\(((?>[^()]+|(?1))*)\))', format_spec)

        format_spec_list = matches
        format_specs = {}
        if condition:
            condition = condition[2]
            format_spec_list = matches[1:]
        for key in format_spec_list:
            format_specs.update(format_class_list[key])

        return condition, format_specs

    def get_format_list(self, template):

        format_classes = {}

        format_tags = re.findall(r'<format>([\s\S]*?)<\/format>', template)
        for tag in format_tags:
            format_class_matches = re.findall(r'((\w+)\s*=\s*({(?:[^{}]|(?3))*}))', tag)
            for format_class in format_class_matches:
                key = format_class[1]
                value = format_class[2]
                format_classes[key] = eval(value)
        template = re.sub(r'\n?<format>([\s\S]*?)<\/format>','',template)
        return template,format_classes

    def process_template(self,template):

        pattern = r'(\{\{(?:((?:[^{}]|(?1))*?))(?:((?:\:\:)(.*)))\}\})'
        matches = re.findall(pattern,template)
        i = 0
        form = ''
        for match in matches:
            value1 =match[0]
            value2 = match[3]
            value3 = match[2]
            form = form+f"\nc{i} = {value2}"

            replacement = re.sub(re.escape(value3),f':c{i}',value1)
            template = re.sub(re.escape(match[0]),replacement,template)
            i = i+1
        format_add = f'<format>{form}</format>'
        template= template+format_add

        return template
