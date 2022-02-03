.. e2xtest documentation master file, created by
   sphinx-quickstart on Thu Feb  3 14:28:52 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

e2xtest
===================================

``e2xtest`` is a tool to create interactive tests for cells in student Jupyter notebooks. The teacher can define a list of tests that are executed and graded. The output of the test can be read by ``nbgrader`` or ``e2xgrader`` to automatically assign partial points to a solution.

There exist two types of tests. One aimed at testing variables, one aimed at testing functions.

.. toctree::
   :maxdepth: 2
   :caption: User Documentation:

   user_guide/highlights
   user_guide/installation
   user_guide/variable_test
   user_guide/function_test



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
