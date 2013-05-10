def get_json_cache_key(keyword, dictionary):
    """
    Returns a cache key for the given word and dictionary.
    """
    version = "1.0"
    return ":".join(["entry:utils", version, "dictionary", dictionary,
                     "meaning", keyword])
