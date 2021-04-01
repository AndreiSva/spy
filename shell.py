#!/usr/bin/python

import os
import os.path
import sys
import select
import subprocess
import shlex
import pathlib
import readline

from components import components_list
from shellglobals import shell_vars

def parse_variables(shell_input):
    for arg_index in range(0, len(shell_input)):
        for char_index in range(0, len(shell_input[arg_index])):
            if shell_input[arg_index][0] == "\\":
                shell_input[arg_index] = shell_input[arg_index][1:len(shell_input[arg_index])]
                break
            if shell_input[arg_index][char_index] == "$": 
                second_index = 0
                for i in range(char_index, len(shell_input[arg_index])):
                    second_index = i
                    if shell_input[arg_index][i] in "/!&| ":
                        break;
                    if i == len(shell_input[arg_index]) - 1:
                        second_index+=1
                        break;
                if shell_input[arg_index][char_index + 1:second_index] in shell_vars:
                    variable_database = shell_vars
                else:
                    variable_database = os.environ
                try:
                    shell_input[arg_index] = shell_input[arg_index][0:char_index] + variable_database[shell_input[arg_index][char_index + 1:second_index]] + shell_input[arg_index][second_index:len(shell_input[arg_index])]
                except KeyError:
                    pass
    return shell_input

def parse_ps():
    ps1 = parse_variables(shell_vars["PS1"])

def main(args):
    directory = subprocess.Popen("pwd", stdout=subprocess.PIPE)
    preview = str(directory.communicate()[0].decode("utf-8"))
    # os.environ["PS1"] = f"\u001b[31m(\u001b[33m{preview[0:len(preview) - 1]}\u001b[31m)\u001b[33m -> \u001b[0m"
    # if running interactively
    if select.select([sys.stdin,],[],[],0.0)[0] != True:
        shell_input = [None]
        # shell main loop
        while True:
            directory = subprocess.Popen("pwd", stdout=subprocess.PIPE)
            # preview = str(directory.communicate()[0].decode("utf-8"))
            # os.environ["PS1"] = f"\u001b[31m(\u001b[33m{preview[0:len(preview) - 1]}\u001b[31m)\u001b[33m -> \u001b[0m"
            parse_ps()
            
            shell_input = input(shell_vars['PS1']) # .replace("\\", "^")
            shell_input = shlex.split(shell_input)
            
            # environment variable replacements
            shell_input = parse_variables(shell_input)
            match = False
            for c in components_list:
                try:
                    if c.__name__ == shell_input[0]:
                        c(shell_input)
                        match = True
                except IndexError:
                    return
            if match != True:
                try:
                    # subprocess.call(shell_input)
                    program = subprocess.Popen(shell_input)
                    program.communicate()[0]
                    os.environ["?"] = str(program.returncode)
                except FileNotFoundError:
                    print(f"spy: {shell_input[0]}: command not found")
                except KeyboardInterrupt:
                    pass
                except PermissionError:
                    print(f"spy: {shell_input[0]}: Permission Denied")
                except IndexError:
                    pass
    pass

if __name__ == "__main__":
    while True:
        try:
            main(sys.argv)
        except KeyboardInterrupt:
            print()
