import json

from django.core.cache import cache
from django.db import connection
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render

from entry.utils import get_json_cache_key
from entry.models import Entry


def find_meaning(keyword):
    """
    Returns a JSON string representing keyword and its meanings according to
    the dictionary specified.
    """
    try:
        # Check if related entry is in DB.
        entry = Entry.objects.get(keyword=keyword)
    except Entry.DoesNotExist:
        from entry.tdk import get_meaning
        # This should add an Entry (it will also add meaning if it exists).
        try:
            tdk_meaning = get_meaning(keyword)
            return tdk_meaning
        except IndexError:
            # There was an error in parsing TDK. DB error on their side.
            return None

    # Entry exists, so presumably we have made a round trip to TDK to get
    # meaning. We'll see if meaning exists in the DB.
    cursor = connection.cursor()

    """
    Custom SQL using some advanced functions such as array_agg and
    row_to_json which returns JSON data.
    """
    cursor.execute("SELECT array_to_json(array_agg(row_to_json(t1))) "
        "FROM ("
            "SELECT m.id, m.tags, content FROM entry_meaning as m "
            "WHERE m.entry_id=%s) t1", [entry.id])
    """
    Meaning is a dict like:

{u'meaning': [{u'content': u'aslen cinceden gecmis tum dunya dillerine',
   u'id': 1,
   u'tags': [u'isim', u'cince']},
  {u'content': u'tropik firtina', u'id': 2, u'tags': [u'isim', u'ingilizce']}],
 u'keyword': u'tayfun'}
        """
    result = cursor.fetchone()[0]
    if result:
        entry_dict = model_to_dict(entry, ["keyword", "extra_info", "tags"])
        entry_dict['meaning'] = result
        return entry_dict
    else:
        return None


def index_view(request):
    """
    Main page view. If there are no GET parameters, return main page, else
    return JSON data.
    """
    try:
        # REQUEST has GET and POST parameters.
        keyword = request.REQUEST["search"]
    except KeyError:
        # if there's no search keyword, show base page.
        return render(request, "base.html")

    cache_key = get_json_cache_key(keyword)
    entry_dict = cache.get(cache_key)
    if not entry_dict:
        entry_dict = find_meaning(keyword)
        if not entry_dict:
            # can't get it from TDK as well. Return 404.
            # TODO: Create a generic 404 page including search keywords.
            raise Http404
        cache.set(cache_key, entry_dict)

    if request.is_ajax():
        return HttpResponse(json.dumps(entry_dict),
                            content_type='application/json')
    return render(request, "base.html", {"entry_dict": entry_dict})
