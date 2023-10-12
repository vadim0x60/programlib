from collections import namedtuple
from statistics import mean, StatisticsError
from typing import NamedTuple
from uuid import uuid4
from pathlib import Path
from itertools import zip_longest

from programlib import Agent, language_, Terminal

def correctness(expected_outputs, outputs):
    assert expected_outputs, 'expected_outputs is empty. Cannot test program correctness.'

    try:
        return mean(int(expected_line == actual_line) 
                    for expected_line, actual_line 
                    in zip_longest(expected_outputs, outputs))
    except StatisticsError:
        return 0

TestRun = namedtuple('TestRun', ['input_lines', 'expected_output_lines', 
                                 'output_lines', 'exit_status', 'correctness'])

class Program():
    """
    Program object: represents a runnable program in some programming language

    You can specify the program with its source code:
        source: source code of the program
    Or with a file on disk:
        workdir: directory where the program is stored
        name: name of the file without the extension
        ephemeral: if True, the file will be deleted when Program is destroyed

    If both specifications are set, workdir/name.ext be overwritten with the source.

    Whichever specification you use, you also have to specify the language:
        language: programming language of the program
    """

    def __init__(self, source=None, name=None, language='C++', 
                       workdir=None, ephemeral=False):
        self.language = language_(language)
        self.term = Terminal()
        
        self.name = name or str(uuid4())
        
        if workdir:
            self.workdir = Path(workdir)
            self.ephemeral = ephemeral
        else:
            self.workdir = Path(__file__).parent / 'programs'
            self.ephemeral = True

        if source:
            self.language.write_source(self.workdir, self.name, source)
        else:
            source = self.language.read_source(self.workdir, self.name)

        self.stdout, self.exitstatus = self.language.build(self.workdir, self.name)

        # Please send your opinions on 'not not' vs 'bool()' to dont@vadim.me
        self.compile_error = not not self.exitstatus

    def __lt__(self, other):
        return self.name < other.name

    def read(self):
        """Obtain the source code of the program"""

        return self.language.read_source(self.workdir, self.name)

    def run(self, input_lines=[], force=True):
        """
        Run the program and capture its output

        If 'input_lines' are specified, they will be sent to stdin.
        If exit status is non-zero, an AssertionError will be raised.
        Otherwise, a list of output lines will be returned.

        Use 'force=True' to skip the exit status check.
        Raw results will always be stored in `program.stdout` and `program.exitstatus` attributes
        """

        self.stdout, self.exitstatus = self.language.run(self.workdir, self.name, input_lines)
        assert force or not self.exitstatus, f'Exit status {self.exitstatus}'
        return self.term.emulate(self.stdout)
    
    def spawn(self, delimiter='\n'):
        """
        Launch the program and get a process object to communicate with it interactively
        """

        process = self.language.spawn(self.workdir, self.name)
        return Agent(self, process, delimiter=delimiter)

    def test(self, test_cases, force=True):
        """
        Test the program against a list of input output pairs

        If 'force=True', program outputs will be checked even if the exit status is non-zero
        If 'cache=True', all the test logs will be stored in `program.test_runs` attribute
        """

        test_runs = []

        for input_lines, expected_output_lines in test_cases:
            test_run = None

            if not self.compile_error:
                try:
                    output_lines = self.run(input_lines, force=force)
                    test_run = TestRun(input_lines, expected_output_lines, 
                                       output_lines, self.exitstatus,
                                       correctness(expected_output_lines, output_lines))          
                except AssertionError:
                    pass

            if not test_run:
                test_run = TestRun(input_lines, expected_output_lines, 
                                   [], self.exitstatus, 0)

            test_runs.append(test_run)

        self.avg_score = mean([run.correctness for run in test_runs])
        self.pass_rate = mean([int(run.correctness == 1) for run in test_runs])

        return test_runs

    def save(self, path):
        self.language.copy_source(self.workdir, self.name, path)

    def __del__(self):
        if self.ephemeral:
            self.language.cleanup(self.workdir, self.name)