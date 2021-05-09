import re


class ConstantVariables(object):
    URL = r"https://news.ycombinator.com/news?p={page}"
    SUBTEXT_CLASS = ".subtext"
    SCORE_CLASS = ".score"
    LINKS_CLASS = ".storylink"
    SCORE_TEXT_PATTERN = r"^(\d{0,})[^.*\s]"
    SCORE_TEXT_PATTERN = re.compile(SCORE_TEXT_PATTERN)
