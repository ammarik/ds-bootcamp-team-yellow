"""ToDo"""
import csv
from os import error
from lxml import etree
from urllib.request import urlopen

from PIL import Image
import requests
from io import BytesIO

class MovieInfoSource:
    
    MOVIES = './data/movies.csv'
    LINKS = './data/links.csv'

    LINK_PREFIX = 'https://www.imdb.com/title/tt'
    
    def __init__(self):

        self.movies_info = []

        with open(self.MOVIES) as movies_file, open(self.LINKS) as links_file:
            movies_file_reader = csv.reader(movies_file, delimiter=',')
            links_file_reader = csv.reader(links_file, delimiter=',')
            for movie_row, link_row in zip(movies_file_reader, links_file_reader):
                self.movies_info.append((movie_row[1], link_row[1]))
        

    def get_movie_name(self, movie_id):
        return self.movies_info[movie_id][0]

    def get_movie_info(self, movie_id): 
        movie_url = self.LINK_PREFIX + self.movies_info[movie_id][1] + '/'
        
        usock = urlopen(movie_url)
        data = usock.read()
        usock.close()

        # Define custom parser that ignores errors when the html is non-valid
        parser = etree.XMLParser(recover=True)
        # Parse html source using the parse
        root = etree.fromstring(data, parser=parser)

        description = self._get_movie_description(root)
        img = self._get_movie_image(root)
        
        return description, img

    def _get_movie_image(self, root):
        
        results = root.xpath("//meta[@property='og:image']/@content")
        if len(results) < 1:
            return None
        
        image_url = results[0]
        
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        return img


    def _get_movie_description(self, root):
        description = ''

        # Get movie description 
        results = root.xpath("//meta[@name='description']/@content")

        if len(results) > 0:
            description = results[0]

        return  description