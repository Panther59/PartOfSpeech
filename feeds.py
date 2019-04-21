import feedparser
import html2text
from dateutil import parser


class News:
    def __init__(self, key, title, post, date, orgs=None):
        self.key = key
        self.title = title
        self.post = post
        self.date = date
        if(orgs != None):
            self.organizations = orgs


class FeedHelper:

    def get_news(self, feedurl):

        NewsFeed = feedparser.parse(feedurl)

        return [self.map_news(e) for e in NewsFeed.entries]

    def map_news(self, e):
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_maker.ignore_images = True

        text_maker.bypass_tables = False
        news = News(e.id, e.title, text_maker.handle(
            e.summary).strip(), parser.parse(e.published))
        return news


# feedhelper = FeedHelper()
# feedhelper.get_news("http://feeds.reuters.com/reuters/companyNews")
