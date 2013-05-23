# -*- coding: utf-8 -*-
import urllib
import re

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request


# from tdk_crawler.items import EntryItem
from entry.models import Entry, Meaning
from utils.encoding import normalize


class MeaningSpider(BaseSpider):
    name = "meaning"
    allowed_domains = ["m.tdk.org.tr"]
    domain = "http://m.tdk.org.tr"
    search_url = "http://m.tdk.org.tr/index.php?option=com_gts&arama=gts&%s"
    meaning_start_re = re.compile("^\s*(\d*\.)?\s*")
    meaning_end_re = re.compile(r"[-\"'\s]*$")

    def __init__(self, keyword=None):
        if keyword:
            self.start_urls = [self.__create_url__(keyword)]

    def __create_url__(self, keyword):
        params = {"kelime": keyword.encode("utf8")}
        params_encoded = urllib.urlencode(params)
        return self.search_url % params_encoded

    def start_requests(self):
        for entry in Entry.objects.all().order_by("id"):
            yield Request(self.__create_url__(entry.keyword), self.parse)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        tr_list = hxs.select("/html/body/div/div/div/table/tr")[3].select(
            "td/table[@id='hor-minimalist-a']")
        entry = None
        for meaning_tr in tr_list:
            # Keyword is not needed here because we already have correct
            # keywords crawled from official website.
            keyword = "".join(meaning_tr.select(
                "thead/tr/th/b//text()").extract()).split("(")[0].strip()

            if not entry:
                entry = Entry.objects.get(keyword=keyword)

            tags = "".join(meaning_tr.select(
                "thead/tr/th/i/b//text()").extract()).strip()
            if tags:
                tags = [tag.strip() for tag in tags.split(",")]

            extra_info = "".join(meaning_tr.select(
                "thead/tr/th/i/text()").extract()).strip()
            if extra_info:
                extra_info = [extra.strip() for extra in extra_info.split(",")]

            if tags:
                if not entry.tags:
                    entry.tags = tags
                else:
                    entry.tags.extend(tags)
                    entry.tags = list(set(entry.tags))

            if extra_info:
                if not entry.extra_info:
                    entry.extra_info = extra_info
                else:
                    entry.extra_info.extend(extra_info)
                    entry.extra_info = list(set(entry.extra_info))
            if not entry.normalized:
                entry.normalized = normalize(keyword.lower())
            entry.save()
            for meaning in meaning_tr.select("tr"):
                tags = "".join(meaning.select("td")[0].select("i")[0].select(
                        "text()").extract()).strip()
                if tags:
                    tags = [tag.strip() for tag in tags.split(",")]
                else:
                    tags = None
                meaning_text = "".join(meaning.select("td")[0].select(
                    "text()").extract())
                meaning_text = self.meaning_start_re.sub("", meaning_text)
                meaning_text = self.meaning_end_re.sub("", meaning_text)
                try:
                    example = "".join(meaning.select("td")[0].select(
                        "i")[1].select("text()").extract())
                except IndexError:
                    example = None
                if example:
                    source = "".join(meaning.select("td")[0].select(
                        "b/text()").extract()).strip()
                    if source:
                        example = example + " - " + source
                Meaning.objects.create(entry=entry, tags=tags,
                                      content=meaning_text, example=example)
