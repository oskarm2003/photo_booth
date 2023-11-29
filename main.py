from sys import path as sys_path
from os import path as os_path

sys_path.append(os_path.join(sys_path[0],'utils'))

from session_manager import Session
from display_view import View

session = Session('./assets/templates/video2.mp4')
session.render_view()
# view = View('./assets/templates/video2.mp4')
# print(view)