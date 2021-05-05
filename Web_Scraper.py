from bs4 import BeautifulSoup
import requests
import re
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import urlopen

# must pass in url and head as strings
def scrape(URL, head):
    # Checking for good URL
    try:
        urlopen(URL)
    except HTTPError as e:
        print(e)
        exit()
    except URLError:
        print("Website cannot be reached")
        exit()

    html_text = requests.get(URL).text
    soup = BeautifulSoup(html_text, 'lxml')

    # Finds the header in the wiki page that matches the input for 'head' and appends to output array
    output = []
    # json_out = BeautifulSoup("<h2>"+head+"</h2>", 'html.parser')
    header = soup.find('span', class_='mw-headline', text=head)

    # Lets user know if incorrect header name
    try:
        output.append(header.text)
    except AttributeError:
        print("Header \"" + head + "\" does not exist in the URL provided")
        exit()

    output.append(":")

    # Jumps to next paragraph tag to avoid adding unnecessary info from wiki page and appends
    para = header.find_parent().find_next_sibling()
    output.append(para.text)
    # json_out.append(para)

    # Runs on a loop checking next elements tag.  As long as next tag isn't 'h2' (next header), it changes value
    # of para and appends to output.  If it is 'h2', break
    while True:
        if para.find_next_sibling().name != 'h2':
            para = para.find_next_sibling()
            output.append(para.text)
            #json_out.append(para)
        else:
            break

    # Cleaning up the output
    output = ' '.join(output)
    #output = re.sub(r"\[.*?\]+", '', output)
    output = re.sub(r"\[[0-9]*?\]", '', output)
    #output = output.replace('\n', '')[:-11]

    # Write output to a file
    f = open("wikiscrape.txt", "w")
    f.write(output)

    # Report successful search to user
    print("Web Scraper Success")




if __name__ == '__main__':
    scrape('https://en.wikipedia.org/wiki/Blackjack', 'Rules')
