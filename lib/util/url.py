def Formater(uri):
    result = set()
    uri = uri.strip()
    if not uri.endswith("/"):
        uri = "{}/".format(uri)
    if (not uri.startswith("http://")) and (not uri.startswith("https://")):
        result.add("http://{}".format(uri))
        result.add("https://{}".format(uri))
    else:
        result.add(uri)
    return result
