import sys
import traceback
from enum import Enum
import re
from typing import Any


class CodeType(Enum):
    """
    传递给runtime.run()的代码类型
    """

    REPL = "REPL"  # REPL模式
    STATEMENT_BLOCK = "STATEMENT_BLOCK"  # 语句块，需要强制用exec执行
    NORMAL = "NORMAL"  # 普通代码，正常情况下优先使用exec执行


def need_next_line(line: str) -> bool:
    """
    判断是否需要下一行输入

    :param line: 要判断的行字符串
    :return: 是否需要下一行输入
    """
    l_brackets_count = [
        line.count(char) for char in ("(", "[", "{")
    ]
    r_brackets_count = [
        line.count(char) for char in (")", "]", "}")
    ]
    return l_brackets_count != r_brackets_count or line.endswith("\\")


def generate_version_detail(version: str) -> str:
    """
    生成版本详细信息

    :param version: 版本字符串
    :return: 版本详细信息字符串
    """
    if "pa" in version:
        pre, suf = version.split("pa")
        res = f"PyLamina v{pre} Pre-Alpha {suf}"
    elif "a" in version:
        pre, suf = version.split("a")
        res = f"PyLamina v{pre} Alpha {suf}"
    elif "b" in version:
        pre, suf = version.split("b")
        res = f"PyLamina v{pre} Beta {suf}"
    elif "rc" in version:
        pre, suf = version.split("rc")
        res = f"PyLamina v{pre} Release Candidate {suf}"
    else:
        res = f"PyLamina v{version}"

    res += f" {{Python v{sys.version}}}"
    return res


def is_block_start(ln: str, next_ln: str) -> bool:
    """
    判断某一行是否为代码块的开始

    :param ln: 要判断的行字符串
    :param next_ln: 下一行字符串
    :return: 是否为代码块的开始
    """
    for i in ("if ", "for ", "while "):
        if (ln.startswith(i) and
                (ln.rstrip()[-1] == "{" or next_ln.strip() == "{")):
            # 这一行的开始是if/for/while 且 以{结束或下一行是{，参见LSR002
            return True
    return False


def repl_welcome_msg(version: str) -> str:
    """
    生成REPL欢迎消息

    :return: REPL欢迎消息字符串
    """
    res = r"""
███████\            ██\                               ██\                     
██  __██\           ██ |                              \_\|                    
██ |  ██ |██\   ██\ ██ |       ██████\  ██████\████\  ██\ ███████\   ██████\  
███████ \|██ |  ██ |██ |       \____██\ ██\ _██\ _██\ ██ |██\ __██\  \____██\ 
██\ ___\/ ██ |  ██ |██ |       ███████ |██ / ██ / ██ |██ |██ |  ██ | ███████ |
██ |      ██ |  ██ |██ |      ██  __██ |██ | ██ | ██ |██ |██ |  ██ |██  __██ |
██ |      \███████ |████████\ \███████ |██ | ██ | ██ |██ |██ |  ██ |\███████ |
\_\|       \____██ |\_______\| \______\|\_\| \_\| \_\|\__|\_\|  \_\| \______\|
          ██\   ██ |                                                          
          \██████ \|                                                          
           \______/                                                           
"""
    res += version + "\n"
    res += "If you find an error while using PyLamina, please submit an issue on GitHub.\n"
    res += "Type :exit, :quit or :q to exit.\n"

    return res


def translate_to_py(code: str) -> str:
    """
    将Lamina代码转换为Python代码执行

    :param code: Lamina代码
    :return: 翻译后的Python代码
    """
    code = re.sub(r"(\d+)/(\d+)", r"Fraction(\1, \2)", code)  # 精确分数
    code = re.sub(r"(\d*)\.(\d+)", r"Decimal('\1.\2')", code)  # 精确小数
    code = re.sub(r"//.*$", "", code)  # 屏蔽注释
    if re.match(r"var\s*(\w+)\s*=\s*(\w+)", code):
        code = re.sub(r"var\s*(\w+)\s*=\s*(\w+)", r"\1=\2", code)  # 变量定义

    if code.strip().count("\n") > 0:
        # 多行代码（语句块）处理
        code = re.sub(r"if\s+\((\w+)\)\s+\{(.+)}",  # if  # TODO: FIX IT
                      "if \\1:\n\\2",  # 假设\2有缩进
                      code,)

    return code


def direct_run(code: str,
               env: dict,
               code_type: CodeType = CodeType.NORMAL) -> Any:
    """
    补充runtime.run()中运行代码的逻辑

    :param code: Lamina代码
    :param env: 环境变量
    :param code_type: 代码类型，详见CodeType的docstring
    :return: 表达式的值（如果非None且是表达式）
    """
    try:
        if code_type == CodeType.REPL:
            try: return eval(code, env)
            except SyntaxError: exec(code, env)
        else:
            exec(code, env)
    except Exception as e:
        traceback.print_exception(e)
