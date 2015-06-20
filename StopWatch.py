# Running in CodeSkulptor is successful !!

import simplegui

total_time = 0
width, height = 300, 300
win_times = 0
try_times = 0

# Helper Function!
def format(time):
    first = int(time) / 600
    middle = int(time) % 600 / 10
    last = int(time) % 600 % 10
    if middle >= 10:
        return str(first) + ":" + str(middle) + "." + str(last)
    else:
        return str(first) + ":0" + str(middle) + "." + str(last)

def start_button_handler():
    timer.start()

def stop_button_handler():
    global try_times, win_times
    try_times += 1
    if total_time % 10 == 0:
        win_times += 1

def reset_button_handler():
    global total_time, win_times, try_times
    if timer.is_running():
        timer.stop()
        total_time = 0
        win_times = 0
        try_times = 0

def timer_handler():
    global total_time
    total_time += 1

def draw_handler(canvas):
    global total_time
    text = format(total_time)
    text_width = frame.get_canvas_textwidth(text, 60)
    canvas.draw_text(str(win_times) + "/" + str(try_times)
                     , [190, 50], 40, "Green")
    canvas.draw_text(text, [(width - text_width) / 2, height /2 + 10]
                         , 60, "White")
    
# Register!
timer = simplegui.create_timer(100, timer_handler)    
frame = simplegui.create_frame("StopWatch", width, height)
frame.add_button("Start", start_button_handler, 110)
frame.add_button("Stop", stop_button_handler, 110)
frame.add_button("Reset", reset_button_handler, 110)
frame.set_draw_handler(draw_handler)

frame.start()
