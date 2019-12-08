from flask.json import JSONEncoder as _JSONEncoder
from datetime import datetime,date
class JSONEncoder(_JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return _JSONEncoder.default(self, obj)