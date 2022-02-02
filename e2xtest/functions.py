import ast
import inspect
from .test_functions import test_numerical
from .utils import HiddenPrints
from .base import BaseTest

class FunctionTest(BaseTest):
    '''
    A test class for functions.
    '''

    def __init__(
        self,
        namespace,
        function_name,
        max_points,
        reference_function=None,
        test_function=test_numerical,
        r_tol=0,
        a_tol=0,
    ):
        '''
        Create a function test

        Args:
            namespace          -- The namespace the test works on. In a notebook this should usually be globals()
            function_name      -- The name of the student function to be tested
            max_points         -- How many points (marks) all tests are worth
            reference_function -- Optional reference implementation of the function
            r_tol              -- The relative tolerance for a test to pass
            a_tol              -- The absolute tolerance for a test to pass
        '''
        super().__init__(namespace, r_tol, a_tol, f'Function Test for {function_name}', max_points)
        self.fun_name = function_name
        self.test_function = test_function
        self.reference_function = reference_function

    def is_callable(self):
        '''
        Check whether the student function can be called

        Returns:
            callable -- Whether or not the student function is callable
        '''
        return callable(self.namespace[self.fun_name])

    def has_return_statement(self):
        '''
        Check whether the student function has a return statement

        Returns:
            has_return -- Whether or not the student function has a return statement
        '''
        return any(
            isinstance(node, ast.Return)
            for node in ast.walk(
                ast.parse(inspect.getsource(self.namespace[self.fun_name]))
            )
        )

    def run_pre_tests(self):
        '''
        Run specific general tests against the student function
        This includes checking if the function is defined, is callable
        and has a return statement

        Returns:
            passed -- Whether or not the general tests have passed
        '''
        if not self.is_defined(self.fun_name):
            print(f"Function {self.fun_name} is not defined!")
            return False
        elif not self.is_callable():
            print(f"{self.fun_name} is not callable!")
            return False
        elif not self.has_return_statement():
            print(f"{self.fun_name} does not have a return statement!")
            return False
        return True

    def call_function(self, function, test_case):
        '''
        Call the function with the arguments in the test case
        Arguments can be defined as arg (a single argument),
        args (a list of arguments) or kwargs (a dictionary of keyword arguments)

        Args:
            function  -- A function to be called
            test_case -- A dictionary containing information of the test
        Returns:
            result    -- The result of the function applied to the arguments
        '''
        if "arg" in test_case:
            return function(test_case["arg"])
        elif "args" in test_case:
            return function(*test_case["args"])
        elif "kwargs" in test_case:
            return function(**test_case["kwargs"])

    def run_test_case(self, test_case):
        '''
        Run a single test case

        Args:
            test_case -- A dictionary containing information of the test
        Returns:
            passed    -- How much of the test is passed (0 = not passed, 1 = 100% passed)
            msg       -- An explaination in case the test did not pass
        '''
        if "arg" in test_case:
            arguments = f'arg = {test_case["arg"]}'
        elif "args" in test_case:
            arguments = f'args = {test_case["args"]}'
        elif "kwargs" in test_case:
            arguments  = f'kwargs = {test_case["kwargs"]}'
        error_msg = f'Test for {arguments} failed!\n'
        if "expected" in test_case:
            target = test_case["expected"]
        else:
            target = self.call_function(self.reference_function, test_case)

        max_reruns = 1
        if "max_reruns" in test_case:
            max_reruns = test_case["max_reruns"]
        try:
            test_function = test_case.get('test_function', self.test_function)
            with HiddenPrints():
                for _ in range(max_reruns):
                    result = self.call_function(
                        self.namespace[self.fun_name], test_case
                    )
                    status, msg = test_function(
                        result,
                        target,
                        self.a_tol,
                        self.r_tol
                    )
                    if status < 1:
                        error_msg += msg
                    return status, error_msg
        except Exception as e:
            print(self.line)
            print(f"Test with args {test_case} failed!\n{e}\n")
            return 0, e
