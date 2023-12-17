# finds all tests in the current directory (recursively),
# executes them and prints the status for each: PASS, FAIL or SKIP.
# input data can be passed to the tests from the command line:
import argparse
import importlib
import sys
import glob
import os
from inspect import getmembers, isfunction, signature

class TestFailure(Exception):
    """Exception raised when a test fails."""
    pass

def failif(message):
    print(message)

def fail(message):
    print(message)


class TestSkip(Exception):
    """Exception raised to skip a test."""

def skipif(condition, message="Test skipped"):
    if condition:
        raise TestSkip(message)

def skip(message):
    print(message)

def parse_cmdline_args(args):
    cmdline_args = {}
    # Spracujeme argumenty vo dvojiciach
    it = iter(args)
    for arg in it:
        print("vypisem arg")
        print(arg)
        if arg.startswith('--'):
            key = arg[2:]  # Odstránenie '--'
            try:
                # Predpokladáme, že hodnota nasleduje za kľúčom
                value = next(it)
                cmdline_args[key] = value
            except StopIteration:
                print(f"Varovanie: Argument {key} je ignorovaný, pretože neobsahuje hodnotu.")
        else:
            print(f"Varovanie: Argument {arg} nie je platný.")

    return cmdline_args



def run_tests():
    test_files = glob.glob('test_*.py')
    test_modules = [os.path.splitext(os.path.basename(f))[0] for f in test_files]
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--dut_ip', help='IP adress of DUT')
    parser.add_argument('--sky', help='Colour of sky')
    parser.add_argument('--rain', help='Yes or no')
    # Vytvorte parser a povedzte mu, aby ignoroval neznáme argumenty
    # Tu môžete pridať známe argumenty, ak sú nejaké
    known_args, unknown_args = parser.parse_known_args()

    # Použitie funkcie na spracovanie argumentov príkazového riadku
    cmdline_args = parse_cmdline_args(sys.argv[1:])
    print(cmdline_args)

    for module_name in test_modules:
        module = importlib.import_module(module_name)
        functions_in_test_example = getmembers(module, isfunction)
        print(functions_in_test_example)

        # Now, iterate over the list of function tuples
        for func_name, _ in functions_in_test_example:
            # Check if the function name starts with 'test_'
            args_to_send = {}
            if func_name.startswith('test_'):
                num_of_parameters = 0
                test_func = getattr(module, func_name)
                sig = signature(test_func)
                for param_name, param in sig.parameters.items():
                    if param_name in cmdline_args.keys():
                        args_to_send[param_name] = cmdline_args[param_name]

            # param name su argumenty, ktore potrebujem, prechadzam ich a ked taky najdem v slovniku, tak ho poslem


run_tests()
