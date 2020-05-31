
#
# The classic game of MANCALA
#
# Author: John R.Pappenheim
# 5/20/2020
#
import random
import sys

def display_board():
    """
    Print a representation of the Mancala board.
    """
    print()
    backwards = [0,0,0,0,0,0]
    for i in range(6):
        backwards[i] = computers_row[5-i]
    print("     ",end='')
    for i in range(6):
        if backwards[i] < 10:
            b = " " + str(backwards[i])
        else:
            b = str(backwards[i])
        print(b, end=' ')
    print()
    print(computers_home, "                    ", humans_home)
    print("     ",end='')
    for i in range(6):
        if humans_row[i] < 10:
            b = " " + str(humans_row[i])
        else:
            b = str(humans_row[i])
        print(b, end=' ')
    print()

def copy_board():
    """
    Preserve the state of the board in order to restore it later.
    """
    for i in range(6):
        computers_row_copy[i] = int(computers_row[i])
        humans_row_copy[i] = int(humans_row[i])
    computers_home_copy[0] = computers_home[0]
    humans_home_copy[0] = humans_home[0]
    return

def restore_board():
    """
    Restore the board to a previous state.
    """
    for i in range(6):
        computers_row[i] = int(computers_row_copy[i])
        humans_row[i] = int(humans_row_copy[i])
    computers_home[0] = computers_home_copy[0]
    humans_home[0] = humans_home_copy[0]
    return

def computer_move(position, value):
    """
    Determine the best move of all available moves the computer can make.
    """
    pebbles = computers_row[position]
    computer_free_turn = False
    if pebbles == 0:                                # This is an empty pot.
        value = -1
        return(value, computer_free_turn)           # Empty pot, just return.
    hand = computers_row[position]                  # Pick up all pebbles from the position.
    computers_row[position] = 0                     # Remove pebbles from the position.
    for pot in range(position + 1, 6):              # Each pot from position to end of row.
        if hand > 0:
            computers_row[pot] = computers_row[pot] + 1 # Drop a pebble in the next pot.
            hand = hand - 1                             # Remove a pebble from your hand.
            if hand <= 0:                               # If you have run out of pebbles ?
                if computers_row[pot] == 1:             # If you ended in your empty pot ?
                    if humans_row[5 - pot] > 0:         # If humans opposite pot has any pebbles in it.
                        computers_home[0] = computers_home[0] + humans_row[5 - pot] + 1 # collect humans pebbles from opposite pot.
                        value = value + humans_row[5 - pot] + 1 # Increase value of this move.
                        humans_row[5 - pot] = 0             # Remove humans pebbles from opposite pot.
                        computers_row[pot] = 0
                return value, computer_free_turn
    if hand > 0:
        computers_home[0] = computers_home[0] + 1   # Drop pebble in your home pot.
        hand = hand - 1                             # Remove a pebble from your hand.
        value = value + 1                           # A pebble was added to your home.
    if hand <= 0:                                   # If you have run out of pebbles, you get a free turn.
        computer_free_turn = True
        return value, computer_free_turn
    for pot in range(6):                            # Start dropping in Humans row of pots.
        humans_row[pot] = humans_row[pot] + 1       # Drop a pebble in the next pot.
        hand = hand - 1                             # Remove a pebble from your hand.
        if hand <= 0:                               # If you have run out of pebbles, you're done
            return value, computer_free_turn
    if hand <= 0:                                   # If you have run out of pebbles, you're done
        return value, computer_free_turn
    for pot in range(6):                            # You have some pebbles left, keep going.
        computers_row[pot] = computers_row[pot] + 1 # Drop a pebble in the next pot.
        hand = hand - 1                             # Remove a pebble from your hand.
        if hand <= 0:                               # If you have run out of pebbles ?
            if computers_row[pot] == 1:             # If you ended in your empty pot ?
                if humans_row[5 - pot] != 0:
                    computers_home[0] = computers_home[0] + humans_row[5 - pot] # collect humans pebbles from opposite pot.
                    value = value + humans_row[5 - pot] # Increase value of this move.
                    humans_row[5 - pot] = 0         # Remove humans pebbles from opposite pot.
            return value, computer_free_turn
    if hand <= 0:
        return value, computer_free_turn
    humans_home[0] = humans_home[0] + 1             # You have some pebbles left, keep going.
    hand = hand - 1                                 # Drop one in the Humans home pot.
    if hand <= 0:                                   # If you have run out of pebbles, you're done
        return value, computer_free_turn
    computers_home[0] = computers_home[0] + 1       # Drop pebble in your home pot.
    hand = hand - 1                                 # Remove a pebble from your hand.
    value = value + 1                               # A pebble was added to your home.
    if hand <= 0:                                   # If you have run out of pebbles, you're done.
        return value, computer_free_turn
    for pot in range(6):                            # Start dropping in Humans row of pots.
        humans_row[pot] = humans_row[pot] + 1       # Drop a pebble in the next pot.
        hand = hand - 1                             # Remove a pebble from your hand.
        if hand <= 0:                               # If you have run out of pebbles, you're done
            return value, computer_free_turn
    if hand <= 0:                                   # If you have run out of pebbles, you're done
        return value, computer_free_turn
    print()
    print("I can't believe you got this far")
    print()
    return value, computer_free_turn

def humans_move(position):
    """
    Make the move that the human specified.
    """
    repeat = False
    humans_free_turn = False
    hand = humans_row[int(position)]            # Pick up all pebbles from this row.
    while hand > 0:                             # While there are still pebbles in your hand, continue.
        if repeat == False:                     # If not going around the second time.
            humans_row[position] = 0            # Remove the pebbles from this pot.
            start = position + 1
        if repeat == True:
            start = 0
        for i in range(start, 6):        # Starting in the next pot...
            if hand >= 1:                       # If you have any pebbles left in your hand.
                hand = hand - 1                 # Remove a pebble from your hand.
                humans_row[i] = humans_row[i] + 1 # Drop the pebble into the pot.
                if hand == 0:                   # was that your last pebble?
                    break                       # Stop this loop
        if hand <= 0:                           # If you have dropped your last pebble.
            if humans_row[i] == 1:              # If this WAS an empty pot.
                if computers_row[5 - i] > 0:    # If computers opposite pot has some pebbles in it.
                    humans_home[0] = humans_home[0] + computers_row[5 - i] + 1 # Collect his pebbles and yours.
                    humans_row[i] = 0           # Remove your pebble.
                    computers_row[5 - i] = 0    # Remove his pebbles.
                    return humans_free_turn     # Your done with this move.
        if hand >= 1:                           # If you have some pebbles left in your hand.
            humans_home[0] = humans_home[0] + 1 # Drop a pebble into your home pot as you round the corner.
            hand = hand - 1                     # Remove that pebble from your hand.
            if hand == 0:                       # If you have dropped all your pebbles.
                humans_free_turn = True         # Last pebble went into your home. You get a free turn.
                return humans_free_turn         # Done with this move.
        if hand > 0:                            # If you have pebbles left in you hand.
            for i in range(0, 6):               # Start dropping them in his row.
                if hand <= 0:                   # If you have run out of pebbles.
                    return humans_free_turn     # Done with this move.
                hand = hand - 1                 # Remove a pebble from your hand.
                computers_row[i] = computers_row[i] + 1 # Drop the pebble into his pot.
        if hand > 0:                            # IF you still have pebbles in your hand.
            position = 0                        # Prepare to go down your row again if you still have pebbles.
            repeat = True
    return(humans_free_turn)                    # Done with this move.

def is_game_over():
    """
    Determine if the game is over, and if so ask to play again.
    """
    done = False
    game_over = True
    for i in range(0,6):
        if computers_row[i] != 0:
            game_over = False
    if not game_over:
        game_over = True
        for i in range(0,6):
            if humans_row[i] != 0:
                game_over = False
    if game_over:
        print()
        print("GAME OVER")
        if computers_home[0] > humans_home[0]:
            print("Computer wins!")
        if humans_home[0] > computers_home[0]:
            print("You win!")
        if computers_home[0] == humans_home[0]:
            print("It's a tie!")
        done = True
        valid = False
        while not valid:
            again = input("Play again ?")
            if again == "":
                again = " "
            again = again.lower()
            if again[0] == "y":
                valid = True
                main()
            if again[0] == "n":
                sys.exit(0)
            else:
                print("Please answer 'y' or 'n'.")
                valid = False
        sys.exit(0)
    return

def main():
    """
    This is tha main loop for playing the game of Mancala.
    """
    global computers_row_copy
    global computers_row
    computers_row = [4, 4, 4, 4, 4, 4]
    computers_row_copy = [4, 4, 4, 4, 4, 4]
    global computers_home_copy
    global computers_home
    computers_home = [0]
    computers_home_copy = [0]
    global humans_row_copy
    global humans_row
    humans_row = [4, 4, 4, 4, 4, 4]
    humans_row_copy = [4, 4, 4, 4, 4, 4]
    global humans_home_copy
    global humans_home
    humans_home = [0]
    humans_home_copy = [0]
    choices = [True, False]
    computer_turn = random.choice(choices)
    done = False
    display_board()
    best_move = 0
    while not done:
        if computer_turn:
            copy_board()
            best = -1
            computer_free_turn = True
            while computer_free_turn:
                for position in range(6):       # Look for best move.  0 through 5
                    computer_free_turn = True
                    value = 0
                    # while computer_free_turn:
                    value, computer_free_turn = computer_move(position, value)
                    restore_board()
                    if value > best:
                        best = value
                        best_move = position
                computer_free_turn = True
                value = 0
                value, computer_free_turn = computer_move(best_move, value)
                x = input("Press 'Enter' to continue")
                print("This is computer's move.")
                display_board()
                is_game_over()
                if computer_free_turn:
                    print("Computer gets a FREE turn.")
                    copy_board()
                    best = -1
                    best_move = 0
            is_game_over()

        # your turn
        if is_game_over():
            break
        humans_free_turn = True
        while humans_free_turn:
            humans_free_turn = False
            ok = False
            while not ok:
                human_move = input("Your turn: ")
                if human_move.isdigit():
                    human_move = int(human_move)
                    if human_move < 7 and human_move > 0:
                        human_move = human_move - 1
                        if humans_row[human_move] > 0:
                            ok = True
                if not ok:
                    print("That's an illegal move")
                else:
                    humans_free_turn = humans_move(human_move)
                    print("This is your move.")
                    display_board()
                    if is_game_over():
                        break
                    if humans_free_turn:
                        print("You get a FREE turn.")
                    ok = True
        computer_turn = True
        continue

if __name__ == "__main__":
    main()
