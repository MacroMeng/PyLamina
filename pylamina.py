import sys
import runtime
import argparse

parser = argparse.ArgumentParser(description="Lamina Interpreter", epilog="With no arguments, enter REPL mode")
parser.add_argument('file_path', nargs='?', default=None, help="Run from the Lamina source code")
parser.add_argument('-v', '--version', action="store_true", help='Show Lamina version')
args = parser.parse_args()

if not args._get_args():
    runtime.repl()
if args.version:
    print(f"PyLamina v{runtime.VERSION} {{Python {sys.version}}}\n")
    sys.exit(0)
if args.file_path:
    runtime.run_file(args.file_path) 
