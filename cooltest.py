# finds all tests in the current directory (recursively),
# executes them and prints the status for each: PASS, FAIL or SKIP.
# input data can be passed to the tests from the command line:

import importlib
import sys
import glob
import os
from inspect import getmembers, isfunction


class TestFailure(Exception):
    """Exception raised when a test fails."""
    pass

def fail(message):
    print(message)


class TestSkip(Exception):
    """Exception raised to skip a test."""
    pass


def skipif(condition, message="Test skipped"):
    print("Som v skipif")
    if condition:
        raise TestSkip(message)


def run_tests():
    test_files = glob.glob('test_*.py')
    test_modules = [os.path.splitext(os.path.basename(f))[0] for f in test_files]

    for module_name in test_modules:
        module = importlib.import_module(module_name)
        functions_in_test_example = getmembers(module, isfunction)
        print(functions_in_test_example)

        # Now, iterate over the list of function tuples
        for func_name, _ in functions_in_test_example:
            # Check if the function name starts with 'test_'
            if func_name.startswith('test_'):
                test_func = getattr(module, func_name)
                test_func()

run_tests()
