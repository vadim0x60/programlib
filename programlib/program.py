from collections import namedtuple
from statistics import mean
from typing import NamedTuple
from uuid import uuid4
from pathlib import Path

from programlib import language_

def correctness(expected_outputs, outputs):
    assert expected_outputs, 'expected_outputs is empty. Cannot test program correctness.'

    outputs = outputs[:len(expected_outputs)]

    if outputs:
        return mean(int(expected_line == actual_line) 
                    for expected_line, actual_line 
                    in zip(expected_outputs, outputs))
    else:
        return 0

TestRun = namedtuple('TestRun', ['input_lines', 'expected_output_lines', 
                                 'output_lines', 'correctness'])

class Program():
    """
    Program object: represents a runnable program in some programming language
    """

    def __init__(self, source, name=None, language='C++', 
                       workdir=Path(__file__).parent / 'programs', 
                       force_build=False):
        self.language = language_[language]

        self.workdir = workdir
        self.name = name or str(uuid4())
        
        self.language.write_source(self.workdir, self.name, source)
        self.stdout, self.stderr = self.language.build(self.workdir, self.name)

        assert force_build or not self.stderr, self.stderr

    def __lt__(self, other):
        return self.name < other.name

    def run(self, input_lines=[], force=True):
        """
        Run the program and capture its output

        If 'input_lines' are specified, they will be sent to stdin.
        After the program has finished, `run` will check for errors on stderr
        and, in case there aren't any, return a list of output lines

        Use 'force=True' to skip the error check.
        Raw stdout and stderr data will always be stored in `program.stdout` and `program.stderr` attributes
        """
        
        self.stdout, self.stderr = self.language.run(self.workdir, self.name, input_lines)
        assert force or not self.stderr, self.stderr
        return self.stdout.splitlines()

    def score(self, test_cases, force=True, cache=True):
        """
        Test the program against a list of input output pairs

        If 'force=True', program outputs will be checked even if there are errors on stderr
        If 'cache=True', all the test logs will be stored in `program.test_runs` attribute
        """

        self.test_runs = []
        for input_lines, expected_output_lines in test_cases:
            try:
                output_lines = self.run(input_lines, force=force)
                test_run = TestRun(input_lines, expected_output_lines, 
                                   output_lines, correctness(expected_output_lines, output_lines))          
            except AssertionError:
                test_run = TestRun(input_lines, expected_output_lines, [], 0)

            self.test_runs.append(test_run)
        self.score = mean([run.correctness for run in self.test_runs])

        if not cache:
            del self.test_runs

        return self.score

    def save(self, path):
        self.language.copy_source(self.workdir, self.name, path)

    def __del__(self):
        self.language.cleanup(self.workdir, self.name)