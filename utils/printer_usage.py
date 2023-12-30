from os import path as os_path
from sys import path as sys_path
from platform import system
import subprocess

def print_file(relative_filepath, printer_name):

    # prepare the file path
    if relative_filepath[0] == '.':
        relative_filepath = relative_filepath[2:]

    tmp = relative_filepath.split('/')
    if len(tmp) == 1:
        tmp = relative_filepath.split('\\')
    
    new_path = ''
    for el in tmp:
        new_path = os_path.join(new_path,el)

    filepath = os_path.join(sys_path[0],new_path)
    os_name = system()

    # print on Linux
    if os_name == 'Linux':
        # in progress
        0
    
    # print on Windows
    elif os_name == 'Windows':
        # cmd = f'print /d:\\\\%COMPUTERNAME%\\"{printer_name}" {filepath}'
        cmd = f'mspaint /pt {filepath}'

        print(cmd)
        subprocess.run(cmd, shell=True)

    
def printer_selection():

    os_name = system()
    printers = []

    # get printers on Windows
    if os_name == 'Windows':
        result = subprocess.check_output("wmic printer get Name", shell=True, text=True)
        result = result.split('\n')[1:]

        for el in result:
            if not el == '':
                printers.append(el.strip())
        
    # get printers on Linux
    elif os_name == 'Linux':
        # in progress
        0
    
    # display the menu to let user select the printer
    print('----- detected printers -----')
    for i in range(len(printers)):
        print(f'({i+1})',printers[i])
    
    while True:
        selected = input('\nchoose the number of the printer: ')

        try:
            if not 0 < int(selected) <= len(printers):
                raise Exception('wrong input')    
            return printers[int(selected) - 1]
        except:
            print('invalid input - insert number between 1 and '+str(len(printers)))