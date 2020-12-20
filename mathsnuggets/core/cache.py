import flask_caching

cache = flask_caching.Cache(config={"CACHE_TYPE": "simple", "CACHE_DEFAULT_TIMEOUT": 300})
cached = cache.cached
delete = cache.delete
delete_memoized = cache.delete_memoized
memoize = cache.memoize
