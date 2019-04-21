class organizations(object):
    def __init__(self, name, alias):
        self.key = name
        self.values = alias

class feedSource(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url