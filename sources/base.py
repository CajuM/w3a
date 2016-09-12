import traceback

from sources.wikipedia import Wikipedia
from sources.dmoz import DMOZ

class DomSource():
    def __init__(self, source, cache, *args, **kwargs):
        self.build = (source, args, kwargs)
        self.failedCount = 0

        if type(source) == str:
            if source == 'Wikipedia':
               source = Wikipedia

            elif source == 'DMOZ':
               source = DMOZ

            else:
               raise Exception('Invalid source type')

        else:
            raise Exception('Source must be str')

        self.source = source(cache, *args, *kwargs)

    def getDoms(self):
        print('Starting: ' + str(self.build))
        try:
            ret =  self.source.getDoms()
            print('Finished with {} results: {}'.format(len(ret), self.build))
            return ret

        except Exception as e:
            print('Failed: ' + str(self.build))
            traceback.print_exc()
