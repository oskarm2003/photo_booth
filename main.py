from sys import path as sys_path
from sys import argv
from os import path as os_path

sys_path.append(os_path.join(sys_path[0],'utils'))

from session_manager import Session
from display_view import View


video, resolution, save_path = 0, (2560,1440), './saved'

# handle script parameters
for arg in argv:

    if arg == '--help':
        print('\t--video=[int or str] - specify the source of the video:\n\t\t0 - first system camera\n\t\t1 - secondary system camera\n\t\tstr - path to video file\n')
        print('\t--resolution=[intxint] - specify the resolution of displayed video\n\t\texample: --resolution=320x180\n')
        print('\t--save-path=[str] - specify the path to which the photos will be saved\n')
        exit()
    
    match arg.split('=')[0]:
        
        case '--video':
            video = arg.split('=')[1]
        
        case '--resolution':
            tmp = arg.split('='[1]).split('x')
            resolution = (tmp[0],tmp[1])
        
        case '--save_path':
            save_path = arg.split('=')[1]
        
    
session = Session(video, save_path, resolution)
session.render_view()
