from typing import Any, NoReturn
from fractions import Fraction
from decimal import Decimal

from src import helper
from src.helper import CodeType as CodeT


VERSION = "0.9.0pa1"
VERSION_DETAIL = helper.generate_version_detail(VERSION)
REPL_WELCOME_MSG = helper.repl_welcome_msg(VERSION_DETAIL)
env = {"__version__": VERSION,
       "__version_detail__": VERSION_DETAIL}
exec("from cmath import *\n"
     "from fractions import Fraction\n"
     "from decimal import Decimal", env)  # 数学库


def run_file(fp: str) -> None:
    """运行单个.lm文件"""
    with open(fp, "r", encoding="utf-8") as f:
        code_lines = f.readlines()

    tmp = ""  # 临时存储代码块
    looking_for_block_end = False
    for i, c in enumerate(code_lines):
        if not c.strip():
            continue  # 跳过空白行

        try:
            next_ln = code_lines[i + 1]
        except IndexError:
            next_ln = ""
        if helper.is_block_start(c, next_ln):
            tmp += c
            looking_for_block_end = True
            continue

        if looking_for_block_end:
            if c.strip() == "}":
                looking_for_block_end = False
                tmp += c
                run(tmp, code_type=CodeT.STATEMENT_BLOCK)
                tmp = ""
                continue
            else:
                tmp += c
        else:
            run(c, code_type=CodeT.NORMAL)


def repl() -> NoReturn:
    """PyLamina的REPL"""
    print(REPL_WELCOME_MSG)
    i = 0

    while True:
        in_ = input(f" IN[{i}] > ")
        while True:
            if not helper.need_next_line(in_):
                break

            if in_.endswith("\\"):  # 去除“\”续行符
                in_ = in_[:-1]

            # 补全前面的空行，加入一个“|”提示用户
            in_ += " " + input(" " * (len(f" IN[{i}] > ") - 2) + "| ")

        out = run(in_, code_type=CodeT.REPL)

        print(f"OUT[{i}] >")
        if out is not None:
            if isinstance(out, (Decimal, Fraction)):
                print(f"{out}")  # 隐藏Decimal, Fraction的__repl__结果中的类名
            else:
                print(f"{out!r}")

        i += 1


def run(code: str, code_type: CodeT = CodeT.NORMAL) -> Any:
    """
    运行Lamina代码

    :param code: 要运行的代码
    :param code_type: 代码类型，详见CodeType的docstring
    :return: 表达式的值（如果非None且是表达式）
    """
    global env

    if code in (":exit", ":quit", ":q"):  # 退出检测
        exit(0)

    code = helper.translate_to_py(code)
    return helper.direct_run(code, env, code_type)
