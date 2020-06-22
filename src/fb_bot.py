#Written by Ashley 
import json
from data import bot_data, fb_data
from bot_core import bot_class
import fbchat
from fbchat.models import Message, ThreadType

'''This is a wrapper class for fb client'''
class fb_client:
    '''Constructor'''
    def __init__(self, data):
        self.email = data["email"]
        self.password = data["password"]

        #Load cookies
        cookies = self._get_session_cookies()
        #Create client
        self.client = custom_client(self.email, self.password, session_cookies=cookies)
        self.client.connect_bot(bot_data)
    
    def listen(self):
        self.client.listen()

    '''Returns cookies if there is one'''
    def _get_session_cookies(self):
        cookies = {}
        try:
            # Load the session cookies
            with open('session.json', 'r') as f:
                cookies = json.load(f)
            print("Loaded from cookies successfully")
        except:
            # If it fails, never mind, we'll just login again
            print("Loaded from cookies failed")
        return cookies

    '''Send a message to self'''
    def send_to_self(self, message):
        self.client.send(Message(text=message), thread_id=self.client.uid, thread_type=ThreadType.USER)
    
    '''logs out'''
    def logout(self):
        #Log out of client
        #Note: logging out resets cookies
        self.client.logout()
    
    '''Saves the cookies'''
    def save_session(self):
        # Save the session again
        with open('session.json', 'w') as f:
            json.dump(self.client.getSession(), f)
            print("json stored")

'''Custom client of fb chat'''
class custom_client(fbchat.Client):
    bot = None
    '''Connects it to a bot'''
    def connect_bot(self, data):
        self.bot = bot_class(data)

    '''on message'''
    def onMessage(self, message_object, author_id, thread_id, thread_type, **kwargs):
        #Not own message
        if message_object.author != self.uid:
            #In a dm
            if thread_type == ThreadType.USER:
                print(message_object.text)
                self.send_bot_response(message_object, thread_id, thread_type)
            elif thread_type == ThreadType.GROUP:
                #Check if the bot is mentioned
                for mention in message_object.mentions:
                    if mention.thread_id == self.uid:
                        message_object.text = self._filter_message(message_object.text)
                        print(message_object.text)
                        self.send_bot_response(message_object, thread_id, thread_type)
                        break
    
    '''Filters out the mention'''
    def _filter_message(self, message_str):
        return message_str.replace("@Cashley Bashkey", "")

    '''Send a bot response to a certain thread'''
    def send_bot_response(self, message_object, thread_id, thread_type):
        #Formulate response
        if self.bot is None:
            raise SystemError
        response = self.bot.get_response(message_object.text)
        response_message = Message(text=response)
        self.send(response_message, thread_id=thread_id, thread_type=thread_type)



if __name__ == '__main__':
    fb = fb_client(fb_data)
    fb.save_session()
    fb.listen()