import urllib.request
import gzip
import re

from sources.cache import Cache
from sources.serialize import DomSet

class Wikipedia():
    allwikire = re.compile(r'\<a href\="([^/]+)/.*?"\>\1\</a\>')
    allsource = 'https://dumps.wikimedia.org/backup-index-bydb.html'

    domre = re.compile(r'[0-9],\'(?:[a-z]*?://|//|)([\w\-\.]+)')

    def __init__(self, cache, wiki):
        self.wiki = wiki
        self.cache = cache
        self.source = 'https://dumps.wikimedia.org/{0}/latest/{0}-latest-externallinks.sql.gz'.format(self.wiki)

    def getDoms(self):
        resp = urllib.request.urlopen(self.source)

        instkey = Cache.getHttpRespInstkey(self.source, resp)

        if instkey in self.cache:
            return self.cache[instkey]

        with resp as f:
            sql = ''
            gzf = gzip.open(f, 'rt', encoding='utf-8')
            doms = set()

            while True:
                sqlp = gzf.readline()

                if len(sqlp) == 0:
                    ret = DomSet(doms)
                    self.cache[instkey] =  ret

                    return ret

                sql += sqlp
                end = 0

                for match in self.domre.finditer(sql):
                    end = match.end()
                    dom = match.groups()
                    dom = dom[0]
                    doms.update([dom])

                sql = sql[end:]


    @staticmethod
    def getAllWikis():
        with urllib.request.urlopen(Wikipedia.allsource) as f:
            windex = f.read().decode('utf-8')
            return  Wikipedia.allwikire.findall(windex)
