#!/usr/bin/python

import signal
import os
import os.path
import sys
import select
import subprocess
import shlex
import pathlib

from components import components_list

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
                shell_input[arg_index] = shell_input[arg_index][0:char_index] + os.environ[shell_input[arg_index][char_index + 1:second_index]] + shell_input[arg_index][second_index:len(shell_input[arg_index])]
    return shell_input


def main(args):
    directory = subprocess.Popen("pwd", stdout=subprocess.PIPE)
    preview = str(directory.communicate()[0].decode("utf-8"))
    os.environ["PS1"] = f"\u001b[31m(\u001b[33m{preview[0:len(preview) - 1]}\u001b[31m)\u001b[33m -> \u001b[0m"
    os.environ["0"] = "-spy"
    # if running interactively
    if select.select([sys.stdin,],[],[],0.0)[0] != True:
        shell_input = [None]
        # shell main loop
        while shell_input[0] != "exit":
            directory = subprocess.Popen("pwd", stdout=subprocess.PIPE)
            preview = str(directory.communicate()[0].decode("utf-8"))
            os.environ["PS1"] = f"\u001b[31m(\u001b[33m{preview[0:len(preview) - 1]}\u001b[31m)\u001b[33m -> \u001b[0m"
            print(os.environ['PS1'], end="")
            
            shell_input = input() # .replace("\\", "^")
            shell_input = shlex.split(shell_input)
            
            # environment variable replacements
            shell_input = parse_variables(shell_input)
            match = False 
            for c in components_list:
                if c.__name__ == shell_input[0]:
                    c(shell_input)
                    match = True
            if match != True:
                try:
                    subprocess.call(shell_input)
                except FileNotFoundError:
                    print(f"spy: {shell_input[0]}: command not found")
    pass

if __name__ == "__main__":
    main(sys.argv)
