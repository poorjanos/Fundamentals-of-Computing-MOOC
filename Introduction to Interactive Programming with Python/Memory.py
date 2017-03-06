# implementation of card game - Memory

import simplegui
import random

deck = range(0,8) + range(0,8)
turned_first_pos = int() #list.append works too, but this two integer solution is more transaparent
turned_second_pos = int()
turn_count = 0

# helper function to initialize globals
def new_game():
    global deck, state, exposed, turn_count
    random.shuffle(deck)
    exposed = [False for i in range(16)]
    state = 0  
    turn_count = 0
    label.set_text("Turn: " + str(turn_count))

# define event handlers
def mouseclick(pos):
    global state, exposed, turned_first_pos, turned_second_pos, turn_count
    # add game state logic here
    click_where = list(pos)
    if state == 0:
        state = 1
        exposed[pos[0] // 50] = True
        turned_first_pos = pos[0] // 50
    elif state == 1:
        if turned_first_pos != pos[0] // 50: #doubleclick on the same card makes no error
            state = 2
            exposed[pos[0] // 50] = True
            turned_second_pos = pos[0] // 50
            #count turns:
            turn_count += 1
            label.set_text("Turn: " + str(turn_count))
    else:
        state = 1
        if deck[turned_first_pos] != deck[turned_second_pos]:
            exposed[turned_first_pos] = False
            exposed[turned_second_pos] = False
            exposed[pos[0] // 50] = True
            turned_first_pos = pos[0] // 50
        else:
            turned_first_pos = pos[0] // 50
            exposed[pos[0] // 50] = True
  
# cards are logically 50x100 pixels in size    
def draw(canvas):
    num_pos = [0, 80]
    rect_pos = [[0, 0], [0, 100], [50, 100], [50, 0]]
    for i in range(16):
        if exposed[i]:
            canvas.draw_text(str(deck[i]), num_pos, 90, 'White', 'sans-serif')
        else:
            canvas.draw_polygon(rect_pos, 1, 'Black', 'Green')
        num_pos[0] += 50
        for j in range(len(rect_pos)):
            rect_pos[j][0] += 50
            
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turn:")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
