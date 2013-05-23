# Scrapy settings for tdk_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'tdk_crawler'

SPIDER_MODULES = ['tdk_crawler.spiders']
NEWSPIDER_MODULE = 'tdk_crawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the
# user-agent USER_AGENT = 'tdk_crawler (+http://www.yourdomain.com)'

# NOTE:
# Note that we need to set PYTHONPATH so that the settings file can be found.
# For example:
# export PYTHONPATH=$PYTHONPATH:/home/tayfun/projects/bilgisayfam/bilgisayfam
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bilgisayfam.settings.scrapy")
