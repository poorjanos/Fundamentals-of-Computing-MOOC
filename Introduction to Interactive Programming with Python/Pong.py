# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = True
RIGHT = False
paddle1_pos = 160
paddle2_pos = 160
paddle1_vel = 0
paddle2_vel = 0
score_left = 0
score_right = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    if direction == RIGHT:
        ball_vel = [random.randrange(2, 3), -random.randrange(1, 3)]
    elif direction == LEFT:
        ball_vel = [-random.randrange(2, 4), -random.randrange(1, 3)]
        

# define event handlers
def button_handler():
    new_game()

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score_left, score_right  # these are ints
    paddle1_pos = 160
    paddle2_pos = 160
    paddle1_vel = 0
    paddle2_vel = 0
    score_left = 0
    score_right = 0
    if random.randrange(0,11) % 2 == 0:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, score_right, score_left

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    #collision top-bottom
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT-BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    #collision gutter + determine whether paddle and ball collide + increase speed upon paddle and ball collision    
    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH and (ball_pos[1] < paddle1_pos or ball_pos[1] > paddle1_pos + PAD_HEIGHT):
        spawn_ball(RIGHT)
        score_left += 1
    elif ball_pos[0] <= BALL_RADIUS + PAD_WIDTH and (ball_pos[1] >= paddle1_pos or ball_pos[1] >= paddle1_pos + PAD_HEIGHT):
        ball_vel[0] = -ball_vel[0]*1.1
        
    if ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH and (ball_pos[1] < paddle2_pos or ball_pos[1] > paddle2_pos + PAD_HEIGHT):
        spawn_ball(LEFT)
        score_right += 1
    elif ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH and (ball_pos[1] >= paddle2_pos or ball_pos[1] >= paddle2_pos + PAD_HEIGHT):
        ball_vel[0] = -ball_vel[0]*1.1
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel >= 0 and paddle1_pos + PAD_HEIGHT + paddle1_vel <= 400:
        paddle1_pos += paddle1_vel
    if paddle2_pos + paddle2_vel >= 0 and paddle2_pos + PAD_HEIGHT + paddle2_vel <= 400:
        paddle2_pos += paddle2_vel
    
    
    # draw paddles
    #left
    canvas.draw_line((4, paddle1_pos), (4, paddle1_pos + PAD_HEIGHT), 8, 'White')
    #right
    canvas.draw_line((596, paddle2_pos), (596, paddle2_pos + PAD_HEIGHT), 8, 'White')   
    
    # draw scores
    canvas.draw_text(str(score_right), (200, 30), 20, 'White', 'sans-serif')
    canvas.draw_text(str(score_left), (400, 30), 20, 'White', 'sans-serif')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 2
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    acc = -2
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += acc


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', button_handler)


# start frame
frame.start()
new_game()
