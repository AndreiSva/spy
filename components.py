import os
import getpass
import sys

def export(args):
    if len(args) > 0:
        os.environ[args[1].split("=")[0]] = args[1].split("=")[1]
    return 0

def cd(args):
    if len(args) <= 1:
        os.chdir(f"/home/{getpass.getuser()}")
    else:
        try:
            os.chdir(args[1])
        except FileNotFoundError:
            print(f"spy: cd: no such directory exists")

def exit(args):
    sys.exit(0)

components_list = [export, cd, exit]
