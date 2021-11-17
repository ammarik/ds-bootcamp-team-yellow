"""Provide more information about the given film."""
import csv
from io import BytesIO
from urllib.request import urlopen

import requests
from lxml import etree
from PIL import Image


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
        """
        Based on the given movie ID, this method returns name 
        of the movie
        """
        return self.movies_info[movie_id][0]

    def get_movie_info(self, movie_id):
        """
        Based on the given movie ID, this method gets a link 
        to the movie on imdb.com, an image of the movie and 
        a basic description of the movie.
        """
        # Get url of the movie at imdb.
        movie_url = self.LINK_PREFIX + self.movies_info[movie_id][1] + '/'
        
        # Get content of the webpage.
        usock = urlopen(movie_url)
        data = usock.read()
        usock.close()

        # Define custom parser that ignores errors when the html is non-valid.
        parser = etree.XMLParser(recover=True)
        # Parse html source using the parser.
        root = etree.fromstring(data, parser=parser)

        # Obtain from the parsed html source movie description and image.
        description = self._get_movie_description(root)
        img = self._get_movie_image(root)
        
        return description, movie_url, img

    def _get_movie_image(self, root):
        """
        Finds movie title image url in the given html tree
        and downloads the image.
        """
        results = root.xpath("//meta[@property='og:image']/@content")
        if len(results) < 1:
            return None
        
        image_url = results[0]
        
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        return img

    def _get_movie_description(self, root):
        """
        Obtains movie description from the given html tree.
        """
        description = ''

        # Get movie description 
        results = root.xpath("//meta[@name='description']/@content")

        if len(results) > 0:
            description = results[0]

        return  description