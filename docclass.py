#coding:utf-8
import re
import math


def getwords(doc):
    splitter=re.compile('\\W*')# regular pattern
    words = [s.lower() for s in splitter.split(doc)
            if len(s) > 2 and len(s) < 20]
    return dict([(w, 1) for w in words])


class classifier(object):
    def __init__(self, getfeatures, filename=None):
        self.fc = {}
        self.cc = {}
        self.getfeatures = getfeatures

    def infc(self, f, cat):
        # f is feature and cat is class
        self.fc.setdefault(f, {})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat] += 1

    def incc(self, f, cat):
        self.cc.setdefault(cat, 0)
        self.cc[cat] += 1

    def fcount(self, f, cat):
        if f in self.cc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0

    def catcount(self, cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0

    def totalcount(self):
        return sum(self.cc.values())

    def categories(self):
        return self.cc.keys()

    def train(self, item, cat):
        features = self.getfeatures(item)
        for f in features:
            self.incf(f, cat)
        self.incc(cat)



    




