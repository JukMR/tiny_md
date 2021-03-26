import subprocess
import sys


def run_debug(number, bash_cmd_list):
    for i in range(number):
        bashCmd = bash_cmd_list
        process = subprocess.Popen(bashCmd, shell=True,)
        output, error = process.communicate()
        if (error is not None):
            print(f"The output is:{output}. The errors are:{error}")
            sys.exit("An error has ocurred")


command = ["make && ./tiny_md"]
run_debug(2, command)
