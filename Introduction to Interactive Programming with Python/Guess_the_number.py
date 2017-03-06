import simplegui
import random

range_max = int(100)
guess_max = int(7)

# helper function to start and restart the game
def new_game():
    global secret_number
    global remain_guess
    global range_max
    global guess_max
    secret_number = random.randint(0,range_max)
    remain_guess = guess_max
    print 'New game with range 1-' + str(range_max)
    print

# define event handlers for control panel
def range100():
    global range_max
    global guess_max
    range_max = int(100)
    guess_max = int(7)
    new_game()


def range1000():
    global range_max
    global guess_max
    range_max = int(1000)
    guess_max = int(10)
    new_game()

    
def input_guess(guess):
    guess_num = int(guess)
    print "Guess was: " + guess
    global remain_guess
    remain_guess = remain_guess - 1
    if remain_guess > 0:
            if guess_num < secret_number:
                print 'Higher'
                print str(remain_guess) + " guesses remain"
                print
            elif guess_num > secret_number:
                print 'Lower'
                print str(remain_guess) + " guesses remain"
                print
            else:
                print 'Correct'
                new_game()
    elif remain_guess == 0:
            if guess_num < secret_number:
                print 'Higher'
                print "Sorry, you've run out of guesses!"
                print
                new_game()
            elif guess_num > secret_number:
                print 'Lower'
                print "Sorry, you've run out of guesses!"
                print
                new_game()
            else:
                print 'Correct'
                new_game()
    
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Get range 0-100", range100, 200)
frame.add_button("Get range 0-1000", range1000, 200)
frame.add_input("Enter guess!", input_guess, 200)

frame.start()

# call new_game
new_game()


