import subprocess
import shutil

class Language:
    """
    Language object: describes how programs are compiled and run in a particular language
    """

    def __init__(self, build_cmd, run_cmd, source, artefacts) -> None:
        self.build_cmd = build_cmd
        self.run_cmd = run_cmd
        self.source = source
        self.artefacts = artefacts

    def build(self, workdir, name):
        if self.build_cmd:
            completed_process = subprocess.run(self.build_cmd.format(name=name), capture_output=True, 
                                               cwd=workdir, shell=True)
            return completed_process.stdout, completed_process.stderr
        else:
            return '', ''

    def run(self, workdir, name, input_lines=[]):
        completed_process = subprocess.run(self.run_cmd.format(name=name), 
                                           capture_output=True, 
                                           cwd=workdir, 
                                           input='\n'.join(input_lines).encode(), 
                                           shell=True)
        return completed_process.stdout.decode(), completed_process.stderr.decode()

    def write_source(self, workdir, name, source):
        with open(workdir / self.source.format(name=name), 'w') as f:
            f.write(source)

    def copy_source(self, workdir, name, dest):
        shutil.copy(workdir / self.source.format(name=name), dest)

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
        run_cmd='python3 {name}.py',
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

def language_(language):
    if isinstance(language, Language):
        return language
    else:
        return languages[language]