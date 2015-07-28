# Running in CodeSkulptor!
import simplegui
import math
import random

WIDTH = 800
HEIGHT = 600
friction = 0.4
score = 0
lives = 3
time = 0


# Help function!
def angle_to_vector(angle):
    vertical = math.cos(math.radians(angle))
    horizontal = math.sin(math.radians(angle))
    return [horizontal, vertical]


class ImageInfo:
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
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
debris_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

soundtrack = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


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

    # Stop by friction!Down is unuseful!
    def accelerate(self, key):
        """
        if key == simplegui.KEY_MAP['down']:
        if self.thrust:
            self.thrust = False
        """
        if key == simplegui.KEY_MAP['up']:
            self.thrust = True
            direction = angle_to_vector(self.angle)
            self.vel[1] += 3 * direction[1]
            self.vel[0] += 3 * direction[0]
        elif key == simplegui.KEY_MAP['left']:
            self.angle_vel -= 5
        elif key == simplegui.KEY_MAP['right']:
            self.angle_vel += 5

    def slow_down(self, key):
        global ship_thrust_sound
        if key == simplegui.KEY_MAP['up']:
            self.thrust = False
            ship_thrust_sound.rewind()

    def shoot(self):
        global a_missile
        direction = angle_to_vector(self.angle)
        if direction[0] > 0 and direction[1] > 0:
            a_missile = Sprite([self.pos[0] + self.image_center[0], self.pos[1] - self.image_center[1]],
                               [self.vel[0] + 4 * direction[0], self.vel[1] + 4 * direction[1]],
                               self.angle, 0, missile_image, missile_info, missile_sound)
        elif direction[0] > 0 > direction[1]:
            a_missile = Sprite([self.pos[0] + self.image_center[0], self.pos[1] + self.image_center[1]],
                               [self.vel[0] + 4 * direction[0], self.vel[1] + 4 * direction[1]],
                               self.angle, 0, missile_image, missile_info, missile_sound)
        elif direction[0] < 0 < direction[1]:
            a_missile = Sprite([self.pos[0] - self.image_center[0], self.pos[1] + self.image_center[1]],
                               [self.vel[0] + 4 * direction[0], self.vel[1] + 4 * direction[1]],
                               self.angle, 0, missile_image, missile_info, missile_sound)
        elif direction[0] < 0 and direction[1] < 0:
            a_missile = Sprite([self.pos[0] - self.image_center[0], self.pos[1] - self.image_center[1]],
                               [self.vel[0] + 4 * direction[0], self.vel[1] + 4 * direction[1]],
                               self.angle, 0, missile_image, missile_info, missile_sound)

    def draw(self, canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + 90, self.image_center[1]], self.image_size, self.pos,
                              self.image_size, math.radians(self.angle))
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size,
                              math.radians(self.angle))

    def update(self):
        global ship_thrust_sound, friction
        self.angle += self.angle_vel
        if self.thrust:
            ship_thrust_sound.play()
        self.pos[0] += self.vel[0] * (1 - friction)
        self.pos[1] -= self.vel[1] * (1 - friction)
        if self.pos[0] >= WIDTH:
            self.pos[0] %= WIDTH
        elif self.pos[0] <= 0:
            self.pos[0] += WIDTH
        if self.pos[1] >= HEIGHT:
            self.pos[1] %= HEIGHT
        elif self.pos[1] <= 0:
            self.pos[1] += HEIGHT


class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
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
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size,
                          math.radians(self.angle))

    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if self.pos[0] >= WIDTH:
            self.pos[0] %= WIDTH
        elif self.pos[0] <= 0:
            self.pos[0] += WIDTH
        if self.pos[1] >= HEIGHT:
            self.pos[1] %= HEIGHT
        elif self.pos[1] <= 0:
            self.pos[1] += HEIGHT


def draw(canvas):
    global time, lives, score

    # animate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                      [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]],
                      [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]],
                      [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)

    my_ship.update()
    a_rock.update()
    a_missile.update()

    canvas.draw_text("Lives", [100, 70], 20, 'White')
    canvas.draw_text(str(lives), [100, 100], 20, 'White')
    canvas.draw_text("Score", [650, 70], 20, 'White')
    canvas.draw_text(str(score), [650, 100], 20, 'White')


def key_up(key):
    global my_ship
    my_ship.slow_down(key)


def key_down(key):
    global my_ship
    if key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
    else:
        my_ship.accelerate(key)


def rock_spawner():
    global a_rock
    a_rock = Sprite([WIDTH / random.randint(0, 10), HEIGHT / random.randint(0, 10)],
                    [random.randint(0, 3), random.randint(0, 3)],
                    random.randint(0, 360), random.randint(0, 20), asteroid_image, asteroid_info)


frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keyup_handler(key_up)
frame.set_keydown_handler(key_down)

my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1, 1], 0, 0, missile_image, missile_info, missile_sound)

timer = simplegui.create_timer(1000.0, rock_spawner)

timer.start()
frame.start()
