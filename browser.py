import sys
import os
import requests
from bs4 import BeautifulSoup
from collections import deque
from colorama import Fore


# write your code here


args = sys.argv
director = args[1]

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/70.0.3538.77 Safari/537.36"


def main():
    back_stack = deque()

    if not os.path.exists(director):
        os.makedirs(director, exist_ok=True)

    while True:
        url = input(">")
        file_name = url
        browser_url = url

        if browser_url == 'exit':
            exit()
        # use stack to release "back button"
        # if "back" is written so in console will show previous tab
        if browser_url == 'back':
            back_stack.pop()
            print(back_stack.pop())

        # try to correct user input url
        if browser_url[:7] != 'https://':
            browser_url = 'https://' + browser_url
        else:
            file_name = file_name[7:]

        # search all "info" tags and pars its from site then write in directory
        # where file is entitled as url
        try:
            page = requests.get(browser_url, headers={'User-Agent': user_agent})
            soup = BeautifulSoup(page.content, 'lxml')
            tags_list = soup.find_all(['p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li'])

            with open(f".\\{director}\\{file_name}.txt", 'w', encoding='UTF-8') as f:
                for tag in tags_list:
                    temp_tag = tag
                    if temp_tag:
                        temp_tag = str(temp_tag)
                        if temp_tag.startswith('<a'):
                            print(Fore.BLUE + tag.text.strip())
                        else:
                            print(tag.text.strip())
                        line = tag.text.strip()
                        f.write(line + '\n')
        except (OSError, ConnectionError):
            print("Incorrect URL")


if __name__ == '__main__':
    main()
