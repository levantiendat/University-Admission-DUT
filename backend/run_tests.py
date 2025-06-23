#!/usr/bin/env python
import sys
import subprocess
import os
import argparse

def run_tests(test_type=None, specific_test=None, verbose=False, html_report=False):
    """
    Runs pytest with specified parameters
    
    Args:
        test_type (str): The type of tests to run ('unit', 'integration', or None for all)
        specific_test (str): A specific test file or test function to run
        verbose (bool): Whether to run tests in verbose mode
        html_report (bool): Whether to generate HTML coverage report
    """
    command = ["pytest"]
    
    if verbose:
        command.append("-v")
    
    if test_type == "unit":
        command.append("tests/unit/")
    elif test_type == "integration":
        command.append("tests/integration/")
    
    if specific_test:
        command.append(specific_test)
        
    # Add coverage report generation
    command.extend(["--cov=app"])
    if html_report:
        command.append("--cov-report=html")
    else:
        command.append("--cov-report=term-missing")
    
    print(f"Running command: {' '.join(command)}")
    result = subprocess.run(command)
    return result.returncode

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run tests for University Admission backend")
    parser.add_argument("-t", "--type", choices=["unit", "integration"], 
                        help="Type of tests to run (unit or integration)")
    parser.add_argument("-s", "--specific", help="Run a specific test file or test function")
    parser.add_argument("-v", "--verbose", action="store_true", help="Run tests in verbose mode")
    parser.add_argument("--html", action="store_true", help="Generate HTML coverage report")
    
    args = parser.parse_args()
    
    exit_code = run_tests(args.type, args.specific, args.verbose, args.html)
    sys.exit(exit_code)
