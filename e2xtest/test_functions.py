def test_numerical(answer, solution, a_tol, r_tol):
    '''
    Test an numerical answer vs a solution

    Args:
        answer   -- Student answer
        solution -- Correct answer
        a_tol    -- Absolute error tolerance
        r_tol    -- Relative error tolerance
    Returns:
        passed   -- How much of the test is passed (0 = not passed, 1 = 100% passed)
        msg      -- A feedback message for the student
    '''
    abs_error = abs(answer - solution)
    rel_error = abs_error / solution
    if (abs_error <= a_tol or rel_error <= r_tol):
        return 1, ''
    return 0, f'Expected was {solution}. Your answer is {answer}.'
