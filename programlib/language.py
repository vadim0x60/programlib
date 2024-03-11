import pexpect
import shutil
import os
from pathlib import Path
from programlib.pexpectutil import pexpect_exceptions

class Language:
    """
    Language object: describes how programs are compiled and run in a particular language
    """

    def __init__(self, build_cmd, run_cmd, source, artefacts, name='custom') -> None:
        self.build_cmd = build_cmd
        self.run_cmd = run_cmd
        self.source = source
        self.artefacts = artefacts
        self.name = name

    def build(self, name):
        if self.build_cmd:
            stdout, status = pexpect.run(self.build_cmd.format(name=name), 
                                         withexitstatus=True, echo=False)
            return stdout.decode(), status
        else:
            return '', ''

    @pexpect_exceptions
    def run(self, name, input_lines=[]):
        child = self.spawn(name)
        for line in input_lines:
            child.sendline(line)
        output = child.read()
        child.close()
        return output.decode(), child.exitstatus
    
    def spawn(self, name):
        child = pexpect.spawn(self.run_cmd.format(name=name))
        child.setecho(False)
        return child

    def write_source(self, name, source):
        with open(self.source.format(name=name), 'w') as f:
            f.write(source)

    def read_source(self, name):
        with open(self.source.format(name=name), 'r') as f:
            return f.read()

    def copy_source(self, name, dest):
        shutil.copy(self.source.format(name=name), dest)

    def cleanup(self, name):
        for path in [self.source] + self.artefacts:
            try:
                Path(path.format(name=name)).unlink()
            except FileNotFoundError:
                pass

    def __repr__(self) -> str:
        return self.name

languages = {
    'C++': Language(
        build_cmd='g++ {name}.cpp -o {name}',
        run_cmd='./{name}',
        source='{name}.cpp',
        artefacts=['{name}'],
        name='C++'
    ),
    'Python': Language(
        build_cmd=None,
        run_cmd='python3 {name}.py',
        source='{name}.py',
        artefacts=[],
        name='Python'
    ),
    'Java': Language(
        build_cmd='javac {name}.java',
        run_cmd='java {name}',
        source='{name}.java',
        artefacts=['{name}.class'],
        name='Java'
    ),
    'Ruby': Language(
        build_cmd=None,
        run_cmd='ruby {name}.rb',
        source='{name}.rb',
        artefacts=[],
        name='Ruby'
    ),
    'Rust': Language(
        build_cmd='rustc {name}.rs',
        run_cmd='./{name}',
        source='{name}.rs',
        artefacts=['{name}'],
        name='Rust'
    ),
    'Go': Language(
        build_cmd=None,
        run_cmd='go run {name}.go',
        source='{name}.go',
        artefacts=[],
        name='Go'
    ),
    'Haskell': Language(
        build_cmd=None,
        run_cmd='runhaskell {name}.hs',
        source='{name}.hs',
        artefacts=[],
        name='Haskell'
    ),
    'Scala': Language(
        build_cmd=None,
        run_cmd='scala {name}.scala',
        source='{name}.scala',
        artefacts=[],
        name='Scala'
    ),
    'Kotlin': Language(
        build_cmd='kotlinc {name}.kt',
        run_cmd='java {name}',
        source='{name}.kt',
        artefacts=['{name}.class'],
        name='Kotlin'
    ),
    'PHP': Language(
        build_cmd=None,
        run_cmd='php {name}.php',
        source='{name}.php',
        artefacts=[],
        name='PHP'
    ),
    'C#': Language(
        build_cmd='mcs {name}.cs',
        run_cmd='mono {name}.exe',
        source='{name}.cs',
        artefacts=['{name}.exe'],
        name='C#'
    ),
    'Swift': Language(
        build_cmd=None,
        run_cmd='swift {name}.swift',
        source='{name}.swift',
        artefacts=[],
        name='Swift'
    ),
    'D': Language(
        build_cmd=None,
        run_cmd='dmd -of{name} {name}.d',
        source='{name}.d',
        artefacts=['{name}.o'],
        name='D'
    ),
    'Julia': Language(
        build_cmd=None,
        run_cmd='julia {name}.jl',
        source='{name}.jl',
        artefacts=[],
        name='Julia'
    ),
    'Clojure': Language(
        build_cmd=None,
        run_cmd='clj -M {name}.clj',
        source='{name}.clj',
        artefacts=[],
        name='Clojure'
    ),
    'Elixir': Language(
        build_cmd=None,
        run_cmd='elixir {name}.ex',
        source='{name}.ex',
        artefacts=[],
        name='Elixir'
    ),
    'Erlang': Language(
        build_cmd=None,
        run_cmd='erl -noshell -s {name} main -s init stop',
        source='{name}.erl',
        artefacts=[],
        name='Erlang'
    )
}

def language_(language):
    if isinstance(language, Language):
        return language
    else:
        return languages[language]