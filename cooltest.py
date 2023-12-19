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
        if arg.startswith('--'):
            key = arg[2:]  # Odstránenie '--'
            try:
                # Predpokladáme, že hodnota nasleduje za kľúčom
                value = next(it)
                cmdline_args[key] = value
            except StopIteration:
                print(f"Warning: Argument {key} is ignored because doesnt contain value")
        else:
            print(f"Warning: Argument {arg} is not valid")

    return cmdline_args


def run_tests(cmdline_args):
    passed_count = 0
    failed_count = 0
    skipped_count = 0
    test_files = glob.glob('test_*.py')
    test_modules = [os.path.splitext(os.path.basename(f))[0] for f in test_files]
    print("Collected tests from: " + ', '.join(test_modules))

    for module_name in test_modules:
        header = f"=== {module_name} " + "=" * (50 - len(module_name))
        print(header)

        module = importlib.import_module(module_name)
        functions_in_test_example = getmembers(module, isfunction)

        for func_name, _ in functions_in_test_example:
            if func_name.startswith('test_'):
                print(f"{module_name}.{func_name}():")
                test_func = getattr(module, func_name)
                sig = signature(test_func)
                args_to_send = {}
                for param_name, param in sig.parameters.items():
                    if param_name in cmdline_args.keys():
                        args_to_send[param_name] = cmdline_args[param_name]
                try:
                    if args_to_send:
                        test_func(**args_to_send)
                    else:
                        test_func()
                    print("[PASS]")
                    passed_count += 1
                except TestFailure as tf:
                    print("    [FAIL]")
                    print(f"    Reason: {tf}")
                    failed_count += 1
                except TestSkip as ts:
                    # Handle test skip exception
                    print("    [SKIP]")
                    print(f"    Reason: {ts}")
                    skipped_count += 1

        total_count = passed_count + failed_count + skipped_count
        print(f"Finished. {total_count} total; {passed_count} passed, {failed_count} failed, {skipped_count} skipped.")


def main():
    print("Starting a new test session with arguments:")
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--dut_ip', help='IP address of DUT')
    parser.add_argument('--sky', help='Colour of sky')
    parser.add_argument('--rain', help='Yes or no')
    # Parse known arguments
    # Process command-line arguments
    cmdline_args = parse_cmdline_args(sys.argv[1:])
    print(cmdline_args)
    # Run the tests with the processed command-line arguments
    run_tests(cmdline_args)

if __name__ == '__main__':
    main()