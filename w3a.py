#!/usr/bin/env python3

from sources.serialize import DomSet
from sources.base import DomSource
from sources.cache import Cache

from sources.wikipedia import Wikipedia

import pathlib

if __name__ == '__main__':
    cache = Cache(pathlib.Path('.') / 'cache')

    domss = []

    for wiki in Wikipedia.getAllWikis():
        domss.append(DomSource('Wikipedia', cache, wiki))

    domss.append(DomSource('DMOZ', cache))

    domset = DomSet([])
    for doms in domss:
        doml = doms.getDoms()
        if doml is not None:
            domset = DomSet([domset, doml])
            print('Total: {}'.format(len(domset)))

        elif doms.failedCount < 3:
            doms.failedCount += 1
            domss.append(doms)


    domset.toTxt('dom.txt')
