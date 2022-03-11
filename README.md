# Programlib: programs as objects

Programlib is a tool that turns programs in any programming language into convenient Python objects, letting you run any string as a C++/Python/Clojure/etc program from a Python script.
This project is aimed to help develop automatic programming and genetic software improvement systems, though many other applications are possible.

## Installation

Programlib can be installed with

```
pip install programlib
```

However, you have to also make sure that the programming languages you want to use are installed.
By default, programlib uses command line tools that come with the programming languages, i.e. `python3` or `javac`.

## Standard usage

Create a program object with

```python
from programlib import Program
program = Program(source_code, language='C++')
```

This object has
- a `run` method that runs the program and returns a list of strings it printed to `stdout`. You can optionally provide a list of input strings as well.
- a `score` method that takes a list of test cases. A test case is a tuple of 2 lists: the first list is the input strings, the second is the expected output strings. The method returns percentage of output strings that matched expectations.

See also `example.py`.

Currently supported programming languages out of the box are C++, Python, Java, Clojure, Ruby, Rust, Go, Haskell, Scala, Kotlin, PHP, C#, Swift, D, Julia, Clojure, Elixir and Erlang.
See "Advanced usage" below for instructions on how to add other languages.

## Advanced usage

By default, program execution will fail if anything is output to `stderr` at compile or run time. 
You can override this by creating a Program object with `allow_stderr=True` argument.

When you create a program object with a language name like `language='C++'`, `programlib` retrieves an appropriate language configuration from it's database.
If you have a different opinion on how to compile or run in this language or want to use a language that is not supported out of the box, you can create your own language configuration object:

```python
from programlib import Program, Language
language = Language(
        build_cmd='g++ {name}.cpp -o {name}',
        run_cmd='./{name}',
        source='{name}.cpp',
        artefacts=['{name}']
    )
program = Program(source_code, language=language)
```

`source` parameter describe the naming convention for the source file (usually `{name}.extension`). Make sure that this parameter contains a `{name}` placeholder, so that `programlib` can keep track of several source files at the same time.
`build_cmd` and `run_cmd` respectively instruct `programlib` which commands to use to compile and run the program in this language.
`artefacts` is a list of all the files produced by `build_cmd` command.
It is needed to clean up the artefacts when the program object is destroyed.