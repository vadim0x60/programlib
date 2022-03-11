from pathlib import Path
import subprocess
from uuid import uuid4
from statistics import mean

class Language:
    """
    Language object: describes how programs are compiled and run in a particular language
    """

    def __init__(self, build_cmd, run_cmd, source, artefacts) -> None:
        self.build_cmd = build_cmd
        self.run_cmd = run_cmd
        self.source = source
        self.artefacts = artefacts

    def build(self, workdir, name, allow_stderr=False):
        if self.build_cmd:
            completed_process = subprocess.run(self.build_cmd.format(name=name), capture_output=True, 
                                               cwd=workdir, shell=True)
            assert allow_stderr or not completed_process.stderr, completed_process.stderr

    def run(self, workdir, name, input_lines=[], allow_stderr=False):
        completed_process = subprocess.run(self.run_cmd.format(name=name), 
                                           capture_output=True, 
                                           cwd=workdir, 
                                           input='\n'.join(input_lines).encode(), 
                                           shell=True)
        assert allow_stderr or not completed_process.stderr, completed_process.stderr
        self.stdout, self.stderr = completed_process.stdout.decode(), completed_process.stderr.decode()
        return self.stdout.split('\n')

    def write_source(self, workdir, name, source):
        with open(workdir / self.source.format(name=name), 'w') as f:
            f.write(source)

    def cleanup(self, workdir, name):
        (workdir / self.source.format(name=name)).unlink()
        for artefact in self.artefacts:
            (workdir / artefact.format(name=name)).unlink()

languages = {
    'C++': Language(
        build_cmd='g++ {name}.cpp -o {name}',
        run_cmd='./{name}',
        source='{name}.cpp',
        artefacts=['{name}']
    ),
    'Python': Language(
        build_cmd=None,
        run_cmd='python3 {name}',
        source='{name}.py',
        artefacts=[]
    ),
    'Java': Language(
        build_cmd='javac {name}.java',
        run_cmd='java {name}',
        source='{name}.java',
        artefacts=['{name}.class']
    ),
    'Ruby': Language(
        build_cmd=None,
        run_cmd='ruby {name}.rb',
        source='{name}.rb',
        artefacts=[]
    ),
    'Rust': Language(
        build_cmd='rustc {name}.rs',
        run_cmd='./{name}',
        source='{name}.rs',
        artefacts=['{name}']
    ),
    'Go': Language(
        build_cmd=None,
        run_cmd='go run {name}.go',
        source='{name}.go',
        artefacts=[]
    ),
    'Haskell': Language(
        build_cmd=None,
        run_cmd='runhaskell {name}.hs',
        source='{name}.hs',
        artefacts=[]
    ),
    'Scala': Language(
        build_cmd=None,
        run_cmd='scala {name}.scala',
        source='{name}.scala',
        artefacts=[]
    ),
    'Kotlin': Language(
        build_cmd='kotlinc {name}.kt',
        run_cmd='java {name}',
        source='{name}.kt',
        artefacts=['{name}.class']
    ),
    'PHP': Language(
        build_cmd=None,
        run_cmd='php {name}.php',
        source='{name}.php',
        artefacts=[]
    ),
    'C#': Language(
        build_cmd='mcs {name}.cs',
        run_cmd='mono {name}.exe',
        source='{name}.cs',
        artefacts=['{name}.exe']
    ),
    'Swift': Language(
        build_cmd=None,
        run_cmd='swift {name}.swift',
        source='{name}.swift',
        artefacts=[]
    ),
    'D': Language(
        build_cmd=None,
        run_cmd='dmd -of{name} {name}.d',
        source='{name}.d',
        artefacts=['{name}.o']
    ),
    'Julia': Language(
        build_cmd=None,
        run_cmd='julia {name}.jl',
        source='{name}.jl',
        artefacts=[]
    ),
    'Clojure': Language(
        build_cmd=None,
        run_cmd='clj -M {name}.clj',
        source='{name}.clj',
        artefacts=[]
    ),
    'Elixir': Language(
        build_cmd=None,
        run_cmd='elixir {name}.ex',
        source='{name}.ex',
        artefacts=[]
    ),
    'Erlang': Language(
        build_cmd=None,
        run_cmd='erl -noshell -s {name} main -s init stop',
        source='{name}.erl',
        artefacts=[]
    )
}

def correctness(expected_outputs, outputs):
    outputs = outputs[:len(expected_outputs)]

    return mean(int(expected_line == actual_line) 
                for expected_line, actual_line 
                in zip(expected_outputs, outputs))

class Program():
    """
    Program object: represents a runnable program in some programming language
    """

    def __init__(self, source, name=None, language='C++', workdir=Path(__name__).parent / 'programs', allow_stderr=False):
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

    def __del__(self):
        self.language.cleanup(self.workdir, self.name)