import sys
import traceback
from typing import Any
import re


VERSION = "0.9.0a1"
env = {}
env.update(dict(  # 常量
    __version__=VERSION,
))
exec("from cmath import *\n"
     "from fractions import Fraction\n"
     "from decimal import Decimal", env)  # 数学库


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
    global env
    is_expression = True

    if code in (":exit", ":quit", ":q", ":q!"):  # 退出检测
        exit(0)

    code = re.sub(r"(\d+)/(\d+)", r"Fraction(\1, \2)", code)  # 精确分数
    code = re.sub(r"(\d*)\.(\d+)", r"Decimal('\1.\2')", code)  # 精确小数
    if re.match(r"var\s*(\w+)\s*=\s*(\w+)", code):
        is_expression = False
        code = re.sub(r"var\s*(\w+)\s*=\s*(\w+)", r"\1=\2", code)  # 变量定义

    try:
        if is_expression:
            return eval(code, env)
        else:
            exec(code, env)
    except Exception as e:
        traceback.print_exception(e)
        print("TIP: 若认为此问题为PyLamina解释器Bug，请提交Issue。"
              if "a" in VERSION or "b" in VERSION else "")  # 仅开发版本提示
