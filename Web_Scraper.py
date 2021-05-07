from bs4 import BeautifulSoup
import requests
import re
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import urlopen
import sys
import json


# must pass in url and head as strings
def scrape(URL, head):
    # Checking for good URL
    try:
        urlopen(URL)
    except HTTPError as e:
        sys.stderr.write(str(e))
        return
    except URLError:
        sys.stderr.write("Website cannot be reached")
        return

    html_text = requests.get(URL).text
    soup = BeautifulSoup(html_text, 'lxml')

    # Finds the header in the wiki page that matches the input for 'head' and appends to output array
    output = []
    # json_out = BeautifulSoup("<h2>"+head+"</h2>", 'html.parser')
    header = soup.find('span', class_='mw-headline', text=head)

    # Lets user know if incorrect header name
    try:
        header.text
    except AttributeError:
        sys.stderr.write("Header \"" + head + "\" does not exist in the URL provided")
        return

    # output.append(":")

    # Jumps to next paragraph tag to avoid adding unnecessary info from wiki page and appends
    para = header.find_parent().find_next_sibling()
    output.append(re.sub(r"\[[0-9]*?\]", '', para.text))
    # json_out.append(para)

    # Runs on a loop checking next elements tag.  As long as next tag isn't 'h2' (next header), it changes value
    # of para and appends to output.  If it is 'h2', break
    while True:
        if para.find_next_sibling().name != 'h2':
            para = para.find_next_sibling()
            output.append(re.sub(r"\[[0-9]*?\]", '', para.text))
            # json_out.append(para)
        else:
            break

    # Convert to JSON
    dd = {head: output}
    json_object = json.dumps(dd)
    sys.stdout.write(json_object)
    # output = re.sub(r"\[.*?\]+", '', output)
    # output = output.replace('\n', '')[:-11]


if __name__ == '__main__':
    if len(sys.argv) == 3:
        url_str = sys.argv[1]
        header_str = sys.argv[2]
        scrape(url_str, header_str)
    else:
        sys.stderr.write("::ERROR::")
    sys.stdout.flush()
    sys.stderr.flush()
