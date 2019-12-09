import scrapy
from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
import urlparse
import logging

class WikipediaSpider(scrapy.Spider):
    name = 'wikipedia'
    allowed_domains = ['en.wikipedia.org']
    start_urls = [
                    'https://en.wikipedia.org/wiki/List_of_American_films_of_2000',
                    'https://en.wikipedia.org/wiki/List_of_American_films_of_2001',
                    'https://en.wikipedia.org/wiki/List_of_American_films_of_2002',
                    'https://en.wikipedia.org/wiki/List_of_American_films_of_2003',
                    'https://en.wikipedia.org/wiki/List_of_American_films_of_2004',
                    'https://en.wikipedia.org/wiki/List_of_American_films_of_2005',
                    'https://en.wikipedia.org/wiki/List_of_American_films_of_2006',
                    'https://en.wikipedia.org/wiki/List_of_American_films_of_2007',
                    'https://en.wikipedia.org/wiki/List_of_American_films_of_2008',
                    'https://en.wikipedia.org/wiki/List_of_American_films_of_2009',
                    'https://en.wikipedia.org/wiki/List_of_American_films_of_2010',
                    'https://en.wikipedia.org/wiki/List_of_American_films_of_2011',
                    'https://en.wikipedia.org/wiki/List_of_American_films_of_2012',
                    'https://en.wikipedia.org/wiki/List_of_American_films_of_2013',
                    'https://en.wikipedia.org/wiki/List_of_American_films_of_2014',
                    'https://en.wikipedia.org/wiki/List_of_American_films_of_2015',
                    'https://en.wikipedia.org/wiki/List_of_American_films_of_2016'
                 ]
    convert_unit = {
                   "hundred": 100, 
                   "thousand": 1000, 
                   "million": 1000000, 
                   "billion": 1000000000, 
                   "trillion": 1000000000
                   }
    
    """This function parses a page of movies given a url to it.
    We are parsing the table on the Wikipedia page.
    If the table is malformed then we kill the program.
    This function returns void when the page is malformed.
    """
    def parse(self, response):

        logging.info('Visited: ' + response.url)

        try:
            soup = BeautifulSoup(response.text, 'lxml')

            table = soup.find('table', attrs={'class': 'wikitable'})
            
            movie_urls = [] 
            for row in table.find_all('tr')[1:]:
                movie_title = row.find_all('td')[0]
                for movie_url in movie_title.find_all('a'):
                    movie_urls.append(movie_url.get('href'))

            for movie_url in movie_urls:
                url = urlparse.urljoin(response.url, movie_url)
                result = self.parse_movie(url) 
                if(result != -1):
                    yield result
        except:
            logging.error('Cannot visit ' + response.url)
            return

    """This function parses a movie page given a url to it.
    We are parsing the side table on the Wikipedia page.
    If the movie page is malformed then we do not include in our output.
    This function returns -1 when the page is malformed.
    """
    def parse_movie(self, movie_url):
        logging.info('Visited: ' + movie_url)

        soup = BeautifulSoup(urlopen(movie_url), 'lxml')
        
        try:
            infobox = soup.find('table', class_='infobox')
        
            movie_name = infobox.find('th', class_='summary').get_text().encode('ascii', 'ignore')
        
            release_date = infobox.find('span', class_='bday dtstart published updated').get_text().encode('ascii', 'ignore')
            
            release_year = int(release_date.split('-')[0])
            release_month = int(release_date.split('-')[1])
            release_day = int(release_date.split('-')[2])
            
            grossing = infobox.find('th', text='Box office').next_sibling.next_sibling.get_text().encode('ascii', 'ignore')
            grossing = re.sub('\[1]$', '', grossing)
            grossing = re.sub('\[2]$', '', grossing)
            grossing = re.sub('\[3]$', '', grossing)
            grossing = re.sub('\[4]$', '', grossing)
            grossing = re.sub('\[5]$', '', grossing)
            grossing = re.sub('\[6]$', '', grossing)
            grossing = re.sub('\[7]$', '', grossing)
            grossing = re.sub('\[8]$', '', grossing)
            grossing = re.sub('\[9]$', '', grossing)
            grossing = re.sub('[$]', '', grossing)
            grossing = re.sub('[,]', '', grossing)
            grossing = re.sub('[US]', '', grossing)
            grossing = re.sub('[4]', '', grossing)
        
            if len(grossing) > 16:
                logging.warning(movie_url + ' page is malformed [dropping it ...]')
                return -1 #malformed movie
            
            grossing = grossing.split()
            if len(grossing) == 2:
                number = float(grossing[0]) * self.convert_unit[grossing[1]]
                if number == 0.0:
                    logging.warning(movie_url + ' page is malformed [dropping it ...]')
                    return -1 #malformed movie
                grossing = str(number)

            if not(isinstance(grossing, str)):
                logging.warning(movie_url + ' page is malformed [dropping it ...]')
                return -1 #malformed movie
            
            starring = infobox.find('th', text='Starring')
            starring = starring.next_sibling.next_sibling

            actors = []

            for actor in starring.find_all('a'):
                next_actor_url = urlparse.urljoin(movie_url, actor.get('href'))
                result = self.parse_actor(next_actor_url)
                if(result != -1):
                    actors.append(result)

            return {'movie_name': str.lower(movie_name), 'release_date': release_date, 'grossing': grossing, 'actors': actors}
        except:
            logging.warning(movie_url + ' page is malformed [dropping it ...]')
            return -1 #malformed movie

    """This function parses a actor page, given a url to it.
    We are parsing the side table on the Wikipedia page.
    If the actor page is malformed then we do not include the actor in the actor list of the movie.
    This function returns -1 when the page is malformed.
    """
    def parse_actor(self, actor_url):
        logging.info('Visited: ' + actor_url)

        soup = BeautifulSoup(urlopen(actor_url), 'lxml')
        
        try:
            infobox = soup.find('table', class_='infobox')

            actor_name = infobox.find('span', class_='fn').get_text().encode('ascii', 'ignore')
        
            actor_age = infobox.find('span', class_='noprint ForceAgeToShow').get_text().encode('ascii', 'ignore')
            actor_age = re.sub('[()age]', '', actor_age)

            return (str.lower(actor_name), actor_age)
        except:
            logging.warning(actor_url + ' page is malformed [not including it...]')
            return -1 #malformed actor