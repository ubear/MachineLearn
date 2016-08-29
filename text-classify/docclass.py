#coding:utf-8
import re
import math


def getwords(doc):
    # 按非字母字符拆分
    splitter=re.compile('\\W*')# regular pattern
    words = [s.lower() for s in splitter.split(doc)
            if len(s) > 2 and len(s) < 20]
    # 返回一组不重复的单词
    # 注意dict函数的参数是List
    return dict([(w, 1) for w in words])


#  分类器
class Classifier(object):
    def __init__(self, getfeatures, filename=None):
        # 统计 特征/分类 组合的数量
        # {"python": {"bad": 0, "good": 6}}
        # python 是特征 对应的字典是分类情况
        # 特征python在bad的分类里出现了0次
        # 在good的分类里出现了6次
        self.fc = {}
        # 统计 每个分类中文档数量
        self.cc = {}
        # 对应一个函数 用于提取特征
        # 即getwords函数：单词出现在文档无论多少次
        # 只计为1次
        self.getfeatures = getfeatures

    def infc(self, f, cat):
        # f 是一个特征（单词）
        # cat 是一个分类

        # setdefault:
        # If key is in the dictionary,
        # return its value. If not, insert key
        # with a value of default and return default.
        # default defaults to None.
        self.fc.setdefault(f, {})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat] += 1

        # 增加某一分类的计数
    def incc(self, cat):
        self.cc.setdefault(cat, 0)
        self.cc[cat] += 1

        # 某一特征出现于某一分类中的次数
    def fcount(self, f, cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0

        # 属于某一分类的内容项数量
    def catcount(self, cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0

        # 所有内容项的数量
    def totalcount(self):
        return sum(self.cc.values())

        # 所有分类的列表
    def categories(self):
        return self.cc.keys()

        # item 为文档
        # cat 为分类
    def train(self, item, cat):
        # 得到文档中的所有特征单词
        features = self.getfeatures(item)
        for f in features:
            # 增加特征单词及所在分类
            self.infc(f, cat)
        # 增加分类项
        self.incc(cat)

    def fprob(self, f, cat):
        if self.catcount(cat) == 0:
            return 0
        return self.fcount(f, cat) / self.catcount(cat)


def sampletrain(cl):
    cl.train("Nobody owns the water.", "good")
    cl.train("the quick rabbit jumps fences", "good")
    cl.train("buy pharmaceuticals now", 'bad')
    cl.train("make quick money at the online casino", "bad")
    cl.train("the quick brown fox jumps", "good")

