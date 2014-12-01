# coding=utf-8
__author__ = 'Sławomir Domagała'
from result import Passed, Failed, Error
from test_runner import TestsRunner


class Printer:
    def __init__(self, scenarios_results):
        self.scenarios_results = scenarios_results

    def print_summary(self):
        print("Execution finished")
        for scenario_result in self.scenarios_results:
            print("Scenario \"{}\" with flags: {}".format(scenario_result.name, scenario_result.flags))
            for test_result in scenario_result.test_results:
                print("\tTest {}".format(test_result.name))
                for result in test_result.results:
                    if isinstance(result, Passed):
                        print("\t\t ASSERTION: {}\n\t\tPASSED".format(TestsRunner.assertions_names[result.class_name]))
                    elif isinstance(result, Failed):
                        print("\t\t ASSERTION: {}\n\t\tFAILED: EXPECTED {}\tGOT {}".format(
                            TestsRunner.assertions_names[result.class_name], result.expected, result.actual))
                    elif isinstance(result, Error):
                        print("\t\t {}\n\t\tERROR: {}".format(
                            TestsRunner.assertions_names[result.class_name], result.error))
                    else:
                        print("\t\t ASSERTION: {}\n\t\tUNKNOWN RESULT".format(
                            TestsRunner.assertions_names[result.class_name]))