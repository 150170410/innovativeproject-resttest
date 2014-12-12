__author__ = 'Damian Mirecki'

import unittest
from scenario_results import ScenarioResults
from result import Passed, Error, Failed
import test_runner
import input_parser as parser


class TestBehavioral(unittest.TestCase):
    def run_indor(self, data):
        test_data = parser.parse(data)
        runner = test_runner.TestsRunner()
        return runner.run(test_data)

    def assertAllPassed(self, results):
        for result in results:
            self.assertIsInstance(result, Passed)

    def assertScenarioCount(self, count, result):
        self.assertEqual(count, len(result))
        for scenario in result:
            self.assertIsInstance(scenario, ScenarioResults)

    def test_hello_world(self):
        test = """
            GET http://httpbin.org/ .
            ASSERT RESPONSE STATUS OK.
        """

        result = self.run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]
        self.assertEqual(1, len(scenario.test_results))

        results = scenario.test_results[0].results
        self.assertAllPassed(results)

    def test_basic_assertions(self):
        test = """
            # Connect
            GET http://httpbin.org/get.

            # Basic assertions on response

            ASSERT RESPONSE STATUS OK.		# Other options: Not Found, number eg. 500...
            ASSERT RESPONSE TYPE JSON.		# Other options: XML, HTML
            ASSERT RESPONSE NOT EMPTY.
            ASSERT RESPONSE LENGTH < 12345.  # Options: "=" , "<" , ">" , "<=" , ">="
        """

        result = self.run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]

        results = scenario.test_results[0].results
        self.assertEqual(4, len(results))
        self.assertAllPassed(results)

    def test_basic_auth(self):
        test = """
            GET
                http://httpbin.org/basic-auth/username/password,
            AUTH
                username password
                .

            ASSERT RESPONSE STATUS OK.
        """

        result = self.run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]

        results = scenario.test_results[0].results
        self.assertEqual(1, len(results))
        self.assertAllPassed(results)

    def test_digest_auth(self):
        test = """
            GET
                http://httpbin.org/digest-auth/auth/user/pass,
            AUTH DIGEST
                user pass.

            ASSERT RESPONSE STATUS OK.
        """

        result = self.run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]

        results = scenario.test_results[0].results
        self.assertEqual(1, len(results))
        self.assertAllPassed(results)

    def test_allow_redirects(self):
        test = """
            GET
                http://httpbin.org/redirect/2,
            ALLOW REDIRECTS.
            ASSERT RESPONSE STATUS Ok.
            ASSERT RESPONSE REDIRECTS COUNT = 2.
        """

        result = self.run_indor(test)
        self.assertScenarioCount(1, result)

        scenario = result[0]

        results = scenario.test_results[0].results
        self.assertEqual(2, len(results))
        self.assertAllPassed(results)
