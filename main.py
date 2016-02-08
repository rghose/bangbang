__version__ = "0.1"
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

#setup graphics
from kivy.config import Config
Config.set('graphics','resizable',0)

#Graphics fix
from kivy.core.window import Window

Window.fullscreen = True
Window.borderless = True
Window.clearcolor = (0.2,0.5,0.5,0.5)

bird_entry_times= [
    [250],
    [250, 1000, 2000, 3000],
    [250, 1000, 2000, 3000, 4000, 6000]
]


__NAME_OF_THE_GAME__ = "Bang Bang"
__about_text__ = "Hello this is a mirage game. (C) Oshur Inc."

__score_level_up__ = 1000
__score_kill_bird__ = 100
__score_shoot_bullet__ = 1

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
        self.layout.width = Window.width/2
        self.layout.height = Window.height/2
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
        self.layout = BoxLayout(orientation = 'vertical')
        self.layout.width = Window.width/2
        self.layout.height = Window.height/2
        self.layout.x = Window.width/2 - self.layout.width/2
        self.layout.y = Window.height/2 - self.layout.height/2
        self.add_widget(self.layout)

        self.msg = Label(text = __NAME_OF_THE_GAME__)
        self.msg.font_size = Window.width*0.07
        self.msg.pos = (Window.width*0.45,Window.height*0.75)
        self.add_widget(self.msg)
        self.img = Image(source = './images/hunt.jpg')
        self.img.size = (Window.width*1,Window.height*1)
        self.img.pos = (0,0)
        self.img.opacity = 0.45
        self.add_widget(self.img)


class WidgetDrawer(Widget):
    def __init__(self, imageStr, **kwargs):
        super(WidgetDrawer, self).__init__(**kwargs)
        with self.canvas:
            self.size = (Window.width*.002* self.mylength,Window.height*.002* self.myheight)
            self.rect_bg=Rectangle(source=imageStr,pos=self.pos,size = self.size)
            self.bind(pos=self.update_graphics_pos)
            self.x = self.center_x
            self.y = self.center_y
            self.pos = (self.x,self.y)
            self.rect_bg.pos = self.pos
    def update_graphics_pos(self, instance, value):
        self.rect_bg.pos = value
    def setSize(self,width, height):
        self.size = (width, height)
    def setPos(xpos,ypos):
        self.x = xpos
        self.y = ypos


class Water(WidgetDrawer):
    mylength=NumericProperty(1/0.002)
    myheight=NumericProperty(Window.height*(0.3))

    def move(self):
        pass

    def update(self):
        pass

# This is a bird shit
class BirdShit(WidgetDrawer):
    velocity_y = -1
    mylength = NumericProperty(2)
    myheight = NumericProperty(2)
    def move(self):
        self.y = self.y + self.velocity_y
    def update(self):
        self.move()

# This draws the bird.
class Bird(WidgetDrawer):
    #all_d_shitz = [] # Do we need to track the shitz of each bird? No.
    velocity_x = 1
    mylength = NumericProperty(20)
    myheight = NumericProperty(20)
    def move(self):
        self.x = self.x + self.velocity_x
    def update(self):
        self.move()

class Bullet(WidgetDrawer):
    velocity_y = 1
    mylength = NumericProperty(2)
    myheight = NumericProperty(2)
    def move(self):
        self.y = self.y + self.velocity_y
    def update(self):
        self.move()

class Shooter(WidgetDrawer):

    velocity_x = 0
    mylength = NumericProperty(40)
    myheight = NumericProperty(25)

    def move(self):
        self.x = self.x + self.velocity_x
        if self.x+self.mylength > Window.width*0.95 or self.x < Window.width*0.02:
            self.velocity_x = 0

    def update(self):
        self.move()

class Explosion(WidgetDrawer):
    mylength = NumericProperty(50)
    myheight = NumericProperty(50)
    pass

class GUI(Widget):

    current_score = 0

    explosion_widget = None
    remove_explosion_widget = -1

    explosion_sound = None

    change_level_flag = False
    current_level = 1
    current_counter = 0
    bullets = []
    birds = []

    # data...
    bird_entry = []

    def play_sound(self):
        if self.explosion_sound == None:
            self.explosion_sound = SoundLoader.load('./sounds/explosion.wav')
            print(self.explosion_sound)
        self.explosion_sound.volume = 1
        self.explosion_sound.play()
        print(self.explosion_sound.length)

    def stop_sound(self):
        if self.explosion_sound == None:
            self.explosion_sound = SoundLoader.load('./sounds/explosion.wav')
            return
        self.explosion_sound.stop()

    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)

        # Preload audio and images...
        self.explosion_widget = Explosion(imageStr='./images/explosion.gif')
        self.explosion_sound = SoundLoader.load('./sounds/explosion.wav')

        self.highScoreLabel = Label(text='Score: 0')
        self.highScoreLabel.x = Window.width/2 - self.highScoreLabel.width/2
        self.highScoreLabel.y = Window.height * 0.85
        self.highScoreLabel.halign = 'center'
        self.add_widget(self.highScoreLabel)

        self.shooter = Shooter(imageStr = './images/shooter.png')
        self.shooter.x = Window.width*0.25
        self.shooter.y = Window.height*0.35
        self.add_widget(self.shooter)

        self.water = Water(imageStr ='./images/water.jpg')
        self.water.x = 0
        self.water.y = 0
        self.add_widget(self.water)

    def on_touch_down(self, touch):
        if touch.y > self.shooter.y + 10:
            #print "before:", self.bullets
            bullet = Bullet(imageStr = './images/bullet.gif')
            bullet.x = self.shooter.x + (self.shooter.mylength/2)
            bullet.y = self.shooter.y + (self.shooter.myheight)
            self.add_widget(bullet)
            self.bullets.append(bullet)
            self.current_score -= __score_shoot_bullet__
            self.highScoreLabel.text = "Level: "+str(self.current_level)+"\nScore: "+str(self.current_score)
            #print "after:", self.bullets
        elif touch.x > self.shooter.x:
            self.shooter.velocity_x = 1
        elif touch.x < self.shooter.x:
            self.shooter.velocity_x = -1

    # This is the main function that gets updated with each interval
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

        # All loading done... (remove unwanted widgets)
        if self.remove_explosion_widget == 0:
            self.remove_widget(self.explosion_widget)
            self.remove_explosion_widget-=1
        elif self.remove_explosion_widget > 0:
            self.remove_explosion_widget-=1

        # Check if bird is scheduled for now...
        if self.bird_entry.count(self.current_counter) > 0:
            self.bird_entry.remove(self.current_counter)
            bird = Bird(imageStr='./images/bird.jpg')
            bird.x = 50
            bird.y = Window.height * 0.9
            self.add_widget(bird)
            self.birds.append(bird)
            print("Adding bird")

        # Update birds and remove if not needed
        for b in self.birds:
            # Check if bird needs to be killed
            for bullet in self.bullets:
                if (bullet.x > b.x and bullet.x < b.x + b.mylength) and (bullet.y > b.y and bullet.y < b.y+b.myheight):
                    self.remove_widget(b)
                    self.remove_widget(bullet)
                    print("Detected collision and hence removing:", bullet, b)
                    self.explosion_widget.x = bullet.x-20
                    self.explosion_widget.y= bullet.y-20
                    self.add_widget(self.explosion_widget)
                    self.bullets.remove(bullet)
                    self.birds.remove(b)
                    self.remove_explosion_widget = 30
                    self.play_sound()
                    # Update score
                    self.current_score += __score_kill_bird__
                    self.highScoreLabel.text = "Level: "+str(self.current_level)+"\nScore: "+str(self.current_score)
            b.update()
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

        if len(self.bird_entry) == 0:
            self.change_level_flag = True

        # Update shooter
        self.shooter.update()

class ClientApp(App):
    def build(self):
        self.parent = Widget() #this is an empty holder for buttons, etc
        self.app = GUI()
        self.sm = SmartStartMenu()
        self.sm.buildUp()

        # Nested function...
        def check_button(obj):
            if self.sm.buttonText == 'start':
                #remove menu and optional about text
                try:
                    self.parent.remove_widget(self.aboutText)
                except:
                    pass
                self.parent.remove_widget(self.sm)
                print (' we should start the game now')
                Window.clearcolor = (0.1,0.5,1,1.)
                self.parent.add_widget(self.app)
                Clock.unschedule(self.app.update)
                Clock.schedule_interval(self.app.update, 1.0/60.0)

            if self.sm.buttonText == 'about':
                self.aboutText = Label(text = __about_text__)
                self.aboutText.pos = (Window.width*0.45,Window.height*0.15)
                self.parent.add_widget(self.aboutText)

        self.sm.bind(on_button_release = check_button)
        self.parent.add_widget(self.sm)
        return self.parent

ClientApp().run()