#coding:utf-8


def mdclassify(observation, tree):
    if tree.results != None:
        return tree.results

    else:
        v = observation[tree.col]
        if v == None:
            tr, fr = (mdclassify(observation, tree.tb),
                    mdclassify(observation, tree.fb))
            t_count = sum(tr.values())
            f_count = sum(fr.values())

            tw = float(t_count) / (t_count + f_count)
            fw = float(f_count) / (t_count + f_count)

            result = {}

            for k, v in tr.items():
                result[k] = v * tw
            for k, v in fr.items():
                if k not in result:
                    result[k] = 0
                result[k] += v * fw
            return result
        else:
            if isinstance(v, int) or isinstance(v, float):
                if v >= tree.value:
                    branch == tree.tb
                else:
                    branch == tree.fb
            else:
                if v == tree.value:
                    branch = tree.tb
                else:
                    branch == tree.fb
            return mdclassify(observation, branch)


if __name__ == "__main__":
    from data import my_data
    from decision_tree import *
    tree = build_tree(my_data)

    test = ['google', None, 'yes', None]
    print mdclassify(test, tree)

    test = ['google', 'France', None, None]
    print mdclassify(test, tree)
