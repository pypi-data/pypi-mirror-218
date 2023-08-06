import feedparser
from bs4 import BeautifulSoup
from functools import cache

class BaseFeedScraper:
    def __init__(self):
        self.link = self.get_link()

    def get_link(self):
        return None 
    
    def scrape_news(self)-> dict:
        """ Scrape the news feed, and return a list of news articles and source details."""
        parsed_xml_news = self._get_xml_news()
        return self._sanitize_news(parsed_xml_news)
    
    @cache
    def _get_xml_news(self)-> dict:
        """ Return an object of parsed xml news feed"""
        return feedparser.parse(self.link)

    def _sanitize_news(self, parsed_xml_news: dict) -> dict:
        """ Satinize news parsed from xml"""
        sanitized_news = []
        news_list = parsed_xml_news.entries
        for news in news_list:
            title = news['title']
            link = news['link']
            author = news['author']
            published_date = news['published']
            content = news['content'][0]['value'] if len(news.get('content', [])) > 0 else ''
            cover_image = self._get_image_url(content)
            sanitized_news.append({
                'title': title,
                'link': link,
                'author': author,
                'published_date': published_date,
                'cover_image': cover_image,
            })
        return {
            'data': sanitized_news,
            'source': self._get_source_details(parsed_xml_news.feed)
        }
            
    def _get_image_url(self, content: str)->str:
        """Returns the image url for the given content news feed"""
        soup = BeautifulSoup(content, 'html.parser')
        img_tag = soup.find_all('img')
        img = img_tag[0]['src'] if len(img_tag) > 0 else ''
        return img
    
    def _get_source_details(self, feed: dict) -> dict:
        """Returns the source details for the news, that is, the site the feed is being scraped from"""
        name = feed['title']
        link = feed['link']
        if len(name) == 0:
            name = self._get_source_name(link)
        source_details = {
            'name': name,
            'url': link,
            'mission_statement': feed['subtitle'] if len(feed['subtitle']) > 0 else self._get_mission_statement(name),
        }
        return source_details

    def _get_source_name(self, link):
        """Returns source name of the news based on link provided should the feed have no defined source name"""
        name = ''
        if 'investigativeplatform-mw' in link:
            name = 'Platform For Investigative Journalism'
        return name
    
    def _get_mission_statement(self, source_name):
        """Returns source mission statement of the news based on source name provided should the feed have no defined source statement"""
        statement = ''
        if source_name == 'Platform For Investigative Journalism':
            statement = 'Digging Truth. Lighting Democracy'
        return statement