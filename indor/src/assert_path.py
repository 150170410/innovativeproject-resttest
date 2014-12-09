import xml.etree.ElementTree as ET
from command import Command
from command_factory import CommandFactory
from command_register import CommandRegister
from xml_tree_factory import XmlTreeFactory
from xml_tree_register import XmlTreeRegister
from result import Error, Passed, Failed
import result
import parsers_to_xml_tree


class AssertPath(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH"

    def __init__(self, result_collector):
        super(AssertPath, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 2:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
        else:
            url = path[0]
            next_step = CommandFactory().get_class(self.__class__.__name__, path[1], self.result_collector)
            path = path[2:]
            path.insert(0, url)
            next_step.parse(path)


class AssertPathExists(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH EXISTS"

    def __init__(self, result_collector):
        super(AssertPathExists, self).__init__(result_collector)

    def parse(self, path):
        if len(path) != 1:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
        else:
            self.execute(path[0])

    def execute(self, url):
        tree = XmlTreeFactory().get_class(self.result_collector.get_response().headers.get('content-type'))
        doc = tree.parse(self.result_collector.get_response().content)
        url.replace("\"", "", 2)
        if len(doc.findall(url)) > 0:
            self.result_collector.add_result(Passed(self))
        else:
            self.result_collector.add_result(Failed(self,"EXISTS", "NO EXISTS"))


class AssertPathContains(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH CONTAINS"

    def __init__(self, result_collector):
        super(AssertPathContains, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 2:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
        else:
            url = path[0]
            from command_factory import CommandFactory

            next_step = CommandFactory().get_class(self.__class__.__name__, path[1], self.result_collector)
            path = path[2:]
            path.insert(0, url)
            next_step.parse(path)


class AssertPathContainsAny(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH CONTAINS ANY"

    def __init__(self, result_collector):
        super(AssertPathContainsAny, self).__init__(result_collector)

    def parse(self, path):
        if len(path) != 2:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
        else:
            self.execute(path)

    def execute(self, path):
        tree = XmlTreeFactory().get_class(self.result_collector.get_response().headers.get('content-type'))
        doc = tree.parse(self.result_collector.get_response().content)
        path[0].replace("\"", "", 2)
        for e in doc.findall(path[0]):
            if path[1] == e.text:
                self.result_collector.add_result(Passed(self))
                return

        self.result_collector.add_result(Failed(self, "ASSERT PATH CONTAINS ANY", "NOP"))


class AssertPathContainsEach(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH CONTAINS EACH"

    def __init__(self, result_collector):
        super(AssertPathContainsEach, self).__init__(result_collector)

    def parse(self, path):
        if len(path) != 2:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
        else:
            self.execute(path)


    def execute(self, path):
        tree = XmlTreeFactory().get_class(self.result_collector.get_response().headers.get('content-type'))
        doc = tree.parse(self.result_collector.get_response().content)
        path[0].replace("\"", "", 2)
        for e in doc.findall(path[0]):
            if path[1] == e.text:
                self.result_collector.add_result(Failed(self), "ASSERT PATH CONTAINS EACH", "NOP")
                return
        self.result_collector.add_result(Passed(self))


class AssertPathNodes(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH NODES"

    def __init__(self, result_collector):
        super(AssertPathNodes, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 2:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
        else:
            url = path[0]
            next_step = CommandFactory().get_class(self.__class__.__name__, path[1], self.result_collector)
            path = path[2:]
            path.insert(0, url)
            next_step.parse(path)


class AssertPathNodesCount(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH NODES COUNT"

    def __init__(self, result_collector):
        super(AssertPathNodesCount, self).__init__(result_collector)

    def parse(self, path):
        if len(path) < 2:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
        else:
            symbol = path[1]
            url = path[0]
            path = path[2:]
            path.insert(0, url)
            if symbol == "=":
                next_step = AssertPathNodesCountEqual(self.result_collector)
                next_step.parse(path)
            elif symbol == ">":
                next_step = AssertPathNodesCountGreater(self.result_collector)
                next_step.parse(path)
            elif symbol == "<":
                next_step = AssertPathNodesCountLess(self.result_collector)
                next_step.parse(path)
            else:
                next_step = CommandFactory().get_class(self.__class__.__name__, path[1], self.result_collector)
                next_step.parse(path)


class AssertPathNodesCountEqual(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH NODES COUNT EQUAL"

    def __init__(self, result_collector):
        super(AssertPathNodesCountEqual, self).__init__(result_collector)

    def parse(self, path):
        if len(path) >= 2:
            self.execute(path)

    def execute(self, path):
        tree = XmlTreeFactory().get_class(self.result_collector.get_response().headers.get('content-type'))
        doc = tree.parse(self.result_collector.get_response().content)
        path[0].replace("\"", "", 2)
        num = len(doc.findall(path[0]))
        if num == int(path[1]):
            self.result_collector.add_result(Passed(self))
        else:
            self.result_collector.add_result(Failed(self, "ASSERT PATH NODES COUNT EQUAL", "IS :" + str(num)
                                                    + " expected " + path[1]))


class AssertPathNodesCountGreater(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH NODES COUNT GREATER"

    def __init__(self, result_collector):
        super(AssertPathNodesCountGreater, self).__init__(result_collector)

    def parse(self, path):
        if len(path) >= 2:
            self.execute(path)

    def execute(self, path):
        tree = XmlTreeFactory().get_class(self.result_collector.get_response().headers.get('content-type'))
        doc = tree.parse(self.result_collector.get_response().content)
        path[0].replace("\"", "", 2)
        num = len(doc.findall(path[0]))
        if num > int(path[1]):
            self.result_collector.add_result(Passed(self))
        else:
            self.result_collector.add_result(Failed(self, "ASSERT PATH NODES COUNT GREATER", "IS :" + str(num)
                                                    + " expected more than " + path[1]))


class AssertPathNodesCountLess(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH NODES COUNT LESS"

    def __init__(self, result_collector):
        super(AssertPathNodesCountLess, self).__init__(result_collector)

    def parse(self, path):
        if len(path) >= 2:
            self.execute(path)

    def execute(self, path):
        tree = XmlTreeFactory().get_class(self.result_collector.get_response().headers.get('content-type'))
        doc = tree.parse(self.result_collector.get_response().content)
        path[0].replace("\"", "", 2)
        num = len(doc.findall(path[0]))
        if num < int(path[1]):
            self.result_collector.add_result(Passed(self))
        else:
            self.result_collector.add_result(Failed(self, "ASSERT PATH NODES COUNT LESS", "IS :" + str(num)
                                                    + " expected less than " + path[1]))


class AssertPathFinal(Command):
    __metaclass__ = CommandRegister

    pretty_name = "ASSERT PATH FINAL"

    def __init__(self, result_collector):
        super(AssertPathFinal, self).__init__(result_collector)

    def parse(self, path):
        if len(path) != 1:
            self.result_collector.add_result(Error(self, result.ERROR_NOT_ENOUGH_ARGUMENTS))
        else:
            self.execute(path)

    def execute(self, path):
        tree = XmlTreeFactory().get_class(self.result_collector.get_response().headers.get('content-type'))
        doc = tree.parse(self.result_collector.get_response().content)
        path[0].replace("\"", "", 2)
        if len(doc.findall(path[0]))>0 and len(doc.findall(path[0]+"/*")) == 0:
            self.result_collector.add_result(Passed(self))
        else:
            self.result_collector.add_result(Failed(self, "ASSERT PATH FINAL", "NOT FINAL"))