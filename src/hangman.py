'''Hang man game'''
import random
from hangman_ascii import ascii_art


class hangman_game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.word = None
        self.letters_left = None
        self.display = None
        self.guess_left = 0
        self.game_active = False
        self.guesses = None

    '''Sets chosen word'''
    def set_word(self, string):
        #only takes lower case
        self.word = list(string.lower())
    
    def get_word(self):
        return " ".join(self.word)

    '''Gets a random word'''
    def get_random_word(self):
        lines = open("hangman_words.txt").read().splitlines()
        return random.choice(lines)

    '''Starts a game.'''
    def start_game(self):
        #Checks error
        if self.word is None:
            return False
        elif self.game_active:
            return False

        self.game_active = True
        self.guess_left = 7
        self.display = list('_' * len(self.word))
        self.letters_left = len(self.word)
        self.guesses = []

        return True
    
    def get_display(self):
        return " ".join(self.display)

    def get_guess_left(self):
        return self.guess_left
    
    '''Makes a guess'''
    def guess(self, string):
        if not string.isalpha():
            return False
        if not self.game_active:
            return False
        if len(string) != 1:
            return False
        
        #Convert to lower
        string = string.lower()

        letter_found = False

        #Loops through and change
        for i in range(len(self.word)):
            if self.word[i] == string:
                letter_found = True
                self.letters_left -= 1
                self.display[i] = string
        
        if not letter_found:
            self.guess_left -= 1
        
        self.guesses.append(string)

        return True
    
    '''Returns the guessed letters'''
    def get_guesses(self):
        return " ".join(self.guesses)


    def game_state(self):
        if self.letters_left == 0:
            return "WON"
        elif self.guess_left == 0:
            return "LOST"
        return "PLAYING"

    def get_ascii(self):
        return ascii_art[7 - self.get_guess_left()]

    def get_message(self):
        ascii_pic = self.get_ascii()
        display = self.get_display()
        output = "Guesses left: " + str(self.get_guess_left())
        words_guessed = self.get_guesses()
        return ascii_pic + display + "\n" + output + "\n" + "Guesses: " +words_guessed


if __name__ == "__main__":
    hangman = hangman_game()
    hangman.set_word(hangman.get_random_word())
    hangman.start_game()

    while hangman.game_state() == "PLAYING":
        print(hangman.get_message())
        guess = input("make your guess: ")
        if not hangman.guess(guess):
            print("Invalid input")
    print(hangman.get_ascii())
    print(hangman.get_word())
    print("You have " + hangman.game_state())