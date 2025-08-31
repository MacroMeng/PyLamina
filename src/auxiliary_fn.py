import sys


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


def is_block_start(ln: str) -> bool:
    """
    判断某一行是否为代码块的开始

    :param ln: 要判断的行字符串
    :return: 是否为代码块的开始
    """
    for i in ("if ", "for ", "while "):
        if _full_start_with(ln, i) and ln.rstrip()[-1] == "{":
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


def _full_start_with(ln: str, prefix: str) -> bool:
    return ln[:len(prefix)] == prefix
