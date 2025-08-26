import sys
import runtime


cmd_args = sys.argv
if len(cmd_args) == 2:
    runtime.run_file(cmd_args[1])
elif len(cmd_args) == 1:
    runtime.repl()
else:
    print("Usage: pylamina.py [file_path]\n"
          "    No arguments: Enter REPL mode\n"
          "    With arguments: Run from the Lamina source code")
    sys.exit(1)
