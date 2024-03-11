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
- a `save` method that will save the source code to a file at the specified path.
- a `run` method that runs the program and returns a list of strings it printed to `stdout`. You can optionally provide a list of input strings as well.
- a `spawn` method that launches the program in an interactive mode. It returns an `Agent` object with and `act` method that takes a sequence of input strings and returns a list of strings printed to `stdout` in response.
- a `test` method that takes a list of test cases. A test case is a tuple of 2 lists: the first list is the input strings, the second is the expected output strings. The method returns a full log of all test runs and updates `program.avg_score` and `program.test_pass_rate` attributes.

To use the program to process some input lines, do

```python
output_lines = program.run(input_lines)
```

To use the program as an agent in a Reinforcement Learning environment, do

```python
env = gym.make('Env-vX')
agent = program.spawn().rl(env.action_space, env.obs_space)
obs, info = env.reset()
terminated = False
truncated = False
while not (terminated or truncated):
    action = agent.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
```

See also `examples`.

Currently supported programming languages out of the box are C++, Python, Java, Clojure, Ruby, Rust, Go, Haskell, Scala, Kotlin, PHP, C#, Swift, D, Julia, Clojure, Elixir and Erlang.
See "Advanced usage" below for instructions on how to add other languages.

## Advanced usage

### Language configuration

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

`source` parameter describes the naming convention for the source file (usually `{name}.extension`). Make sure that this parameter contains a `{name}` placeholder, so that `programlib` can keep track of several source files at the same time.
`build_cmd` and `run_cmd` respectively instruct `programlib` which commands to use to compile and run the program in this language.
`artefacts` is a list of all the files produced by `build_cmd` command.
It is needed to clean up the artefacts when the program object is destroyed.

### Error handling

By default, any errors at build time or run time will lead to `RuntimeError` being raised, with 2 exceptions:
- `test` function that catches exceptions during test cases execution and marks these tests as failed.
- Setting `program.run(force=True)` or `program.test(force=True)` will make `programlib` ignore all errors.

You can check `program.stdout` and `program.exitstatus` to check the output during the last run (or, if in was never run, during build).