# Running in CodeSkulptor!

import simplegui
import random

# Basis
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# Controller
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
paddle1_pos = [PAD_WIDTH / 2, HEIGHT / 2]
paddle2_pos = [WIDTH - PAD_WIDTH / 2, HEIGHT / 2]
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]
score1 = 0
score2 = 0

def spawn_ball(direction):
    global ball_pos, ball_vel
    if direction == RIGHT:
        ball_vel[0] = random.randrange(2, 4)
        ball_vel[1] = -(random.randrange(1, 3))
    elif direction == LEFT:
        ball_vel[0] = -(random.randrange(2, 4))
        ball_vel[1] = -(random.randrange(1, 3))

# choice is to use "LEFT" or "RIGHT" randomly.
def new_game(choice):
    global ball_pos, ball_vel, paddle1_pos, paddle2_pos
    global paddle1_vel, paddle2_vel
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    paddle1_pos = [PAD_WIDTH / 2, HEIGHT / 2]
    paddle2_pos = [WIDTH - PAD_WIDTH / 2, HEIGHT / 2]
    paddle1_vel = [0, 0]
    paddle2_vel = [0, 0]
    if choice == 0:
        spawn_ball(LEFT)
    elif choice == 1:
        spawn_ball(RIGHT)
    
def restart_handler():
    choice = random.randrange(0,2)
    new_game(choice)  

# Each collision causes the velocity of the ball increasing by 1.
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    paddle1_pos[1] += paddle1_vel[1]
    paddle2_pos[1] += paddle2_vel[1]
    if paddle1_pos[1] + PAD_HEIGHT / 2 >= HEIGHT or paddle1_pos[1] - PAD_HEIGHT / 2 <= 0:
        paddle1_vel[1] = 0
    if paddle2_pos[1] + PAD_HEIGHT / 2 >= HEIGHT or paddle2_pos[1] - PAD_HEIGHT / 2 <= 0:
        paddle2_vel[1] = 0
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # Do something for physical estimates and good-looking!
    if (ball_pos[0] - BALL_RADIUS) <= (paddle1_pos[0] + PAD_WIDTH / 2) and abs(paddle1_pos[1] - ball_pos[1]) <= PAD_HEIGHT / 2 + 4:
        ball_vel[0] = - ball_vel[0] + 1
    elif ball_pos[1] - BALL_RADIUS <= 0:
        ball_vel[1] = - ball_vel[1] + 1
    elif (ball_pos[0] + BALL_RADIUS) >= (paddle2_pos[0] - PAD_WIDTH / 2)and abs(paddle2_pos[1] - ball_pos[1]) <= PAD_HEIGHT / 2 + 4:
        ball_vel[0] = - ball_vel[0] - 1
    elif ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_vel[1] = - ball_vel[1] - 1
    if ball_pos[0] - BALL_RADIUS <= paddle1_pos[0]:
        score2 += 1
        new_game(random.randrange(0, 2))
    elif ball_pos[0] + BALL_RADIUS >= paddle2_pos[0]:
        score1 += 1
        new_game(random.randrange(0, 2))
        
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, 'White')
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, 'White')
    canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, 'White')
    canvas.draw_text(str(score1), [150, 100], 50, 'White')
    canvas.draw_text(str(score2), [450, 100], 50, 'White')
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'White', 'White')
    canvas.draw_polygon([[paddle1_pos[0] - PAD_WIDTH / 2, paddle1_pos[1] + PAD_HEIGHT /2], 
                        [paddle1_pos[0] + PAD_WIDTH / 2, paddle1_pos[1] + PAD_HEIGHT /2],
                        [paddle1_pos[0] + PAD_WIDTH / 2, paddle1_pos[1] - PAD_HEIGHT /2],
                        [paddle1_pos[0] - PAD_WIDTH / 2, paddle1_pos[1] - PAD_HEIGHT /2]],
                        1, 'White', 'White')
    canvas.draw_polygon([[paddle2_pos[0] - PAD_WIDTH / 2, paddle2_pos[1] + PAD_HEIGHT /2], 
                        [paddle2_pos[0] + PAD_WIDTH / 2, paddle2_pos[1] + PAD_HEIGHT /2],
                        [paddle2_pos[0] + PAD_WIDTH / 2, paddle2_pos[1] - PAD_HEIGHT /2],
                        [paddle2_pos[0] - PAD_WIDTH / 2, paddle2_pos[1] - PAD_HEIGHT /2]],
                        1, 'White', 'White')
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel[1] = - 5
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel[1] = 5
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel[1] = - 5
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel[1] = 5
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['s']:
        paddle1_vel[1] = 0
    if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']:
        paddle2_vel[1] = 0

frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Restart", restart_handler, 80)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.start()
