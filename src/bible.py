#https://api.scripture.api.bible/v1

#american standard version bible id
#06125adad2d5898a-01

import requests
import bible_api_const
from data import bible_data

header = {
    "api-key" : bible_data["bible_api_key"]
}

class bible_api:
    '''Constructor'''
    def __init__(self, api_key):
        self.headers = {
            "api-key" : api_key
        }
        self.bible_id = "06125adad2d5898a-01"
    
    '''Returns a list of books in the bible'''
    def get_books(self):
        get_link = f"https://api.scripture.api.bible/v1/bibles/{self.bible_id}/books"
        output = requests.get(get_link, headers=self.headers)
        return output.json()
    
    '''Returns a list of book ids'''
    def get_books_id(self):
        books = self.get_books()
        output_list = []
        for book in books["data"]:
            output_list.append(book["id"])
        return output_list
        
    '''Returns passages'''
    def get_passage(self, passage):
        get_link = f"https://api.scripture.api.bible/v1/bibles/{self.bible_id}/passages/{passage.upper()}"

        params = {
            "content-type" : "text"
        }

        output = requests.get(get_link, headers=self.headers, params=params)
        return output.json()["data"]["content"]
    
    def search(self, search_terms):
        get_link = f"https://api.scripture.api.bible/v1/bibles/{self.bible_id}/search"

        params = {
            "query" : search_terms,
            "limit" : 1,
        }

        output = requests.get(get_link, headers=self.headers, params=params)

        search_verses = output.json()["data"]["verses"]
        
        #No search results found
        if not len(search_verses):
            return "No search result found"

        verse = search_verses[0]
        
        return self.keyMap(verse["id"]) + " : " + verse["text"]

    #Converts short chapter to full chapter
    def keyMap(self, string):
        chapter = string[3:]
        book = string[0:3]
        if book in bible_api_const.book_id_map:
            book = bible_api_const.book_id_map[book]
        else:
            return string
        return book + chapter


if __name__ == "__main__":
    bible = bible_api(bible_data["bible_api_key"])
    passage = input("What passage?")
    print(bible.get_passage(passage))
