from extensions import register


# Register plugins here.
register("entry.backends", "tdk", "entry.backends.tdk:get_meaning")
