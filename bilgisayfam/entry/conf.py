import datetime

from extensions import register


# Register plugins here.
register("entry.backends", "tdk", "entry.backends.tdk:get_meaning")

# Fresh data should be at most 1 day old.
MAX_FRESH_DELTA = datetime.timedelta(1)
