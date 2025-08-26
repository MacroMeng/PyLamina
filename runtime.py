import sys
from typing import Any

VERSION = "0.9.0a1"


def run_file(fp: str) -> None:
    """运行单个.lm文件"""
    raise NotImplementedError


def repl() -> None:
    """PyLamina的REPL"""
    print(f"PyLamina v{VERSION} {{Python {sys.version}}}\n")
    i = 0

    while True:
        in_ = input(f" IN[{i}] > ")
        out = run_oneline(in_)
        if out is not None:
            print(f"OUT[{i}] > \n{out}")
        i += 1


def run_oneline(code: str) -> Any:
    """运行单行Lamina代码"""
    return 114514
