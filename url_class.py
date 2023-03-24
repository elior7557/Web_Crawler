import os
import requests
from bs4 import BeautifulSoup
import re


class Url:

    def __init__(self, url, maximal_amount=1, depth=0):
        self.url = url
        self.depth = str(depth)
        self.current_depth = 0

    def get_valid_file_name(self):
        """
        The function validates the URL before saving the file
        remove https from the begging 
        <depth>/<url>.html
        the url must not contain: /   ? * '' < > 
        if any of illegar charactes apper it is replaced with _ 
        """
        valid_url = re.sub(r"https?://", '', self.url)
        valid_url = re.sub(r'[<>\.:\"/\\|?*]', '_', valid_url) #regex to match all illegar characters in a file
        if valid_url[-1] == '_':
            valid_url = valid_url[:-1] # remove the / at the end of a url
        return valid_url

    def create_folders(self):
        for folder_name in range(int(self.depth) + 1):
            if not os.path.exists(str(folder_name)):
                print("creting a folder")
                os.mkdir(str(folder_name))

    def scan_and_save_page(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        # print(soup.prettify())
        return soup

    def create_file(self):
        file_path = f"{self.current_depth}/{self.get_valid_file_name()}.html"
        print(file_path)
        with open(f"{file_path}", "w", encoding='utf-8') as file:
            soup = self.scan_and_save_page()
            file.write(str(soup.prettify()))

    def run(self):
        self.create_folders()
        self.create_file()