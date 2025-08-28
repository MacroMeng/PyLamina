import sys
import traceback
from typing import Any
import re
from fractions import Fraction
from decimal import Decimal


VERSION = "0.9.0a1"
env = {"__version__": VERSION}
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
        while True:
            if not need_next_line(in_):
                break

            # 补全前面的空行，加入一个“|”提示用户
            in_ += " " + input(" " * (len(f" IN[{i}] > ") - 2) + "| ")

            if in_.endswith("\\"):  # 去除“\”续行符
                in_ = in_[:-1]

        out = run(in_)

        print(f"OUT[{i}] >")
        if out is not None:
            if isinstance(out, (Decimal, Fraction)):
                print(f"{out}")  # 隐藏Decimal, Fraction的__repl__结果中的类名
            else:
                print(f"{out!r}")

        i += 1


def run(code: str, force_eval: bool = False) -> Any:
    """
    运行单行Lamina代码

    :param code: 要运行的代码
    :param force_eval: 是否强制作为表达式运行
    :return: 表达式的值（如果非None且是表达式）
    """
    global env
    is_expression = True

    if code in (":exit", ":quit", ":q", ":q!"):  # 退出检测
        exit(0)

    code = re.sub(r"(\d+)/(\d+)", r"Fraction(\1, \2)", code)  # 精确分数
    code = re.sub(r"(\d*)\.(\d+)", r"Decimal('\1.\2')", code)  # 精确小数
    code = re.sub(r"//.*$", "", code)  # 屏蔽注释
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


# ====================下面为辅助函数====================
def need_next_line(line: str) -> bool:
    """判断是否需要下一行输入"""
    l_brackets_count = [
        line.count(char) for char in ("(", "[", "{")
    ]
    r_brackets_count = [
        line.count(char) for char in (")", "]", "}")
    ]
    return l_brackets_count != r_brackets_count or line.endswith("\\")
