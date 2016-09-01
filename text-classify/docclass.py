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

    # 三篇good归类的文档中，有两篇出现了单词quick
    # 即一篇“good”分类的文档中包含该单词的概率为 
    # P(quick | good) = 0.666
    # fprob函数有些偏激 不够合理
    def fprob(self, f, cat):
        if self.catcount(cat) == 0:
            return 0
        return self.fcount(f, cat) / self.catcount(cat)

    def weightedprob(self, cat, prf, weight=1.0, ap=0.5):
        # 计算当前概率值
        basicprob = prf(f, cat) # prf 就是 fprob 函数
        # 统计特征在所有分类中出现的次数
        totals = sum([self.fcount(f, c) for c in self.categories()])
        # 计算加权平均
        bp = ((weight * ap) + (totals * basicprob)) / (weight + totals)
        return bp


class NaiveBayes(Classifier):

    def __init__(self, getfeature):
        Classifier.__init__(self, getfeature)
        self.thresholds = {}

    def setthresholds(self, cat, t):
        self.thresholds[cat] = t
    
    def getthresholds(self, cat):
        if cat not in self.thresholds:
            return 1.0
        return self.thresholds[cat]

    # 计算整篇文档中的单词属于某个分类的概率
    def docprob(self, item, cat):
        features = self.getfeatures(item)
        # 将所有概率相乘
        p = 1
        for f in features:
            p *= self.weightedprob(f, cat, self.fprob)
        return p
    
    # 朴素贝叶斯方法 求得P(Category|Document)
    # 这里面没有求P(Document)
    # 因为对每个分类都是一样的
    def prob(self, item, cat):
        catprob = self.catcount(cat) / self.totalcount()
        docprob = self.docprob(item, cat)
        return docprob * catprob
    
    # 构建正式的分类器
    def classify(self, item, default=None):
        probs = {}
        # 寻找概率最大的分类
        max = 0.0
        for cat in self.categories():
            probs[cat] = self.prob(item, cat)
            if probs[cat] > max:
                max = probs[cat]
                best = cat
        
        # 确保概率值超出域值*次大概率值
        for cat in probs:
            if cat == best:
                continue
            if probs[cat] * self.getthresholds(best) > probs[best]:
                return default
        return best


class Fisherclassifier(Classifier):

    def cprob(self, f, cat):
        # 特征在该分类中出现的频率
        clf = self.fprob(f, cat)
        if clf == 0:
            return 0
        
        # 特征在所有分类中出现的频率
        freqsum = sum([self.fprob(f, c) for c in self.categories()])

        # 概率等于特征在该分类中出现的频率除以总体频率
        p = clf / freqsum
        return p
    
    def fisherprob(self, item, cat):
        # 将所有概率值相乘
        p = 1
        features = self.getfeatures(item)
        for f in features:
            p *= self.weightedprob(f, cat, self.cprob)

        fscore = -2 * math.log(p)

        # 利用倒置对数卡方函数求得概率
        return self.invchi2(fscore, len(features) * 2)

        def invchi2(self, chi, df):
            m = chi / 2.0
            sum = term = math.exp(-m)
            for i in range(1, df//2):
                term *= m / i
                sum += term
            return min(sum, 1.0)




def sampletrain(cl):
    cl.train("Nobody owns the water.", "good")
    cl.train("the quick rabbit jumps fences", "good")
    cl.train("buy pharmaceuticals now", 'bad')
    cl.train("make quick money at the online casino", "bad")
    cl.train("the quick brown fox jumps", "good")