# template for "Stopwatch: The Game"

import simplegui

# define global variables
counter = 0
stop_counter = 0
success_counter = 0
watch_running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(time):
    minutes = str(time//600)
    if len(str(time%600//10)) == 1:
        seconds = '0' + str(time%600//10)
    else:
         seconds = str(time%600//10) 
    tenth_of_seconds = str(time%600%10)
    return minutes + ':' + seconds + '.' + tenth_of_seconds
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_watch():
    global watch_running
    timer.start()
    watch_running = True
    
def stop_watch():
    global stop_counter, watch_running, success_counter 
    timer.stop()
    if watch_running:
        stop_counter += 1
        watch_running = False
    
    if counter%600%10 == 0:
        success_counter += 1

def reset_watch():
    global counter, stop_counter, success_counter
    counter = 0
    stop_counter = 0
    success_counter = 0

# define event handler for timer with 0.1 sec interval
def tick():
    global counter
    counter += 1

# define draw handler
def draw(canvas):
    canvas.draw_text(str(format(counter)), (70, 100), 30, 'White', 'sans-serif')
    canvas.draw_text(str(success_counter) + '/' + str(stop_counter), (160, 30), 20, 'Green', 'sans-serif')
  
# create frame
frame = simplegui.create_frame("Stopwatch: the game", 200, 200)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button("Start", start_watch, 100)
frame.add_button("Stop", stop_watch, 100)
frame.add_button("Reset", reset_watch, 100)
timer = simplegui.create_timer(100, tick)

# start frame
frame.start()


# Please remember to review the grading rubric
