__version__ = "0.2.1"
from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivy.graphics import Rectangle
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.properties import StringProperty

from kivy.core.audio import SoundLoader,Sound

from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

#setup graphics
from kivy.config import Config
Config.set('graphics','resizable',0)

#Graphics fix
from kivy.core.window import Window

import random

SIZE_RELATIVE = "rel"
SIZE_ABSOLUTE = "abs"

FRAMES_PER_SECOND = 60.0

Window.fullscreen = True
#Window.size = [520, 800]
Window.borderless = True
Window.clearcolor = (255.0/255.0, 237.0/255.0, 192.0/255.0, 1)

bird_entry_times= [
    [250],
    [250, 1000, 2000, 3000],
    [250, 1000, 2000, 3000, 4000, 6000]
]


__NAME_OF_THE_GAME__ = "Man vs Seagulls"

__color_window_bg__ = [249,198,103]

__score_level_up__ = 10
__score_kill_bird__ = 1

class MenuScreen(Screen):
    pass

class AboutScreen(Screen):
    pass

class MyButton(Button):
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.font_size = Window.width*0.018

class SmartMenu(Widget):
    buttonList = []

    def __init__(self, **kwargs):
        self.register_event_type('on_button_release') #creating a custom event called 'on_button_release' that will be used to pass information from the menu to the parent instance

        super(SmartMenu, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation = 'vertical')
        self.layout.width = Window.width
        self.layout.height = Window.height
        self.layout.x = Window.width/2 - self.layout.width/2
        self.layout.y = Window.height/2 - self.layout.height/2
        self.add_widget(self.layout)

    def on_button_release(self, *args):
        pass

    def callback(self,instance):
        self.buttonText = instance.text
        self.dispatch('on_button_release')

    def addButtons(self):
        for k in self.buttonList:
            tmpBtn = MyButton(text = k)
            tmpBtn.background_color = [.4, .4, .4, .4]
            tmpBtn.bind(on_release = self.callback)
            self.layout.add_widget(tmpBtn)

    def buildUp(self):
        self.addButtons()

# The menu
class SmartStartMenu(SmartMenu):

    buttonList = ['start', 'about']

    def __init__(self, **kwargs):
        super(SmartStartMenu, self).__init__(**kwargs)
        self.size = (Window.width, Window.height)
        print("Start menu:",self.size, self.size_hint)

        self.layout = BoxLayout(orientation = 'vertical')
        self.layout.width = Window.width/2
        self.layout.height = Window.height/2
        self.layout.x = Window.width/2 - self.layout.width/2
        self.layout.y = Window.height/2 - self.layout.height/2
        self.add_widget(self.layout)

        self.msg = Label(text = __NAME_OF_THE_GAME__)
        self.msg.font_size = Window.width*0.07
        self.msg.pos = (Window.width/2 - self.msg.width/2,Window.height*0.8 - self.msg.height/2)
        self.add_widget(self.msg)

        SmartMenu.addButtons(self)

    def setSize(self,width, height):
        self.size = (width, height)

class WidgetDrawer(Widget):
    def __init__(self, imageStr, **kwargs):
        super(WidgetDrawer, self).__init__(**kwargs)
        with self.canvas:
            if self.size_type == SIZE_RELATIVE:
                self.size = (Window.width*self.mywidth ,Window.height*self.myheight)
            elif self.size_type == SIZE_ABSOLUTE:
                self.size = (self.mywidth, self.myheight)
            else:
                self.size = (Window.width*.002* self.mywidth,Window.height*.002* self.myheight)
            self.rect_bg=Rectangle(source=imageStr,pos=self.pos,size = self.size)
            self.bind(pos=self.update_graphics_pos)
            self.x = self.center_x
            self.y = self.center_y
            self.pos = (self.x - self.width,self.y)
            self.rect_bg.pos = self.pos
    def update_graphics_pos(self, instance, value):
        self.rect_bg.pos = value
    def setSize(self,width, height):
        self.size = (width, height)
    def setPos(xpos,ypos):
        self.x = xpos
        self.y = ypos

class HeartLife(WidgetDrawer):
    size_type = SIZE_RELATIVE
    mywidth=0.1
    myheight=0.08

    def move(self):
        pass

    def update(self):
        pass


class Water(WidgetDrawer):

    size_type = SIZE_RELATIVE
    mywidth=1
    myheight=0.35

    def move(self):
        pass

    def update(self):
        pass

# This is a bird shit
class BirdShit(WidgetDrawer):
    velocity_y = -1
    size_type = SIZE_ABSOLUTE
    mywidth = NumericProperty(10)
    myheight = NumericProperty(20)
    def move(self):
        self.y = self.y + self.velocity_y
    def update(self):
        self.move()

# This draws the bird.
class Bird(WidgetDrawer):
    #all_d_shitz = [] # Do we need to track the shitz of each bird? No.
    has_shit = 0 # track the number of shitz by this birdy
    velocity_x = 1
    size_type = SIZE_ABSOLUTE
    mywidth = 0.1*Window.width
    myheight = 0.08*Window.height
    def move(self):
        self.x = self.x + self.velocity_x
    def update(self):
        self.move()

class Bullet(WidgetDrawer):
    velocity_y = 1
    size_type = SIZE_ABSOLUTE
    mywidth = NumericProperty(5)
    myheight = NumericProperty(5)
    def move(self):
        self.y = self.y + self.velocity_y
    def update(self):
        self.move()

class Shooter(WidgetDrawer):
    velocity_x = 0
    size_type = SIZE_ABSOLUTE
    mywidth = 0.16*Window.width
    myheight = 0.1*Window.height

    def move(self):
        self.x = self.x + self.velocity_x
        if self.x+self.mywidth > Window.width*0.95 or self.x < Window.width*0.02:
            self.velocity_x = 0

    def update(self):
        self.move()

class Explosion(WidgetDrawer):
    size_type = SIZE_ABSOLUTE
    mywidth = NumericProperty(50)
    myheight = NumericProperty(50)

    def move(self):
        pass

    def update(self):
        pass

class GUI(Widget):
    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)

class GameScreen(Screen):
    current_score = 0
    current_lives = 3

    explosion_widget = None
    remove_explosion_widget = -1

    explosion_sound = None

    change_level_flag = False
    current_level = 1
    current_counter = 0
    bullets = []
    birds = []
    shitz = []
    hearts = []

    # data...
    bird_entry = []

    def play_swipe_sound(self):
        if self.swipe_sound == None:
            self.swipe_sound = SoundLoader.load('./sounds/Swipe-Sound-Water.mp3')
        self.swipe_sound.volume = 1
        self.swipe_sound.play()

    def stop_swipe_sound(self):
        if self.swipe_sound == None:
            return
        self.swipe_sound.stop()


    def play_explosion_sound(self):
        if self.explosion_sound == None:
            self.explosion_sound = SoundLoader.load('./sounds/Bird-Shot-Sound.mp3')
            print(self.explosion_sound)
        self.explosion_sound.volume = 1
        self.explosion_sound.play()

    def stop_explosion_sound(self):
        if self.explosion_sound == None:
            return
        self.explosion_sound.stop()

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        [self.window_width,self.window_height] = Window.size

        self.current_lives = 3

        # Preload audio and images...
        self.explosion_widget = Explosion(imageStr='./images/explosion.gif')
        self.explosion_sound = SoundLoader.load('./sounds/Bird-Shot-Sound.mp3')
        self.swipe_sound = SoundLoader.load('./sounds/Swipe-Sound-Water.mp3')

        self.shooter = Shooter(imageStr = './images/hunter.png')
        self.shooter.allow_stretch = True
        self.shooter.keep_ratio = False
        self.shooter.x = self.window_width*0.25
        self.shooter.y = self.window_height*0.35
        self.add_widget(self.shooter)

        self.water = Water(imageStr ='./images/water.png')
        self.water.allow_stretch = True
        self.water.keep_ratio = False
        self.water.x = 0
        self.water.y = 0
        self.add_widget(self.water)

        self.highScoreLabel = Label(text='Score: 0')
        self.highScoreLabel.width = self.window_width * 0.2
        self.highScoreLabel.height = self.window_height * 0.05
        self.highScoreLabel.x = self.window_width/2 - self.highScoreLabel.width/2
        self.highScoreLabel.y = self.window_height * 0.85
        self.highScoreLabel.halign = 'center'
        self.highScoreLabel.font_name = "./fonts/KenPixelMiniSquare.ttf"
        self.add_widget(self.highScoreLabel)

        self.heart_life_1 = HeartLife(imageStr='./images/PixelHeart.png')
        self.heart_life_1.allow_stretch = True
        self.heart_life_1.keep_ratio = False
        self.heart_life_1.x = self.window_width*0.65
        self.heart_life_1.y = self.window_height*0.85
        self.add_widget(self.heart_life_1)

        self.heart_life_2 = HeartLife(imageStr='./images/PixelHeart.png')
        self.heart_life_2.allow_stretch = True
        self.heart_life_2.keep_ratio = False
        self.heart_life_2.x = self.window_width*0.75
        self.heart_life_2.y = self.window_height*0.85
        self.add_widget(self.heart_life_2)

        self.heart_life_3 = HeartLife(imageStr='./images/PixelHeart.png')
        self.heart_life_3.allow_stretch = True
        self.heart_life_3.keep_ratio = False
        self.heart_life_3.x = self.window_width*0.85
        self.heart_life_3.y = self.window_height*0.85
        self.add_widget(self.heart_life_3)


        self.hearts.append(self.heart_life_1)
        self.hearts.append(self.heart_life_2)
        self.hearts.append(self.heart_life_3)

    def on_touch_down(self, touch):
        self.play_swipe_sound()
        if touch.x > self.shooter.x:
            self.shooter.velocity_x = 1
        elif touch.x < self.shooter.x:
            self.shooter.velocity_x = -1
        print("touched")

    def update(self,dt):
        self.current_counter += 1

        if self.change_level_flag == True and len(self.birds) == 0:
            print("Change level from ",self.current_level)
            self.current_level += 1
            self.current_counter = 1
            self.change_level_flag = False
            self.current_score += __score_level_up__
            self.highScoreLabel.text = "Level: "+str(self.current_level)+"\nScore: "+str(self.current_score)

        # Load level data... (on level change)
        if self.current_counter <= 1:
            self.bird_entry = bird_entry_times[self.current_level-1]

        # Shoot every second.
        if self.current_counter % FRAMES_PER_SECOND == 0:
            bullet = Bullet(imageStr = './images/bullet.gif')
            bullet.x = self.shooter.x + (self.shooter.mywidth/2)
            bullet.y = self.shooter.y + (self.shooter.myheight)
            self.add_widget(bullet)
            self.bullets.append(bullet)

        # All loading done... (remove unwanted widgets)
        if self.remove_explosion_widget == 0:
            self.remove_widget(self.explosion_widget)
            self.remove_explosion_widget-=1
        elif self.remove_explosion_widget > 0:
            self.remove_explosion_widget-=1

        # Check if bird is scheduled for now...
        if self.bird_entry.count(self.current_counter) > 0:
            self.bird_entry.remove(self.current_counter)
            bird = Bird(imageStr='./images/SeagullRight.png')
            bird.x = 50
            bird.y = Window.height * (0.6 + (random.random()*0.3))
            self.add_widget(bird)
            self.birds.append(bird)
            print("Adding bird")

        # Update birds and remove if not needed
        for b in self.birds:
            # Check if bird needs to be killed
            for bullet in self.bullets:
                if (bullet.x > b.x and bullet.x < b.x + b.mywidth) and (bullet.y > b.y and bullet.y < b.y+b.myheight):
                    self.remove_widget(b)
                    self.remove_widget(bullet)
                    print("Detected collision and hence removing:", bullet, b)
                    self.explosion_widget.x = bullet.x-20
                    self.explosion_widget.y= bullet.y-20
                    #self.add_widget(self.explosion_widget)
                    self.bullets.remove(bullet)
                    self.birds.remove(b)
                    self.remove_explosion_widget = 30
                    self.play_explosion_sound()
                    # Update score
                    self.current_score += __score_kill_bird__
                    self.highScoreLabel.text = "Level: "+str(self.current_level)+"\nScore: "+str(self.current_score)
            b.update()
            # Add a shit... if we wanna
            some_random_number = (random.random() * 10)
            if 0 == b.has_shit and (some_random_number >= 5):
                print("add shit")
                s = BirdShit(imageStr='./images/poop.gif')
                s.x = b.x
                s.y = b.y
                self.add_widget(s)
                self.shitz.append(s)
                b.has_shit = b.has_shit + 1
            if b.x > Window.width*0.95:
                print("Removed bird")
                self.remove_widget(b)
                self.birds.remove(b)

        # Update bullets and remove if not needed
        for b in self.bullets:
            b.update()
            if b.y > Window.height*0.95:
                self.remove_widget(b)
                self.bullets.remove(b)

        # Update shitz and remove if not needed
        for s in self.shitz:
            if (s.x>self.shooter.x and s.x<self.shooter.x+self.shooter.mywidth) and (s.y>self.shooter.y and s.y<self.shooter.y+self.shooter.myheight):
                print("Hit with shitz", s.x, s.y, s.width, s.height, self.shooter.x, self.shooter.y, self.shooter.width, self.shooter.height)
                self.current_lives = self.current_lives - 1
                self.remove_widget(self.hearts[self.current_lives])
                self.hearts.remove(self.hearts[self.current_lives])
                self.remove_widget(s)
                self.shitz.remove(s)
                if self.current_lives == 0: # game over
                    self.manager.current = "main_menu"
                next
            if s.y < Window.height*0.35:
                print("remove shitz", s.x, s.y)
                self.remove_widget(s)
                self.shitz.remove(s)
                next
            s.update()

        if len(self.bird_entry) == 0:
            self.change_level_flag = True

        # Update shooter
        self.shooter.update()

Builder.load_string("""
#:import Clock kivy.clock.Clock
<MenuScreen>:
    name: "main_menu"
    BoxLayout:
        orientation: 'vertical'
        Label:
            font_name: "./fonts/KenPixelMiniSquare.ttf"
            text: "Man vs Seagull"
            color: (0,0,0,1)
            font_size: 35
            size_hint: 1,0.4
        BoxLayout:
            orientation: 'vertical'
            size_hint: 1,0.6
            Button:
                font_name: "./fonts/KenPixelMiniSquare.ttf"
                pos_hint: {"right":0.9, "top":0.6}
                size_hint: 0.8,0.15
                color: (0,0,0,1)
                background_color: (0,0,0,0)
                text: "start"
                on_release: app.root.current="game_screen"
            Button:
                font_name: "./fonts/KenPixelMiniSquare.ttf"
                pos_hint: {"right":0.9, "top":0.4}
                size_hint: 0.8,0.15
                color: (0,0,0,1)
                background_color: (0,0,0,0)
                text: "about"
                on_release: app.root.current="about_screen"
            Widget:
                size_hint: 0.8, 0.7
                background_color: (0,0.2,0.8,0.8)

<AboutScreen>:
    name: "about_screen"
    BoxLayout:
        orientation: 'vertical'
        Label:
            color: (0,0,0,1)
            font_name: "./fonts/KenPixelMiniSquare.ttf"
            text: app.GAME_COPYRIGHT_TEXT
        Button:
            font_name: "./fonts/KenPixelMiniSquare.ttf"
            size_hint: 1,0.2
            pos_hint: {"right":1, "top":0.3}
            text: "back"
            on_release: app.root.current="main_menu"

<GameScreen>:
    id: gamescreen
    name: "game_screen"
    on_enter: Clock.schedule_interval(gamescreen.update, 1.0/app.FRAMES_PER_SECOND)
    on_leave: Clock.unschedule(gamescreen.update)
    GUI:
        id: mygui
        font_name: "./fonts/KenPixelMiniSquare.ttf"

""")

from kivy.base import EventLoop

class TestApp(App):

    FRAMES_PER_SECOND = 60

    GAME_COPYRIGHT_TEXT = "This is a mirage game.\n\
All Rights reserved\n\n\n\
Feel free to contact me at hansum.rahul@gmail.com"

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            if(self.sm.current=="game_screen"):
                self.sm.current = "main_menu"
                return True
            return False

    def build(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(name='main_menu'))
        self.sm.add_widget(AboutScreen(name='about_screen'))

        self.game_screen_widget = GameScreen(name='game_screen')
        self.sm.add_widget(self.game_screen_widget)
        return self.sm


if __name__ == '__main__':
    TestApp().run()

#ClientApp().run()
