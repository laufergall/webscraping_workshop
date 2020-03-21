"""
Definition of spyder to retrieve Cinema instances
"""

import logging
from datetime import datetime
from typing import List

import scrapy

from .data_structures import Cinema, Address, Contact, Show
from .utils import strip_text, is_positiveinteger


logger = logging.getLogger('KinoSpider')


class KinoSpider(scrapy.Spider):
    
    name = 'kinoprogramm'
    start_urls = ['https://www.berlin.de/kino/_bin/azfilm.php']

    @staticmethod
    def create_shows(titles: List[str], movies_times: List[List[str]]) -> List[Show]:

        shows = list()
        for title, movie_times in zip(titles, movies_times):
            show = Show(title=title)
            for show_day, show_times in zip(*[iter(movie_times)] * 2):
                for show_time in show_times.split(','):
                    # remove weekday
                    show_day_ = show_day.split(', ')[1]
                    show.times.append(datetime.strptime(show_day_ + show_time,
                                                        '%d.%m.%y: %H:%M'))
            shows.append(show)
        return shows

    def parse(self, response: scrapy.http.response.html.HtmlResponse):

        selectors = response.xpath('//div[@class="controls"]/select/option')

        hrefs = ['https://www.berlin.de/kino/_bin/kinodetail.php/' + sel.attrib['value']
                 for sel in selectors if is_positiveinteger(sel.attrib['value'])]

        for href in hrefs:
            self.logger.info(f'Scraping: {href}')
            yield response.follow(href, self.parse_cinema)

    @strip_text
    def get_titles(self, response: scrapy.http.response.html.HtmlResponse) -> List[str]:
        return response.css('button.accordion-trigger::text').getall()

    @strip_text
    def get_name(self, response: scrapy.http.response.html.HtmlResponse) -> str:
        return response.css('h1.top::text').get()

    @strip_text
    def get_description(self, response: scrapy.http.response.html.HtmlResponse) -> str:
        return response.xpath('//div[@class="kinodetail echo"]/p/text()').get()

    @strip_text
    def get_description(self, response: scrapy.http.response.html.HtmlResponse) -> str:
        return response.xpath('//div[@class="kinodetail echo"]/p/text()').get()

    @strip_text
    def get_description(self, response: scrapy.http.response.html.HtmlResponse) -> str:
        return response.xpath('//div[@class="kinodetail echo"]/p/text()').get()

    @strip_text
    def get_street(self, response: scrapy.http.response.html.HtmlResponse) -> str:
        return response.xpath('//span[@class="street-address"]/text()').get()

    @strip_text
    def get_postal_code(self, response: scrapy.http.response.html.HtmlResponse) -> str:
        return response.xpath('//span[@class="postal-code"]/text()').get()

    @strip_text
    def get_district(self, response: scrapy.http.response.html.HtmlResponse) -> str:
        return response.xpath('//span[@class="locality"]/text()').get()

    @strip_text
    def get_telephone(self, response: scrapy.http.response.html.HtmlResponse) -> str:
        return response.xpath(
                '//span[contains(text(), "Telefon")]/following-sibling::span/text()').get()

    @strip_text
    def get_prices(self, response: scrapy.http.response.html.HtmlResponse) -> List[str]:
        return response.xpath('//section[@class="infoblock oeffnungszeiten"]/div/*/text()').getall()

    def parse_cinema(self, response: scrapy.http.response.html.HtmlResponse) -> dict:

        titles = self.get_titles(response)
        movies_times = list()
        for movie in response.xpath('//div[@class="table-responsive-wrapper"]'):
            times = list()
            for showtime in movie.xpath('.//tr'):
                times += showtime.xpath('./td/text()').getall()
            movies_times.append(times)

        cinema = Cinema(
            
            name=self.get_name(response),
            description=self.get_description(response),
            address=Address(street=self.get_street(response),
                            postal_code=self.get_postal_code(response),
                            district=self.get_district(response),
                            city='Berlin',
                            country='Germany'),
            contact=Contact(telephone=self.get_telephone(response)),
            prices=self.get_prices(response),

            shows=self.create_shows(titles, movies_times)
        )

        self.logger.info(f'Scraped cinema: {cinema.name}')

        yield cinema.to_dict()
