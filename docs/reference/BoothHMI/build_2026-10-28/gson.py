import json
def dumps(obj):
    s = json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True)   # Ignition writes keys sorted
    for a, b in (("'", "\\u0027"), ("<", "\\u003c"), (">", "\\u003e"), ("&", "\\u0026"), ("=", "\\u003d")):
        s = s.replace(a, b)
    return s
