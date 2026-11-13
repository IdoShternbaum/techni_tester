import argparse
import sys

from compile import Compile
from test_runner import TestRunner, find_executable


def color(text, code):
    if not sys.stdout.isatty():
        return text
    if sys.platform == "win32":
        import ctypes
        kernel = ctypes.windll.kernel32
        handle = kernel.GetStdHandle(-11)
        mode = ctypes.c_uint()
        if not kernel.GetConsoleMode(handle, ctypes.byref(mode)) or not kernel.SetConsoleMode(handle, mode.value | 4):
            return text
    return f"\033[{code}m{text}\033[0m"


def show_results(results):
    print("\nTest results")
    print("------------")
    for result in results:
        label = color("PASS", "32") if result["passed"] else color("FAIL", "31")
        print(f"  [{label}] {result['name']} ({result['file']})")
        if not result["passed"]:
            if "reason" in result:
                print(f"         {result['reason']}")
            else:
                print(f"         Expected: {result['expected']!r}")
                print(f"         Actual:   {result['actual']!r}")
                if result["returncode"]:
                    print(f"         Exit code: {result['returncode']}")
                if result["stderr"]:
                    print(f"         stderr: {result['stderr']!r}")
    passed = sum(result["passed"] for result in results)
    print(f"\n{len(results)} tests: {passed} passed, {len(results) - passed} failed")
    return passed == len(results)


def main():
    parser = argparse.ArgumentParser(description="Build a CMake project before testing it.")
    parser.add_argument("project", nargs="?", default=".", help="project directory (default: current directory)")
    parser.add_argument("--executable", help="executable to test if the build folder contains multiple programs")
    args = parser.parse_args()

    try:
        build = Compile(args.project)
        result = build.result
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    print("Build succeeded." if result.returncode == 0 else "Build failed.")
    if result.returncode != 0:
        return result.returncode

    try:
        executable = find_executable(build.cmake_debug, args.executable)
        results = TestRunner(build.proj_path, executable).run()
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0 if show_results(results) else 1


if __name__ == "__main__":
    sys.exit(main())
