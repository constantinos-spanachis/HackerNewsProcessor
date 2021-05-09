import requests
import re

from pathlib import Path
from bs4 import BeautifulSoup
from utils.constants import ConstantVariables
from utils.logger import Logger
from typing import List, Any, Dict, Union


class HackerNewsProcessor(ConstantVariables):
    logger = Logger("Hacker News Processor").logger

    def __init__(self, score_limit: int = 100, pages_limit: int = 2):
        """
        Initializes the class with a preferred score limit
        Args:
            score_limit: The score that a story needs to have in order to be selected
            pages_limit: How many pages you want to include.
        """
        super().__init__()
        self._score_limit = score_limit
        self.pages_limit = pages_limit

    @property
    def _construct_pages(self) -> List[str]:
        return [self.URL.format(page=str(page)) for page in range(1, self.pages_limit + 1)]

    @staticmethod
    def _sort_news(news_list: List[Dict[str, Union[bool, Any]]]) -> List[Dict[str, Union[bool, Any]]]:
        """

        Returns:
            object:
        """
        return sorted(news_list, key=lambda key: key['votes'], reverse=True)

    def extract(self, page_url: str) -> BeautifulSoup:
        """
        Extracts the content of the URL.
        Returns:
            The url content as a beautiful soup object
        """
        self.logger.info("Extracting the data")
        try:
            req = requests.get(page_url)
            assert req.status_code == 200
        except AssertionError:
            self.logger.error(f"The request was unsuccessful. The status code was {req.status_code}")
        except Exception as e:
            self.logger.error(f"There was an error during the request. The error was {e}")
        else:
            soup = BeautifulSoup(req.text, parser="html.parser", features="lxml")
            return soup

    def transform(self, soup: BeautifulSoup):
        self.logger.info("Transforming the extracted content")
        zipped_ = zip(soup.select(self.LINKS_CLASS), soup.select(self.SUBTEXT_CLASS))
        custom_news = []
        for link, subtext in zipped_:
            score = subtext.select(self.SCORE_CLASS)
            if len(score):
                if points := int(re.match(self.SCORE_TEXT_PATTERN, score[0].getText()).group()) >= self._score_limit:
                    title = link.getText()
                    href = link.get('href', None)
                    custom_news.append({"title": title, 'link': href, 'votes': points})
            else:
                self.logger.warning(f"{link.getText} had no score.")
        return custom_news

    def main(self):
        selected_news = []
        for link in self._construct_pages:
            soup = self.extract(page_url=link)
            selected_news.extend(self.transform(soup=soup))
        selected_news = self._sort_news(selected_news)
        self.logger.info(selected_news)
        return selected_news



if __name__ == '__main__':
    HackerNewsProcessor().main()
