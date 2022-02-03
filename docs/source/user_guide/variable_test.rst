*****************
Testing Variables
*****************

The most basic test you can do is a variable test. This is suited for when you want to check if a student assigned the correct value to a variable.

Setting up the test class
=========================

Setting up the test class:

.. code-block:: python

    from e2xtest import VariableTest

    tester = VariableTest(
        namespace=globals(),
        max_points=20,
        r_tol=0.01,
        a_tol=0.05
    )

First we need to define the namespace we use for testing. In a Jupyter notebook we will generally use ``globals()`` which gives us access to the general notebook namespace. The namespace is a dictionary containing all defined objects. However we can also test on a different namespace.

Next we define how many points the question we want to grade is worth (``max_points``). Finally we set criterias for our test to pass as the relative (``r_tol``) and absolute tolerance (``a_tol``).

.. role:: python(code)
   :language: python

Defining test cases
===================

Next we need to define our test cases. This is done using a list of dictionaries, where each dictionary is a single test case.

Anatomy of a test case
**********************

A basic test case for a variable has two entries. ``name`` is the name of the variable we want to test as a string. ``expected`` is the expected value or solution we want to compare with. Let us look at an example where we want to test if the variable ``answer`` holds the value ``42``.

.. code-block:: python

    test_cases = [
        {
            'name': 'answer',
            'expected': 42
        }
    ]

Optional parameters for a test case are:

* :python:`expected_type` - What type the answer should have
* :python:`weight` - How important the test case is. If this is not set all test cases will be equally important and the number of points per test case is the number of points divided by the number of test cases.
* :python:`test_function` - A custom test function

In the most basic test case the value of the variable will be assumed to be a number. For other data types you can define your own test function which tells the system how you want to compare the student answer with the solution.

Custom test functions
*********************

In case we want to test more complex data types or want to have a custom testing behavior we can define a custom test function.

.. code-block:: python

    def custom_test_function(student_answer, solution, a_tol, r_tol):
        '''
        My custom test function

        Args:
            answer   -- Student answer
            solution -- Correct answer
            a_tol    -- Absolute error tolerance
            r_tol    -- Relative error tolerance
        Returns:
            passed   -- How much of the test is passed (0 = not passed, 1 = 100% passed)
            msg      -- A feedback message for the student
        '''
        if answer != solution:
            return 0, 'The answer and solution do not match!'
        return 1, ''


Example 1
=========

Let us look at a complete example of a variable test. Assume the student has to calculate the mean, standard deviation and mode of a list of numbers. Let us further assume the student does not set the variable ``mode``:

.. code-block:: python

    mean = 5.0
    std = 2.123

The test cell would look like this:

.. code-block:: python

    from e2xtest import VariableTest
    from numbers import Number

    tester = VariableTest(
        namespace=globals(),
        max_points=20,
        r_tol=0.01,
        a_tol=0.05
    )

    test_cases = [
        {
            'name': 'mode',
            'expected': 4,
            'expected_type': Number
        },
        {
            'name': 'mean',
            'expected': 6.0
        },
        {
            'name': 'std',
            'expected': 2.123
        }
    ]

    passed = tester.test(test_cases)

This would produce the following output::

    ============================================================
    Variable Test

    ------------------------------------------------------------
    Running test 1
    Test for variable mode failed!
    Variable mode is not defined!

    0.0 / 6.67 points.
    ------------------------------------------------------------

    ------------------------------------------------------------
    Running test 2
    Test for variable mean failed!
    Expected was 6.0. Your answer is 5.0.

    0.0 / 6.67 points.
    ------------------------------------------------------------

    ------------------------------------------------------------
    Running test 3

    6.67 / 6.67 points.
    ------------------------------------------------------------

    ============================================================
    Total points: 6.67 / 20
    ============================================================



