# coding=utf-8
from assert_path import *
from asserts import *
from command_response import *
from indor_exceptions import SyntaxErrorWrongNumberOfArguments
from parsing_exception import ParsingException
from transform_nested_array import transform_nested_array


class Assert(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT"

    def __init__(self, result_collector):
        super(Assert, self).__init__(result_collector)

    def parse(self, path):
        path = transform_nested_array(path, self.result_collector.use_variables)

        if len(path) == 0:
            raise SyntaxErrorWrongNumberOfArguments(self.__class__.__name__,
                                                         hints=CommandFactory().get_class_children(
                                                             self.__class__.__name__))
        if path[0].lower() == "text" or path[0].lower() == "cookie" or path[0].lower() == "header" or path[0].lower() == "response":
            command = CommandFactory().get_class("Command", path[0], self.result_collector)
            try:
                computed, parsed = command.parse(path[1:])
                if computed == parsed.value:
                    self.result_collector.add_result(Passed(parsed.parsing_object))
                else:
                    self.result_collector.add_result(Failed(parsed.parsing_object, parsed.description, computed))
            except ParsingException as e:
                self.result_collector.add_result(Error(e.parsing_object, e.message))
        else:
            CommandFactory().get_class(self.__class__.__name__, path[0], self.result_collector).parse(path[1:])
