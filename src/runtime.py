import traceback
from typing import Any, NoReturn
import re
from fractions import Fraction
from decimal import Decimal

from src import auxiliary_fn as afn


VERSION = "0.9.0pa1"
VERSION_DETAIL = afn.generate_version_detail(VERSION)
env = {"__version__": VERSION,
       "__version_detail__": VERSION_DETAIL}
exec("from cmath import *\n"
     "from fractions import Fraction\n"
     "from decimal import Decimal", env)  # 数学库


def run_file(fp: str) -> None:
    """运行单个.lm文件"""
    raise NotImplementedError


def repl() -> NoReturn:
    """PyLamina的REPL"""
    print(VERSION_DETAIL)
    i = 0

    while True:
        in_ = input(f" IN[{i}] > ")
        while True:
            if not afn.need_next_line(in_):
                break

            if in_.endswith("\\"):  # 去除“\”续行符
                in_ = in_[:-1]

            # 补全前面的空行，加入一个“|”提示用户
            in_ += " " + input(" " * (len(f" IN[{i}] > ") - 2) + "| ")

        out = run(in_)

        print(f"OUT[{i}] >")
        if out is not None:
            if isinstance(out, (Decimal, Fraction)):
                print(f"{out}")  # 隐藏Decimal, Fraction的__repl__结果中的类名
            else:
                print(f"{out!r}")

        i += 1


def run(code: str, force_exec: bool = False) -> Any:
    """
    运行单行Lamina代码

    :param code: 要运行的代码
    :param force_exec: 是否强制作为语句运行
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
        if is_expression and not force_exec:
            return eval(code, env)
        else:
            exec(code, env)
    except Exception as e:
        traceback.print_exception(e)
        print("TIP: 若认为此问题为PyLamina解释器Bug，请提交Issue。"
              if "a" in VERSION or "b" in VERSION else "")  # 仅开发版本提示
