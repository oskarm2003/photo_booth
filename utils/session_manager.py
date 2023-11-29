from datetime import datetime
from display_view import View
from photo_edit import fill_template, crop_photo
from os import rename, mkdir
from os import path as os_path


class Session:

    def __init__(self, vid_source:str|int, save_path:str='./saved'):

        self.framerate = 30
        self.state = 'idle'
        self.last_step_start_time = 0
        self.freezed_frame = None
        self.view = View(vid_source)

        # validate the save path
        if not os_path.exists(save_path):
            if save_path != './saved': 
                print('given path does not exist, saving in ./saved instead')
            self.save_path = './saved'
            if not os_path.exists('./saved'):
                mkdir('./saved')
        else:
            self.save_path = save_path

        #settings
        self.window_name = 'Photo Booth'
    

    # function for state update
    def update_state(self, state:str):
        
        allowed_states = ['idle','photo.1','photo.2','photo.3','printing']
        if not state in allowed_states:
            print('Session: unhandled state: ' + state)
            return
        
        # change framerate
        if state == 'idle':
            self.framerate = 50
        elif self.state == 'idle':
            self.framerate = 25

        self.state = state
        self.last_step_start_time = datetime.timestamp(datetime.now())


    # take the photo
    def take_photo(self):
        path = './_cache/raw'+self.state.split('.')[1]+'.jpg'
        if self.freezed_frame is None:
            self.freezed_frame = self.view.frame.copy()
            self.view.save_frame(path)
            crop_photo(path, 'crop'+self.state.split('.')[1])
            rename(path,self.save_path+'/'+str(datetime.now()).split('.')[0].replace(':','-')+'.jpg')

        # if os_path.exists(path):
            # crop_photo(path, 'ready'+self.state.split('.')[1])
        self.view.flash_filter()
    

    # create the template
    def put_together(self):

        template_url = ''

        if datetime.now().hour < 12:
            #post midnight template
            template_url = './assets/templates/post_midnight.jpg'
        else:
            #pre midnight template
            template_url = './assets/templates/pre_midnight.jpg'
        
        fill_template(
            ['./_cache/crop1.jpg','./_cache/crop2.jpg','./_cache/crop3.jpg'], 
            template_url
            )


    # manage taking photos and the countdown
    def photo_taker(self):

        seconds_passed = datetime.timestamp(datetime.now()) - self.last_step_start_time

        # move on
        if seconds_passed >= 7:

            current_photo_num = int(self.state.split('.')[1])

            if current_photo_num == 3:
                self.update_state('printing')
                self.view.place_text('printing...')
                return

            self.update_state('photo.' + str(int(self.state.split('.')[1])+1))
        
        if seconds_passed > 6:
            self.freezed_frame = None
            return 
        
        if seconds_passed >= 4.35:
            if not self.freezed_frame is None:
                self.view.frame = self.freezed_frame
            return

        if 4.25 <= seconds_passed < 4.35:
            self.take_photo()
        
        # place text with progress in the corner
        self.view.place_text(self.state.split('.')[1]+'/3', r_pos=(0.90,-0.90), font_scale=30)

        # countdown
        if seconds_passed >= 3:
            self.view.place_text('1')

        elif seconds_passed >= 2:
            self.view.place_text('2')

        elif seconds_passed >= 1:
            self.view.place_text('3')
    

    # manage the session
    def session_manager(self):

        #idle
        if self.state == 'idle':
            self.view.place_text('Naciśnij spację')
            return
        
        elif self.state.split('.')[0] == 'photo':
            self.photo_taker()
        
        elif self.state == 'printing':
            self.put_together()



    # main loop
    def render_view(self):

        try:
            self.view.refresh(self.framerate)
        except:
            print('could not get the view. exiting...')
            return

        key = self.view.pressed_key

        self.session_manager()
        
        if key == ord('q'):
            print('user exit')
            return
        
        elif key == ord(' '):
            if self.state == 'idle':
                self.update_state('photo.1')
        
        #display
        self.view.display(self.window_name)
        self.render_view()