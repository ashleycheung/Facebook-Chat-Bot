#Written by Ashley 
import os
import random
import dialogflow
from data import bot_data, bible_data
from bible import bible_api
from hymn_api import hymn_api
from youtube_api import youtube_api
from google.api_core.exceptions import InvalidArgument
from hangman import hangman_game

'''This is the main class for the bot'''
class bot_class:
    '''Constructor'''
    def __init__(self, data):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'
        self.DIALOGFLOW_PROJECT_ID = data["DIALOGFLOW_PROJECT_ID"]
        self.DIALOGFLOW_LANGUAGE_CODE = data["DIALOGFLOW_LANGUAGE_CODE"]
        self.SESSION_ID = data["SESSION_ID"]
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(self.DIALOGFLOW_PROJECT_ID, self.SESSION_ID)
        self.bible = bible_api(bible_data["bible_api_key"])
        self.hymn = hymn_api()
        self.youtube = youtube_api()
        self.hangman = None

    '''Gets a response given a string'''
    def get_response(self, string):
        if string == '':
            return ""
        elif string[0] == '/':
            return self.get_builtin(string)
        else:
            return self.get_dialogflow(string)
    
    '''Refers to dialogflow for response'''
    def get_dialogflow(self, string):
        #Create text input
        text_input = dialogflow.types.TextInput(text=string, language_code=self.DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)

        #Get response
        try:
            response = self.session_client.detect_intent(session=self.session, query_input=query_input)
        except InvalidArgument:
            raise

        #Return fullfillment text
        return response.query_result.fulfillment_text
    
    '''Gets a hard coded command'''
    def get_builtin(self, string):
        #Split string
        split_string = string.split()
        if split_string[0] == "/bible":
            return self.bible_methods(split_string[1:])
        
        elif split_string[0] == "/youtube":
            return self.youtube_methods(split_string[1:])
        
        elif split_string[0] == "/help":
            return HELP_MSG
        
        elif split_string[0] == "/hangman":
            return self.hangman_methods(split_string[1:])

        elif split_string[0] == "/random":
            return self.random_methods(split_string[1:])

        return f'"{split_string[0]}" is not a built in function. Type "/help" for available commands'
    
    '''Runs methods from bible module'''
    def bible_methods(self, param):
        #Empty string
        if param == []:
            return 'No "/bible" command given'

        #Passage get
        elif param[0:2] == ["passage","get"]:
            try:
                return self.bible.get_passage(param[2])
            except:
                return "Could not find verse :C"

        #Get passage ids
        elif param[0:3] == ["book","get","ids"]:
            #Returns the list as a string
            return " ".join(self.bible.get_books_id())
        
        elif param[0] == "search":
            if len(param) == 1:
                return "No search term given"
            return self.bible.search(" ".join(param[1:]))

        elif param[0] == "hymn":
            if len(param) == 1:
                return "No search passage given"
            return self.hymn.get_hymn(" ".join(param[1:]))

        return f'"{param[0]}" is not a builtin bible command. Type "/help" for available commands'

        '''Responsible for /youtube methods'''
    def youtube_methods(self, param):
        if param == []:
            return 'No "/youtube" command given'

        elif param[0] == "search":
            return self.youtube.search(" ".join(param[1:]))

        return f'"{param[0]}" is not a builtin youtube command. Type "/help" for available commands'

    def hangman_methods(self, param):
        if param == []:
            return "No /hangman command given"

        if param[0] == "start":
            if self.hangman is None:
                self.hangman = hangman_game()
                self.hangman.set_word(self.hangman.get_random_word())
                self.hangman.start_game()
                return self.hangman.get_message()
            else:
                return "Game already exists"
        elif self.hangman is None:
            return 'No active hangman game. Type "/hangman start" to start game'
        
        #Game must exist already then
        if len(param) == 1 and param[0].isalpha():
            if not self.hangman.guess(param[0]):
                return "Invalid guess"
                #Game finished
            elif self.hangman.game_state() != "PLAYING":
                output = "You have " + self.hangman.game_state()
                output = self.hangman.get_ascii() + output
                output = output + "\nWord: " + self.hangman.get_word()
                self.hangman = None
                return output

            return self.hangman.get_message()
        
        if param[0] == "end":
            word = self.hangman.get_word()
            self.hangman = None
            return "Game ended. Word was " + word

        return f'"{param[0]}" is not a builtin hangman command.'
    
    def random_methods(self, param):
        if param[0] == "dice":
            return "I rolled a " + str(random.randint(1,6))

        return f'"{param[0]}" is not a builtin random command. Type "/help" for available commands'
        
        

        




HELP_MSG = """
    Available commands available:
    /help : for help
    /bible passage get : to get a passage
    /bible search : to search a phrase
    /bible hymn : to get a hymn for a given passage
    /youtube search : to search for a video
    /hangman start: to play hangman
    /random dice: to roll a dice
"""


if __name__ == "__main__":
    new_bot = bot_class(bot_data)
    print("Type to start talking to bot")
    while True:
        query = input("You: ")
        response = new_bot.get_response(query)
        print("bot: " + response)
