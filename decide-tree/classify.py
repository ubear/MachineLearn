#coding:utf-8


def classify(observation, tree):
    if tree.results != None:
        return tree.results
    else:
        v = observation[tree.col]
        branch = None
        if isinstance(v, int) or isinstance(v, float):
            if v >= tree.value:
                branch = tree.tb
            else:
                branch = tree.fb
        else:
            if v == tree.value:
                branch = tree.tb
            else:
                branch = tree.fb
        return classify(observation, branch)


if __name__ == '__main__':
    from decision_tree import *
    from data import my_data
    tree = build_tree(my_data)
    test = ['(direct)', 'USA', 'yes', 5]
    print classify(test, tree)
