import requests
from data import youtube_data

key = youtube_data["youtube_api_key"]

class youtube_api:
    def search(self, search_str, raw = False):
        get_link = "https://www.googleapis.com/youtube/v3/search"

        params = {
            "key": key,
            "maxResults" : 1,
            "safeSearch" : "moderate",
            "q" : search_str,
            "type" : "video",
        }
        response = requests.get(get_link, params=params)
        output = response.json()

        if raw:
            return str(output)

        try:
            video_id = output["items"][0]["id"]["videoId"]
        except:
            return "No video found"

        watch_link = "https://www.youtube.com/watch"+ "?v=" + video_id
        
        return "Search result for " + search_str + ": \n" + watch_link

if __name__ == "__main__":
    youtube = youtube_api()
    print("Type search term")
    while True:
        search = input("Search term: ")
        print(youtube.search(search, raw = True))