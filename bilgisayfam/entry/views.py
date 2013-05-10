import json

from django.core.cache import cache
from django.db import connection
from django.shortcuts import render

from entry.utils import get_json_cache_key
from entry.models import Entry, Dictionary


def find_meaning(keyword, dict_name):
    """
    Returns a JSON string representing keyword and its meanings according to
    the dictionary specified.
    """
    json_meaning = cache.get(get_json_cache_key(keyword, dict_name))
    if json_meaning:
        return json_meaning
    # Meaning is not in cache, check DB.

    if not Entry.objects.filter(keyword=keyword).exists():
        from entry.backends.tdk import get_meaning
        # This should add an Entry (it will also add meaning if it exists).
        get_meaning(keyword)

    dictionary = Dictionary.objects.get(name=dict_name)
    cursor = connection.cursor()
    """
    Custom SQL using some advanced functions such as array_agg and
    row_to_json which returns JSON data.
    """
    cursor.execute(
        "SELECT row_to_json(t2) FROM ("
            "SELECT %s as keyword, "
            "(SELECT array_to_json(array_agg(row_to_json(t1)))"
                "FROM ("
                    "SELECT m.id, m.tags, content FROM entry_meaning "
                    "as m, entry_entry as e "
                    "WHERE m.entry_id=e.id and m.dictionary_id=%s and "
                    "e.keyword=%s) t1) "
            "AS meaning) t2;", [keyword, dictionary.id, keyword])
    """
    Meaning is a dict like:

{u'meaning': [{u'content': u'aslen cinceden gecmis tum dunya dillerine',
   u'id': 1,
   u'tags': [u'isim', u'cince']},
  {u'content': u'tropik firtina', u'id': 2, u'tags': [u'isim', u'ingilizce']}],
 u'keyword': u'tayfun'}
        """
    result = cursor.fetchone()[0]
    if result["meaning"]:
        return json.dumps(result)
    else:
        return None


def index_view(request):
    """
    Main page view. If there's no GET parameters, return main page, else
    return JSON data.
    """
    try:
        keyword = request.REQUEST["search"]
    except KeyError:
        # if there's no search keyword, show base page.
        return render(request, "base.html")

    # if no sozluk argument is given, it defaults to TDK.
    dictionary = request.REQUEST.get("dictionary", "tdk")
    # There's a search keyword given. Find the meaning.
    json_meaning = find_meaning(keyword, dictionary)
    import ipdb; ipdb.set_trace()

    # If request is a POST, return JSON, else return html with data filled in.
    if request.method == "GET":
        # return HTML
        return render(request, "base.html", {"search_result": json_meaning})
    # return JSON.
    return json_meaning
