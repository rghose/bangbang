__version__ = "0.1"

from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivy.graphics import Rectangle
from kivy.properties import NumericProperty
from kivy.core.window import Window

from kivy.clock import Clock

#setup graphics
from kivy.config import Config
Config.set('graphics','resizable',0)

#Graphics fix
from kivy.core.window import Window
Window.clearcolor = (0.1,0.5,1,1.)

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

class GUI(Widget):

    bullets = []

    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        l = Label(text='Bang Bang!')
        l.x = Window.width/2 - l.width/2
        l.y = Window.height * 0.85
        self.add_widget(l)

        self.shooter = Shooter(imageStr = './shooter.png')
        self.shooter.x = Window.width*0.25
        self.shooter.y = Window.height*0.35
        self.add_widget(self.shooter)

        self.water = Water(imageStr ='./water.jpg')
        self.water.x = 0
        self.water.y = 0
        self.add_widget(self.water)

    def on_touch_down(self, touch):
        print touch
        if touch.y > self.shooter.y + 10:
            #print "before:", self.bullets
            bullet = Bullet(imageStr = './bullet.gif')
            bullet.x = self.shooter.x + (self.shooter.mylength/2)
            bullet.y = self.shooter.y + (self.shooter.myheight)
            self.add_widget(bullet)
            self.bullets.append(bullet)
            #print "after:", self.bullets
        elif touch.x > self.shooter.x:
            self.shooter.velocity_x = 1
        elif touch.x < self.shooter.x:
            self.shooter.velocity_x = -1

    def update(self,dt):
        #print "Total:",self.bullets
        for b in self.bullets:
            b.update()
            if b.y > Window.height*0.95:
                self.remove_widget(b)
                self.bullets.remove(b)
        self.shooter.update()

class ClientApp(App):
    def build(self):
        app = GUI()
        Clock.schedule_interval(app.update, 1.0/60.0)
        return app

ClientApp().run()