import urllib.request
import gzip
import re
from sources.cache import Cache

from sources.serialize import DomSet

class DMOZ():
    domre = re.compile(r'(?:http|https)://([\w\-\.]+)')
    source = 'http://rdf.dmoz.org/rdf/content.rdf.u8.gz'

    def __init__(self, cache):
        self.cache = cache

    def getDoms(self):
        resp = urllib.request.urlopen(self.source)

        instkey = Cache.getHttpRespInstkey(self.source, resp)

        if instkey in self.cache:
            return self.cache[instkey]


        with resp as f:
            rdf = ''
            gzf = gzip.open(f, 'rt', encoding='utf-8')
            doms = set()

            while True:
                rdfp = gzf.readline()

                if len(rdfp) == 0:
                    ret = DomSet(doms)
                    self.cache[instkey] = ret
                    return ret

                rdf += rdfp
                end = 0

                for match in self.domre.finditer(rdf):
                    end = match.end()
                    dom = match.groups()[0]
                    doms.update([dom])

                rdf = rdf[end:]


    @staticmethod
    def getAllWikis():
        with urllib.request.urlopen(Wikipedia.allsource) as f:
            windex = f.read().decode('utf-8')
            return  Wikipedia.allwikire.findall(windex)
