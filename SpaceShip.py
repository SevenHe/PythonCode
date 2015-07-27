# Running in CodeSkulptor1
import simplegui
import math
import random

WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0

class ImageInfo:
  def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
    self.center = center
    self.size = size
    self.radius = radius
    if lifespan:
      self.lifespan = lifespan
    else:
      self.lifespan = float('inf')
      self.animated = animated
    
  def get_center(self):
    return self.center
  
  def get_size(self):
    return self.size
    
  def get_radius(self):
    return self.radius
    
  def get_lifespan(self):
    return self.lifespan
    
  def get_animated(self):
    return self.animated
  
  
debris_info = ImageInfo([320, 240], [640, 840])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")
splash_info = ImageInfo([200, 150], [400, 300])  
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")  
ship_info = ImageInfo([45, 45], [90, 90], 35)  
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")  
missile_info = ImageInfo([5,5], [10, 10], 3, 50)  
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")  
asteroid_info = ImageInfo([45, 45], [90, 90], 40)  
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")  
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)  
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")  
  

soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")  
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")  
missile_sound.set_volume(.5)  
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")  
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

class Ship:  
  def __init__(self, pos, vel, angle, image, info):  
    self.pos = [pos[0], pos[1]]  
    self.vel = [vel[0], vel[1]]  
    self.thrust = False  
    self.angle = angle  
    self.angle_vel = 0  
    self.image = image  
    self.image_center = info.get_center()  
    self.image_size = info.get_size()  
    self.radius = info.get_radius()  
  
  def draw(self,canvas):  
    canvas.draw_circle(self.pos, self.radius, 1, "White", "White")  
  
  def update(self):
    pass
  
class Sprite:  
  def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):  
    self.pos = [pos[0],pos[1]]  
    self.vel = [vel[0],vel[1]]  
    self.angle = ang  
    self.angle_vel = ang_vel  
    self.image = image  
    self.image_center = info.get_center()  
    self.image_size = info.get_size()  
    self.radius = info.get_radius()  
    self.lifespan = info.get_lifespan()  
    self.animated = info.get_animated()  
    self.age = 0  
    if sound:  
      sound.rewind()  
      sound.play()    
  
  def draw(self, canvas):
    canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
  
  def update(self):
    pass
    
    
def draw(canvas):  
  global time 
  
  # animiate background  
  time += 1  
  center = debris_info.get_center()  
  size = debris_info.get_size()
  wtime = (time / 8) % center[0]
  canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])  
  canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2*wtime, size[1]],
                    [WIDTH/2 + 1.25*wtime, HEIGHT / 2], [WIDTH - 2.5*wtime, HEIGHT])  
  canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2*wtime, size[1]], 
                    [1.25*wtime, HEIGHT / 2], [2.5*wtime, HEIGHT])
  
  my_ship.draw(canvas)
  a_rock.draw(canvas)
  a_missile.draw(canvas)
  
  my_ship.update(canvas)
  a_rock.update(canvas)
  a_missile.update(canvas)

def rock_spawner():
  pass
  
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.set_draw_handler(draw)

my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1, 1], 0, 0, missile_image, missile_info, missile_sound)

timer = simplegui.create_timer(1000.0, rock_spawner)

timer.start()
frame.start()
