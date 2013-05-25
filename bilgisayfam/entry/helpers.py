def get_json_cache_key(keyword):
    """
    Returns a cache key for the given word and dictionary.
    """
    version = "1.0"
    return ":".join(["entry:utils", version, "meaning", keyword])
