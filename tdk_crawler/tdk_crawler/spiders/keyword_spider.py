# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

from django.db import IntegrityError

# from tdk_crawler.items import EntryItem
from entry.models import Entry
from utils.encoding import normalize


turkish_alphabet = list(u"abcçdefgğhıijklmnoöprsştuüvyz")
start_urls = []
for letter in turkish_alphabet:
    start_urls.append("http://m.tdk.org.tr/index.php?option=com_seslissozluk"
                      "&view=seslissozluk&kategori1=yazim_listeli"
                      "&ayn1=bas&kelime1=%s" % letter)


class KeywordSpider(BaseSpider):
    name = "keyword"
    allowed_domains = ["m.tdk.org.tr"]
    start_urls = start_urls
    domain = "http://m.tdk.org.tr"

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        rows = hxs.select("/html/body/div/div/div/table/table/tr")
        # First add all the keywords on this page.
        for tr in rows:
            for td in tr.select("td"):
                keyword = "".join(td.select("p//text()").extract())
                keyword = keyword.split(",")[0].split("/")[0].split("(")[0]
                keyword = keyword.strip()
                """
                Note that for the word "f", TDK dictionary web page
                has a problem and it adds FF0000> to the keyword. So
                "fabrikacilik" becomes u'FF0000">fabrikac\u0131l\u0131k'
                so you might want to use:
                    keyword = keyword.replace('FF0000">', "")
                OR do this on SQL:
                    UPDATE entry_entry SET
                    keyword=replace(keyword, 'FF0000">', ''),
                    normalized=replace(normalized, 'FF0000">', '')
                    WHERE keyword LIKE 'FF%';
                """
                try:
                    Entry.objects.create(keyword=keyword,
                                         normalized=normalize(keyword))
                except IntegrityError:
                    # Pass on when we get an IntegrityError.
                    print "Got IntegrityError on: %s" % keyword
                # entry_item = EntryItem(keyword=keyword)
                # entry_item.save()
        # Next, add the next page to URLs to crawl.
        if len(rows) != 0:
            # add next page link to pages to crawl as well.
            next_page_xpath = \
                "/html/body/div/div/div/table/tr/td/form/p/span[2]/a/@href"
            path = hxs.select(next_page_xpath).extract()[0]
            yield Request(self.domain + path, callback=self.parse)
