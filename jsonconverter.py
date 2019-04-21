from datetime import datetime

class jsonconverter:

    def serialise(self, obj):
        if isinstance(obj, list):
            return [self.serialise(o) for o in obj]
        else:
            return {self.snake_to_camel(k): v for k, v in obj.__dict__.items()}

    def myconverter(self, o):
        if isinstance(o, datetime):
            return o.__str__()


    def snake_to_camel(self, s):
        a = s.split('_')
        a[0] = a[0].lower()
        if len(a) > 1:
            a[1:] = [u.title() for u in a[1:]]
        return ''.join(a)
