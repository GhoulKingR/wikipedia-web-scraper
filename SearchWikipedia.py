import requests
import json
from bs4 import BeautifulSoup

def get_user_search():
    return input("What do you want to know about? ")

def get_response(user_search):
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=opensearch&format=json&formatversion=2&search={user_search}&namespace=0&limit=10"
        response = requests.get(url).text
        return json.loads(response)
    except:
        choice = input("Could not reach site, do you want to try again (y/n)?")
        if choice.lower() == "y":
            get_response(user_search)
        else:
            exit()


def get_user_choice(results):
    print( "Which do you want to search about?" )
    for indexes in range(0, len(results)):
        print( str(indexes + 1) + ". " + results[indexes])
    choice = int( input("\nYour input <1-10>: ") )
    
    if choice >= 0 and choice <= 10:
        return choice - 1
    else:
        print("invalid input")
        return get_user_choice(results)

def get_page(choice, urls):
    page_url = urls[choice]
    page_result = requests.get(page_url).content
    
    soup = BeautifulSoup(page_result, "html.parser")
    body_content = soup.find("div", id="bodyContent")
    parser_output = body_content.find("div", class_="mw-parser-output")
    introduction = ""

    for p in parser_output.find_all("p"):
        if not p.find_parent("table") and len(p.text.strip()) != 0:
            introduction += p.text
            break

    return (introduction + "\n\nTo learn more visit " + page_url)

if __name__ == "__main__":
    user_search = get_user_search()
    response = get_response(user_search)

    results = response[1]
    urls = response[3] 

    choice = get_user_choice(results)
    page = get_page(choice, urls)
    print(page)
