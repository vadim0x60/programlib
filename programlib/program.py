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

    def __init__(self, source, name=None, language='C++', workdir=Path(__file__).parent / 'programs', allow_stderr=False):
        if isinstance(language, str):
            self.language = languages[language]
        else:
            self.language = language

        self.workdir = workdir
        self.name = name or str(uuid4())
        self.allow_stderr = allow_stderr
        
        self.language.write_source(self.workdir, self.name, source)
        self.language.build(self.workdir, self.name, allow_stderr=self.allow_stderr)

    def __lt__(self, other):
        return self.name < other.name

    def run(self, input_lines=[]):
        return self.language.run(self.workdir, self.name, input_lines, allow_stderr=self.allow_stderr)

    def score(self, test_cases):
        test_results = [correctness(output_lines, self.run(input_lines)) for input_lines, output_lines in test_cases]
        return sum(test_results) / len(test_results)

    def save(self, path):
        self.language.copy_source(self.workdir, self.name, path)

    def __del__(self):
        self.language.cleanup(self.workdir, self.name)