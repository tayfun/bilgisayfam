import json

from django.core.cache import cache
from django.db import connection
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render

from entry.helpers import get_json_cache_key
from entry.models import Entry
from utils.encoding import normalize


def find_meaning(keyword):
    """
    Returns a JSON string representing keyword and its meanings according to
    the dictionary specified.
    """
    try:
        entry = Entry.objects.get(keyword=keyword)
    except Entry.DoesNotExist:
        try:
            entry = Entry.objects.filter(normalized=normalize(keyword))[0]
        except IndexError:
            raise Http404

    cursor = connection.cursor()

    """
    Custom SQL using some advanced functions such as array_agg and
    row_to_json which returns JSON data.
    """
    cursor.execute("SELECT array_to_json(array_agg(row_to_json(t1))) "
        "FROM ("
            "SELECT m.id, m.tags, content, example FROM entry_meaning as m "
            "WHERE m.entry_id=%s ORDER BY id ASC) t1", [entry.id])
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
