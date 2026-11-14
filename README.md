# Techni Tester

**Build your C project, run your own tests, and catch mistakes before submitting to Gradescope.**

Techni Tester is a Python command-line tool for students working with CMake projects. Run it from your project folder to build your program and compare its output against your test cases.

```text
Test results
------------
  [PASS] addition (student_tests.json)
  [FAIL] zero input (student_tests.json)
         Expected: '0\n'
         Actual:   '1\n'

2 tests: 1 passed, 1 failed
```

## Getting started

### 1. Install

You need Python 3.9 or newer, pip, and a CMake project that has already been configured with a working C compiler.

If you are using PyCharm's terminal, it may activate the project's virtual environment automatically. Run `deactivate` first so that `--user` installs the command for your user account. If the virtual environment activates again when you open a terminal, disable **Activate virtualenv** in PyCharm's terminal settings or use a terminal outside PyCharm.

From this repository's directory, run:

```powershell
python -m pip install --user .
```

The `--user` option installs the tool for your Windows user account instead of system-wide. Python's user scripts directory must be on your `PATH` for the `techni-tester` command to work. If pip reports that the scripts directory is not on `PATH`, add the directory it names to your user `PATH` and restart your terminal.

Alternatively, to install only inside an active virtual environment, omit `--user` and run `python -m pip install .`. The command will be available while that environment is active.

For development, use `python -m pip install --user -e .` instead. The `-e` option makes the installation editable, so changes to the Python source are available without reinstalling.

### 2. Add your tests

Create a `tests` folder in your project and add a JSON file, for example `student_tests.json`:

```json
{
  "tests": [
    {
      "name": "addition",
      "input": "2 3\n",
      "output": "5\n"
    }
  ]
}
```

Each test has a name, the text sent to standard input, and the expected standard output. Use `\n` for a newline. Output must match exactly, including spaces and trailing newlines.

Your project should look like this:

```text
my-project/
├── CMakeLists.txt
├── main.c
├── cmake-build-debug/       # Existing CMake build directory
└── tests/
    └── student_tests.json
```

The tool validates every `.json` file directly inside `tests`. Each file must contain a `tests` array whose entries have string `name`, `input`, and `output` fields.

### 3. Run

From the project directory, including in CLion's terminal:

```powershell
techni-tester
```

The tool builds the project, runs each test, and shows a summary. A test also fails if the program exits with an error or runs for more than five seconds.

## Command options

Specify a project directory instead of using the current directory:

```powershell
techni-tester path\to\project
```

If the build directory contains more than one executable, select the one to test:

```powershell
techni-tester --executable path\to\program.exe
```

Run `techni-tester --help` for the available options. The current version expects an existing `cmake-build-debug` directory and a valid CMake path in its cache.
