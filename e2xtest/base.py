class BaseTest:
    '''
    Base class for all test classes.
    '''

    def __init__(self, namespace, r_tol, a_tol, test_type, max_points):
        '''
        Create a base test

        Args:
            namespace  -- The namespace the test works on. In a notebook this should usually be globals()
            r_tol      -- The relative tolerance for a test to pass
            a_tol      -- The absolute tolerance for a test to pass
            test_type  -- The type of test we are performing as a string
            max_points -- How many points (marks) all tests are worth
        '''
        self.namespace = namespace
        self.r_tol = r_tol
        self.a_tol = a_tol
        self.line = "-" * 60
        self.double_line = "=" * 60
        self.test_type = test_type
        self.max_points = max_points

    def is_defined(self, name):
        '''
        Check if an object is defined in the namespace

        Args:
            name       -- Name of the object
        Returns:
            is_defined -- If the object is defined
        '''
        return name in self.namespace

    def has_type(self, name, target_type):
        '''
        Check whether an object is of a certain type

        Args:
            name        -- Name of the object
            target_type -- The expected type of the object
        Returns:
            has_type    -- If the object is of the expected type
        '''
        return isinstance(self.namespace[name], target_type)

    def run_pre_tests(self):
        '''
        Run general tests before the single test cases

        Returns:
            success -- Whether or not the general tests passed
        '''
        return True

    def run_test_case(self, test_case):
        '''
        Run a single test case

        Args:
            test_case -- A dictionary containing information of the test
        Returns:
            passed    -- How much of the test is passed (0 = not passed, 1 = 100% passed)
            msg       -- An explaination in case the test did not pass
        '''
        return 1, ''

    def test(self, test_cases):
        '''
        Run a series of test cases
        Prints the status to screen

        Args:
            test_cases -- A list of single test cases
        Returns:
            points     -- How many points the student gets
        '''
        weights = [test_case.get('weight', 1) for test_case in test_cases]
        normalized_weights = [weight / sum(weights) for weight in weights]
        passed = 0

        print(self.double_line)
        print(f"{self.test_type}\n")

        if self.run_pre_tests():
            for test_id, test_case in enumerate(test_cases):
                print(self.line)
                points = round(self.max_points * normalized_weights[test_id], 2)
                print(f'Running test {test_id+1}')
                status, msg = self.run_test_case(test_case)
                passed += normalized_weights[test_id] * status
                if status < 1:
                    print(msg )
                print(f'\n{round(status*points,2)} / {points} points.')
                print(self.line)
                print()
        print(self.double_line)
        print(f"Total points: {round(self.max_points*passed, 2)} / {self.max_points}")
        print(self.double_line)
        return passed
