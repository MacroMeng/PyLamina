import sys
from src import runtime
import argparse


parser = argparse.ArgumentParser(description="Lamina Interpreter", epilog="With no arguments, enter REPL mode")
parser.add_argument('file_path', nargs='?', default=None, help="Run from the Lamina source code")
parser.add_argument('-v', '--version', action="store_true", help='Show Lamina version')
args = parser.parse_args()

if not args._get_args():  # 没有参数时进入REPL模式
    runtime.repl()
if args.version:  # 显示版本信息
    print(runtime.VERSION_DETAIL)
    sys.exit(0)
if args.file_path:  # 运行文件
    runtime.run_file(args.file_path) 
