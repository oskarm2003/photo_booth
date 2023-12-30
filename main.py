from sys import path as sys_path
from sys import argv
from os import path as os_path
from ctypes import windll
from os import mkdir

sys_path.append(os_path.join(sys_path[0],'utils'))

from session_manager import Session
from printer_usage import printer_selection

user32 = windll.user32
user32.SetProcessDPIAware()

video = 0
resolution = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
save_path = './saved'
printer_name = None
fullscreen = True
frame_delay = 5
output_height = None
rotate_output = False

if not os_path.exists('./_cache'):
    mkdir('./_cache')

# handle script parameters
for arg in argv:

    if arg == '--help':
        print('script parameters:')
        print('\t--video=[int or str] - specify the source of the video:\n\t\t0 - first system camera\n\t\t1 - secondary system camera\n\t\tstr - path to video file')
        print('\t--resolution=[intxint] - specify the resolution of displayed video\n\t\texample: --resolution=320x180')
        print('\t--output-height=[int] - specify the height in pixels of the output file that is being created. The width is dynamically calculated')
        print('\t--save-path=[str] - specify the path to which the photos will be saved')
        print('\t--rotate-output - if enabled the output photo will be rotated by 90 degrees')
        print('\t--printer-name=[str] - specify the name of the printer that will print the photos')
        print('\t--frame-delay=int - number of miliseconds awaited between frames during session')
        print("\t--no-fullscreen - don't display the view in fullscreen mode")
        print('\ncontrols:')
        print('\tq - quit. Halt the script')
        print('\tspace - response to session requests')
        print('\ta - abort current action and return to idle state')
        exit()
    
    match arg.split('=')[0]:
        
        case '--video':
            video = arg.split('=')[1]
        
        case '--resolution':
            tmp = arg.split('=')[1].split('x')
            resolution = (int(tmp[0]),int(tmp[1]))
            print(resolution)
        
        case '--save-path':
            save_path = arg.split('=')[1]

        case '--printer-name':
            printer_name = arg.split('=')[1]
        
        case '--no-fullscreen':
            fullscreen = False

        case '--frame-delay':
            frame_delay = arg.split('=')[1]
        
        case '--output-height':
            output_height = int(arg.split('=')[1])

        case '--rotate-output':
            rotate_output = True


# canceled functionality
# if printer_name is None:
#     print('\nno printer is selected, please choose one\n')
#     printer_name = printer_selection()

print('\npress q to exit\nopening...')
session = Session(video, rotate_output=rotate_output, output_file_height=output_height, printer_name=printer_name, save_path=save_path, resolution=resolution, fullscreen=fullscreen, target_frame_delay=frame_delay)
session.render_view()
