from statistics import mean
from uuid import uuid4
from pathlib import Path

from programlib import languages

def correctness(expected_outputs, outputs):
    outputs = outputs[:len(expected_outputs)]

    return mean(int(expected_line == actual_line) 
                for expected_line, actual_line 
                in zip(expected_outputs, outputs))

class Program():
    """
    Program object: represents a runnable program in some programming language
    """

    def __init__(self, source, name=None, language='C++', 
                       workdir=Path(__file__).parent / 'programs', 
                       force_build=False):
        if isinstance(language, str):
            self.language = languages[language]
        else:
            self.language = language

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

    def score(self, test_cases, force=True):
        test_results = []
        for input_lines, expected_output_lines in test_cases:
            try:
                output_lines = self.run(input_lines, force=force)
                test_results.append(correctness(expected_output_lines, output_lines))
            except AssertionError:
                test_results.append(0)
        return mean(test_results)

    def save(self, path):
        self.language.copy_source(self.workdir, self.name, path)

    def __del__(self):
        self.language.cleanup(self.workdir, self.name)