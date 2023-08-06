from abc import ABC, abstractmethod


class IReporter(ABC):

    @abstractmethod
    def report(self, template):
        pass

    @abstractmethod
    def set_successor(self, successor):
        pass

    @abstractmethod
    def set_data(self, data):
        pass


class IMethod(ABC):

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def set_successor(self):
        pass


class IFormatter(ABC):

    @abstractmethod
    def format(self,value,condition,format_sepec):
        pass

    @abstractmethod
    def set_successor(self, successor):
        pass


class IFormatHandler(ABC):

    @abstractmethod
    def handle(self, value, condition, format_specs, format_pattern):
        pass

    @abstractmethod
    def set_successor(self, successor):
        pass
