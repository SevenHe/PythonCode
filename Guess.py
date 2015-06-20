# Running in CodeSkulptor is successful!

import simplegui
import math
import random

secret_number = 0
guesses = -1             # -1 for game ends with no guesses and start another game normally
num_range = 100

def new_game():
    global secret_number, guesses
    if guesses == -1:
        print ""
        print "New game, range is from 0 to 100"
        secret_number = random.randrange(0, 100)
    if num_range == 100:
        guesses = 7
        print "Number of remaining guesses is ", guesses
    elif num_range == 1000:
        guesses = 10
        print "Number of remaining guesses is ", guesses
    else:
        print "Random Number Error !"
        
def range100():
    global secret_number, num_range
    print ""
    print "New game, range is from 0 to 100"
    secret_number = random.randrange(0, 100)
    num_range = 100
    new_game()
    
def range1000():
    global secret_number, num_range
    print ""
    print "New game, range is from 0 to 1000"
    secret_number = random.randrange(0, 1000)
    num_range = 1000
    new_game()
    
    
def input_guess(guess):
    guess = int(guess)
    print ""
    print "Guess was ", guess
    global secret_number, guesses
    if guess > secret_number and guesses != 0:
        print "Lower!"
        guesses -= 1
        print "Number of remaining guesses is ", guesses
    elif guess < secret_number and guesses != 0:
        print "Higher!"
        guesses -= 1
        print "Number of remaining guesses is ", guesses
    elif guess == secret_number and guesses != 0:
        print "Correct!!"
        guesses = -1
        new_game()
    if guesses == 0:
        print "You ran out of guesses!"
        print "The number is ", secret_number, "."
        guesses = -1
        new_game();

f = simplegui.create_frame("Guess the number", 200, 200)

f.add_button("Range is [0, 100)", range100, 200)
f.add_button("Range is [0, 1000)", range1000, 200)
f.add_input("Enter a guess", input_guess, 200)

new_game()
