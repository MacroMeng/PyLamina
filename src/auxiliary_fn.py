import sys


def need_next_line(line: str) -> bool:
    """判断是否需要下一行输入"""
    l_brackets_count = [
        line.count(char) for char in ("(", "[", "{")
    ]
    r_brackets_count = [
        line.count(char) for char in (")", "]", "}")
    ]
    return l_brackets_count != r_brackets_count or line.endswith("\\")


def generate_version_detail(version: str) -> str:
    """生成版本详细信息"""
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
