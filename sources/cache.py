import arrow
import dbm.gnu as gdbm
import hashlib
import pickle

class Cache:

    def __init__(self, path):
        self.path = path

        if self.path.exists() and not self.path.is_dir():
            raise Exception('{} exists and is not a directory'.format(self.path))
           
        if not self.path.exists():
            self.path.mkdir()

        self.db = gdbm.open(str(self.path / 'cache.db'), 'cs')
        self.db.reorganize()

    @staticmethod
    def getHttpTime(htstr):
        for fstr in ['EEE, dd MMM yyyy HH:mm:ss zzz', 'EEE, dd-MMM-yy HH:mm:ss zzz', 'EEE MMM d HH:mm:ss yyyy']:
            try:
                return arrow.get(htstr, fstr).timestamp
            except:
                pass

    @staticmethod
    def getHttpRespInstkey(url, resp):
        reskey = Cache.hash(url)

        return {
            'reskey': reskey,
            'ETag': resp.getheader('ETag'),
            'Last-Modified': resp.getheader('Last-Modified')
        }

    @staticmethod
    def hash(obj):
        m = hashlib.sha256()
        m.update(pickle.dumps(obj))
        return m.digest()

    def __getitem__(self, instkey):
        instkey = Cache.hash(instkey)

        if instkey in self.db:
            return pickle.loads(self.db[instkey])

        else:
            return None

    def __setitem__(self, instkey, obj):
        reskey = Cache.hash(instkey['reskey'])
        instkey = Cache.hash(instkey)

        if instkey in self.db:
            return

        self.db[instkey] = pickle.dumps(obj)

        if reskey in self.db:
            oldinstkey = self.db[reskey]

            del self.db[oldreskey]

        self.db[reskey] = instkey

    def __contains__(self, instkey):
        instkey = Cache.hash(instkey)

        return instkey in self.db

