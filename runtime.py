import sys
from typing import Any

VERSION = "0.9.0a1"


def run_file(fp: str) -> None:
    raise NotImplementedError


def repl() -> None:
    print(f"PyLamina v{VERSION} {{Python {sys.version}}}\n")
    i = 0

    while True:
        in_ = input(f" IN[{i}] > ")
        out = run_oneline(in_)
        if out is not None:
            print(f"OUT[{i}] > \n{out}")
        i += 1


def run_oneline(code: str) -> Any: return 114514
    # raise NotImplementedError
