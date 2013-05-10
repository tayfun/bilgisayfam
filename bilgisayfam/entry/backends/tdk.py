import json

from bs4 import BeautifulSoup
import requests

from django.forms.models import model_to_dict

from entry.models import Entry, Meaning, Dictionary


def get_meaning(keyword):
    """
    Assuming that there are no Entry or Meaning objects in the DB for the
    given /keyword/, it makes a request and extracts data from TDK website
    and adds it to the DB.
    """
    form_fields = {"kelime": keyword}
    response = requests.post(
        "http://www.tdk.gov.tr/index.php?option=com_gts&arama=gts",
        data=form_fields)
    soup = BeautifulSoup(response.text)
    try:
        table_tag = soup.select("#hor-minimalist-a")[0]
        meta_data_list = table_tag.select("thead i")[0].contents
    except TypeError:
        # add a basic row and postpone adding adding data from other
        # web sites.
        Entry.objects.create(keyword=keyword)
        # TODO: Add a simple task for checking other dictionary web sites
        # via a task scheduler like celery or rq.
        return None

    entry_tags = list()
    extra_info = list()
    for meta_data_tag in meta_data_list:
        try:
            if meta_data_tag.name == "b":
                tag_list = unicode(meta_data_tag.string).\
                    split(',')
                entry_tags.extend(
                    map(lambda x: x.strip(), tag_list))
        except AttributeError:
            # Extra info like "ingilizce typhoon".
            tag_list = unicode(meta_data_tag.string).\
                split(',')
            extra_info.extend(
                map(lambda x: x.strip(), tag_list))
    entry = Entry.objects.create(keyword=keyword, tags=entry_tags,
        extra_info=extra_info)
    entry_dict = model_to_dict(entry, fields=["tags", "extra_info",
                                              "keyword"])
    entry_dict["meaning"] = []
    tdk = Dictionary.objects.get(name="tdk")
    for meaning_td in table_tag.select("td"):
        meaning_tags = list()
        content = unicode()
        for td_tag in meaning_td:
            try:
                if td_tag.name == 'i':
                    meaning_tags.extend(
                            unicode(td_tag.string).split(','))
            except AttributeError:
                content += unicode(td_tag.string)
        meaning = Meaning.objects.create(
            dictionary=tdk, entry=entry, tags=meaning_tags,
            content=content.strip())
        meaning_dict = model_to_dict(meaning, fields=["tags", "content", ])
        meaning_dict["dictionary"] = "tdk"
        meaning_dict["votes"] = 0
        entry_dict["meaning"].append(meaning_dict)
    # Return JSON.
    return json.dumps(entry_dict)
