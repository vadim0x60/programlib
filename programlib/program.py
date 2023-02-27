from collections import namedtuple
from statistics import mean, StatisticsError
from typing import NamedTuple
from uuid import uuid4
from pathlib import Path
from itertools import zip_longest

from programlib import language_

def correctness(expected_outputs, outputs):
    assert expected_outputs, 'expected_outputs is empty. Cannot test program correctness.'

    try:
        return mean(int(expected_line == actual_line) 
                    for expected_line, actual_line 
                    in zip_longest(expected_outputs, outputs))
    except StatisticsError:
        return 0

TestRun = namedtuple('TestRun', ['input_lines', 'expected_output_lines', 
                                 'output_lines', 'error_lines', 'correctness'])

class Agent():
    """
    Agent: represents a running program that can be interacted with
    """

    def __init__(self, program, process):
        self.program = program
        self.process = process
        
        self.program.stdout = ''
        self.program.stderr = ''

    def act(self, input_lines):
        input = '\n'.join(input_lines).encode()
        stdout, stderr = self.process.communicate(input)
        stdout = stdout.decode()
        stderr = stderr.decode()
        self.program.stdout += stdout
        self.program.stderr += stderr
        return stdout.splitlines()
    
    def close(self):
        self.process.kill()
    
    def __del__(self):
        self.close()

class Program():
    """
    Program object: represents a runnable program in some programming language
    """

    def __init__(self, source, name=None, language='C++', 
                       workdir=Path(__file__).parent / 'programs'):
        self.language = language_(language)

        self.workdir = workdir
        self.name = name or str(uuid4())
        
        self.language.write_source(self.workdir, self.name, source)
        self.stdout, self.stderr = self.language.build(self.workdir, self.name)

        # Please send your opinions on 'not not' vs 'bool()' to dont@vadim.me
        self.compile_error = not not self.stderr

    def __lt__(self, other):
        return self.name < other.name

    def read(self):
        """Obtain the source code of the program"""

        return self.language.read_source(self.workdir, self.name)

    def run(self, input_lines=[], force=True):
        """
        Run the program and capture its output

        If 'input_lines' are specified, they will be sent to stdin.
        After the program has finished, `run` will check for errors on stderr
        and, in case there aren't any, return a list of output lines

        Use 'force=True' to skip the error check.
        Raw stdout and stderr data will always be stored in `program.stdout` and `program.stderr` attributes
        """

        input = '\n'.join(input_lines).encode()
        stdout, stderr = self.language.run(self.workdir, self.name, input)
        assert force or not stderr, stderr

        self.stdout = stdout.decode()
        self.stderr = stderr.decode()
        return self.stdout.splitlines()
    
    def start(self):
        """
        Launch the program and get a process object to communicate with it interactively
        """

        process = self.language.Popen(self.workdir, self.name)
        return Agent(self, process)

    def test(self, test_cases, force=True):
        """
        Test the program against a list of input output pairs

        If 'force=True', program outputs will be checked even if there are errors on stderr
        If 'cache=True', all the test logs will be stored in `program.test_runs` attribute
        """

        test_runs = []

        for input_lines, expected_output_lines in test_cases:
            test_run = None

            if not self.compile_error:
                try:
                    output_lines = self.run(input_lines, force=force)
                    test_run = TestRun(input_lines, expected_output_lines, 
                                       output_lines, self.stderr.splitlines(),
                                       correctness(expected_output_lines, output_lines))          
                except AssertionError:
                    pass

            if not test_run:
                test_run = TestRun(input_lines, expected_output_lines, 
                                   self.stderr.splitlines(), [], 0)

            test_runs.append(test_run)

        self.avg_score = mean([run.correctness for run in test_runs])
        self.pass_rate = mean([int(run.correctness == 1) for run in test_runs])

        return test_runs

    def save(self, path):
        self.language.copy_source(self.workdir, self.name, path)

    def __del__(self):
        self.language.cleanup(self.workdir, self.name)