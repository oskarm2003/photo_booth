from os import startfile
from platform import system
from subprocess import Popen, PIPE

def print_file(filepath):
    
    if system == 'Linux':
        0
        # TODO
    
    elif system == 'Windows':
        print(filepath)
        startfile(filepath, 'print')