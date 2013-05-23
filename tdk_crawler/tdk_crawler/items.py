# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

# from scrapy.item import Item, Field
from scrapy.contrib.djangoitem import DjangoItem

from bilgisayfam.entry.models import Entry


class EntryItem(DjangoItem):
    # keyword = Field()
    django_model = Entry
