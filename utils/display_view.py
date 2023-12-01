import cv2 as cv
from PIL import ImageFont, ImageDraw, Image
from numpy import array, ones
from sys import path as sys_path
from os import path as os_path

class View:
    
    def __init__(self, vid_source:str|int, resolution:tuple[int, int], name='Photo Booth'):

        self.vid = cv.VideoCapture(vid_source)

        self.resolution = resolution
        self.vid.set(cv.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.vid.set(cv.CAP_PROP_FRAME_HEIGHT, resolution[1])
        print()
        self.font_path = os_path.join(sys_path[0],'assets','fonts','lato.ttf')
        self.dimensions = [self.vid.get(4), self.vid.get(3)]
        self.name = name

        self.pressed_key = ''
        self.refresh(0)
        
        cv.namedWindow(self.name,cv.WINDOW_NORMAL)
        cv.setWindowProperty(self.name, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    

    # place text on the frame
    # r_pos values should be in range (-1,1) - meaning the distance from the center
    def place_text(self, text:str, r_pos:tuple[int,int]=(0,0), font_scale=125):
        

        font = ImageFont.truetype(self.font_path, font_scale)
        pil_img = Image.fromarray(self.frame)
        pil_img = pil_img.resize(self.resolution)
        draw = ImageDraw.Draw(pil_img)
        text_len = draw.textlength(text,font)
        draw.text(
            (int((self.resolution[0] - text_len)//2 * (1 + r_pos[0])),int((self.resolution[1] - font_scale)//2 * (1 + r_pos[1]))),
            text,
            font=font
        )
        
        self.frame = array(pil_img)


    # save the frame as png
    def save_frame(self, path:str):

        if not os_path.exists(path):
            cv.imwrite(path, self.frame)


    # brighten the frame
    def flash_filter(self):

        matrix = ones(self.frame.shape, dtype="uint8") * 100
        self.frame = cv.add(self.frame, matrix)


    # refresh frame and get the pressed key
    def refresh(self, delay:int):

        ret, self.frame = self.vid.read()

        if not ret:
            raise Exception('Frame: could not get the view')
        
        self.pressed_key = cv.waitKey(delay)


    # display the frame
    def display(self):

        cv.imshow(self.name, self.frame)