from .base import BaseTest
from .test_functions import test_numerical

class VariableTest(BaseTest):
    '''
    A test class for variables.
    '''

    def __init__(self, namespace, max_points, r_tol=0, a_tol=0):
        super().__init__(namespace, r_tol, a_tol, 'Variable Test', max_points)

    def run_test_case(self, test_case):
        '''
        Run a single test case

        Args:
            test_case -- A dictionary containing information of the test
        Returns:
            passed    -- How much of the test is passed (0 = not passed, 1 = 100% passed)
            msg       -- An explaination in case the test did not pass
        '''
        name = test_case['name']
        expected = test_case['expected']

        error_msg = f'Test for variable {test_case["name"]} failed!\n'
        if not self.is_defined(name):
            error_msg += f'Variable {name} is not defined!'
            return 0, error_msg
        if 'expected_type' in test_case:
            expected_type = test_case['expected_type']
            if not self.has_type(name, expected_type):
                error_msg += f"Variable {name} is not of type {expected_type}!"
                return 0, error_msg
        try:
            test_function = test_case.get('test_function', test_numerical)
            status, msg = test_function(
                self.namespace[test_case['name']],
                test_case['expected'],
                self.a_tol,
                self.r_tol
            )
            if status < 1:
                error_msg += msg
            return status, error_msg
        except Exception as e:
            return 0, e
