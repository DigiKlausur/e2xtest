*****************
Testing Functions
*****************

Often we want a student to provide an answer in the form of a function. For this we can use the ``FunctionTest`` class.

Setting up the test class
=========================

Setting up the test class:

.. code-block:: python

    from e2xtest import FunctionTest

    tester = VariableTest(
        namespace=globals(),
        max_points=20,
        r_tol=0.01,
        a_tol=0.05,
        function_name='square',
    )

First we need to define the namespace we use for testing. In a Jupyter notebook we will generally use ``globals()`` which gives us access to the general notebook namespace. The namespace is a dictionary containing all defined objects. However we can also test on a different namespace.

Next we define how many points the question we want to grade is worth (``max_points``). Finally we set criterias for our test to pass as the relative (``r_tol``) and absolute tolerance (``a_tol``). Finally we need to specify the name of the function by the student (``function_name``) as a string.

If we want to test the student function against a reference function we can provide this using the ``reference_function`` argument.

.. role:: python(code)
   :language: python

Defining test cases
===================

Next we need to define our test cases. This is done using a list of dictionaries, where each dictionary is a single test case.

Anatomy of a test case
**********************

The first entry in the test case should be the arguments on which the student function is tested. This can be specified in three ways:

1. ``arg`` - a single argument. The student function will be called as :python:`f(arg)`
2. ``args`` - a list of arguments. The student function will be called as :python:`f(*args)`
3. ``kwargs`` - a dictionary of keyword arguments. The student function will be called as :python:`f(**kwargs)`

If you provided a reference function in the constructor of the function test you do not need to specify a desired result:

.. code-block:: python

    test_cases = [
        {
            'arg': 5
        }
    ]

In case you did not provide a reference function you need to give the expected value. If you provided a reference function and still give an expected value the output will be tested against this:

.. code-block:: python

    test_cases = [
        {
            'arg': 5,
            'expected': 25
        }
    ]

Optional parameters for a test case are:

* :python:`weight` - How important the test case is. If this is not set all test cases will be equally important and the number of points per test case is the number of points divided by the number of test cases.
* :python:`max_reruns` - In case you want to do a probabilistic test that might sometimes fail, you can give a parameter that tells the test how often it should run until it is marked as failed.
* :python:`test_function` - A custom test function.


Example 1 - Function fails with some arguments
==============================================

Let us look at a complete example of a function test. Assume the student has to implement a function ``square`` that returns the square of a number. The student implemented this wrong (see below). We also want to provide a reference function.

.. code-block:: python

    def square(x):
        if x < 7:
            return x*x
        return 70

The test cell would look like this:

.. code-block:: python

    from e2xtest import FunctionTest

    tester = FunctionTest(
        namespace=globals(),
        max_points=20,
        r_tol=0.01,
        a_tol=0.05,
        function_name='square',
        reference_function=lambda x: x**2
    )

    test_cases = [
        {
            'arg': 5
        },
        {
            'arg': 6,
            'expected': 36
        },
        {
            'args': [7]
        }
    ]

    passed = tester.test(test_cases)

This would produce the following output::

    ============================================================
    Function Test for square

    ------------------------------------------------------------
    Running test 1

    6.67 / 6.67 points.
    ------------------------------------------------------------

    ------------------------------------------------------------
    Running test 2

    6.67 / 6.67 points.
    ------------------------------------------------------------

    ------------------------------------------------------------
    Running test 3
    Test for args = [7] failed!
    Expected was 49. Your answer is 70.

    0.0 / 6.67 points.
    ------------------------------------------------------------

    ============================================================


Example 2 - No return statement
===============================

Let us now assume the student forgot to return the result of the square function and instead prints it.

Student answer:

.. code-block:: python

    def square(x):
        print(x*x)

The test cell would look like this:

.. code-block:: python

    from e2xtest import FunctionTest

    tester = FunctionTest(
        namespace=globals(),
        max_points=20,
        r_tol=0.01,
        a_tol=0.05,
        function_name='square',
        reference_function=lambda x: x**2
    )

    test_cases = [
        {
            'arg': 5
        }
    ]

    passed = tester.test(test_cases)

This would produce the following output::

    ============================================================
    Function Test for square

    square does not have a return statement!
    ============================================================
    Total points: 0 / 20
    ============================================================


Example 3 - Function not callable
=================================

Let us now assume the student did not provide a function.

Student answer:

.. code-block:: python

    x = 5

    square = x*x

The test cell would look like this:

.. code-block:: python

    from e2xtest import FunctionTest

    tester = FunctionTest(
        namespace=globals(),
        max_points=20,
        r_tol=0.01,
        a_tol=0.05,
        function_name='square',
        reference_function=lambda x: x**2
    )

    test_cases = [
        {
            'arg': 5
        }
    ]

    passed = tester.test(test_cases)

This would produce the following output::

    ============================================================
    Function Test for square

    square is not callable!
    ============================================================
    Total points: 0 / 20
    ============================================================


Example 4 - Using a custom test function
========================================

Let us assume that we know that some students return a string instead of float. We still want to give them some points for this.

Then we can implement a custom test function.

Student answer:

.. code-block:: python

    def square(x):
        return str(x*x)

The test cell would look like this:

.. code-block:: python

    from e2xtest import FunctionTest

    def test_square(student_answer, solution, a_tol, r_tol):
        '''
        My square test function

        Args:
            answer   -- Student answer
            solution -- Correct answer
            a_tol    -- Absolute error tolerance
            r_tol    -- Relative error tolerance
        Returns:
            passed   -- How much of the test is passed (0 = not passed, 1 = 100% passed)
            msg      -- A feedback message for the student
        '''
        passed = 1.0
        msg = ''
        if isinstance(student_answer, str):
            # Deduct 40% of marks for this test
            passed -= 0.4
            msg += 'You should give your result as a number and not a string!\n'
            student_answer = float(student_answer)
        abs_error = abs(student_answer - solution)
        if abs_error < a_tol:
            return passed, msg
        msg += f'Your result is wrong. Expected answer was {solution}.'
        msg += f'Your answer is {student_answer}'
        return 0, msg

    tester = FunctionTest(
        namespace=globals(),
        max_points=20,
        r_tol=0.01,
        a_tol=0.05,
        function_name='square',
        reference_function=lambda x: x**2
    )

    test_cases = [
        {
            'arg': 5
        }
    ]

    passed = tester.test(test_cases)

This would produce the following output::

    ============================================================
    Function Test for square

    ------------------------------------------------------------
    Running test 1
    Test for arg = 5 failed!
    You should give your result as a number and not a string!


    14.0 / 20.0 points.
    ------------------------------------------------------------

    ============================================================
    Total points: 14.0 / 20
    ============================================================
