from bs4 import BeautifulSoup
import requests
import re
import textwrap


# must pass in url and head as strings
def scrape(URL, head):
    html_text = requests.get(URL).text
    soup = BeautifulSoup(html_text, 'lxml')

    # finds the header in the wiki page that matches the input for 'head' and appends to output array
    output = []
    header = soup.find('span', class_='mw-headline', text=head)
    output.append(header.text)

    # Jumps to next paragraph tag to avoid adding unnecessary info from wiki page and appends
    para = header.find_next('p')
    output.append(para.text)

    # Runs on a loop checking next elements tag.  As long as next tag isn't 'h2' (next header), it changes value
    # of para and appends to output.  If it is 'h2', break
    while True:
        if para.find_next().name != 'h2':
            para = para.find_next()
            output.append(para.text)
        else:
            break

    # Cleaning up the output
    output = ' '.join(output)
    output = re.sub(r"\[.*?\]+", '', output)
    output = output.replace('\n', '')[:-11]
    print(textwrap.fill(output, 70))

    # Still need to write this output to a file (?)


if __name__ == '__main__':
    scrape('https://en.wikipedia.org/wiki/Blackjack', 'Rules')
