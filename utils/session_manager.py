from datetime import datetime
from display_view import View
from photo_edit import fill_template, crop_photo, double_join, clear_cache, display_image
from os import rename, mkdir
from os import path as os_path
from printer_usage import print_file


class Session:

    def __init__(self, vid_source:str|int, printer_name:str, save_path:str='./saved', resolution:tuple[int,int]=(2560,1440), fullscreen=True):

        self.frame_refresh_delay = 30
        self.state = 'idle'
        self.last_step_start_time = 0
        self.freezed_frame = None
        self.view = View(vid_source, resolution, fullscreen)
        self.printer_name = printer_name

        # validate the save path
        if not os_path.exists(save_path):
            if save_path != './saved': 
                print('given path does not exist, saving in ./saved instead')
            self.save_path = './saved'
            if not os_path.exists('./saved'):
                mkdir('./saved')
        else:
            self.save_path = save_path    

    # function for state update
    def update_state(self, state:str):

        allowed_states = ['idle','photo.1','photo.2','photo.3','compiling','printing','printing.active','await_answer','delay']
        if not state in allowed_states:
            print('Session: unhandled state: ' + state)
            return
        
        # change frame_time_gap
        if state == 'idle':
            self.frame_refresh_delay = 30
        elif self.state == 'idle':
            self.frame_refresh_delay = 1

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
        
        double_join('./_cache/ready.jpg')



    # manage taking photos and the countdown
    def photo_taker(self):

        seconds_passed = datetime.timestamp(datetime.now()) - self.last_step_start_time

        # move on
        if seconds_passed >= 7:

            current_photo_num = int(self.state.split('.')[1])

            if current_photo_num == 3:
                self.update_state('compiling')
            else:
                self.update_state('photo.' + str(int(self.state.split('.')[1])+1))
            return

        if seconds_passed > 6:
            self.freezed_frame = None
            return 
        
        if seconds_passed >= 4.4:
            if not self.freezed_frame is None:
                self.view.frame = self.freezed_frame
            return

        if 4.25 <= seconds_passed < 4.4:
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
            self.view.place_text('Naciśnij spację', r_pos=(0,-0.15))
            self.view.place_text('aby rozpocząć sesję', r_pos=(0,0.15), font_scale=80)
            return
        
        elif self.state.split('.')[0] == 'photo':
            self.photo_taker()
        
        elif self.state == 'compiling':
            self.put_together()
            if os_path.exists('./_cache/ready.jpg'):
                self.update_state('printing')
        
        elif self.state.split('.')[0] == 'printing':
            if self.state == 'printing':
                print_file('./_cache/ready.jpg', self.printer_name)
                self.update_state('printing.active')
            self.view.place_text('drukowanie...')

            #check for print finish
            if datetime.timestamp(datetime.now()) - self.last_step_start_time > 5:
                self.update_state('await_answer')
        
        # wait for user answer
        elif self.state == 'await_answer':

            seconds_passed = int(datetime.timestamp(datetime.now()) - self.last_step_start_time)

            self.view.place_text('kliknij spację',r_pos=(0,-0.15),font_scale=100)
            self.view.place_text('aby wydrukwoać kolejną kopię',r_pos=(0,0.1),font_scale=80)
            self.view.place_text(str(5 - seconds_passed),r_pos=(0,0.30),font_scale=60)

            # end the loop
            if seconds_passed >= 5:
                print('clearing cache')
                self.update_state('delay')
                # display_image('./_cache/ready.jpg')
                clear_cache()
        
        # delay between potential sessions
        elif self.state == 'delay' and int(datetime.timestamp(datetime.now()) - self.last_step_start_time) >= 2:
            self.update_state('idle')


    # main loop
    def render_view(self):

        while True:
            try:
                self.view.refresh(self.frame_refresh_delay)
            except:
                print('could not get the view. exiting...')
                return

            key = self.view.pressed_key

            self.session_manager()
            
            if key == ord('q'):
                print('user exit')
                return
            
            elif key == ord('a'):
                if not self.state == 'idle':
                    clear_cache()
                    self.update_state('idle')
            
            elif key == ord(' '):
                if self.state == 'idle':
                    self.update_state('photo.1')
                if self.state == 'await_answer':
                    self.update_state('printing')
            
            #display
            self.view.display()