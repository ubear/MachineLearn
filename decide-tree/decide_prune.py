#coding:utf-8
from decision_tree import *


def prune(tree, mingain):
    if tree.tb.results == None:
        prune(tree.tb, mingain)
    if tree.fb.results == None:
        prune(tree.fb, mingain)


    if tree.tb.results != None and tree.fb.results != None:
        tb, fb = [], []
        for v, c in tree.tb.results.items():
            tb += [[v]] * c

        for v, c in tree.fb.results.items():
            fb += [[v]] * c

        delta = entropy(tb + fb) - (entropy(tb) + entropy(fb)) / 2
        if delta < mingain:
            tree.tb, tree.fb = None, None
            tree.results = unique_counts(tb + fb)


if __name__ == '__main__':
    from data import my_data
    from build_dt_img import draw_tree

    tree = build_tree(my_data)
    draw_tree(tree, 'previous.jpg')
    prune(tree, 1.0)
    draw_tree(tree, 'next.jpg')
