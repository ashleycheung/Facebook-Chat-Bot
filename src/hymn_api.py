import requests

class hymn_api:
    def get_hymn(self, query, num = 5):
        get_link = "https://hymnary.org/api/scripture"
        params = {
            "reference" : query,
        }
        response = requests.get(get_link, params=params)
        output = response.json()

        if len(output) == 0:
            return "No hymns found"

        output_str = ""

        if num > len(output):
            num = len(output)

        for i in range(num):
            hymn_key = list(output.keys())[i]
            hymn_ref = output[hymn_key]["scripture references"]
            hymn_result = "Hymn: " + hymn_key + ",\n" + "references:" + hymn_ref + "\n"
            output_str = output_str + hymn_result + "\n"

        return output_str

if __name__ == "__main__":
    hymn = hymn_api()
    print("search hymn")
    while True:
        query = input("search: ")
        response = hymn.get_hymn(query)
        print("bot: " + response)