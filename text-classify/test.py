#coding:utf-8
import re
import math

from docclass import Classifier


def test_infc_func():
    c = Classifier(getfeatures=None)
    c.infc("python", "good")
    c.infc("python", "good")
    c.infc("the", "bad")
    c.infc("the", "good")

    print c.fc


if __name__ == "__main__":
    test_infc_func()
