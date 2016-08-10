#coding:utf-8


class DecisionNode(object):

    def __init__(self, col=-1, value=None,
            results=None, tb=None, fb=None):
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb


def divide_set(rows, column, value):
    split_funtion = None
    # function program
    if isinstance(value, int) or isinstance(value, float):
        split_funtion = lambda row:row[column] >= value
    else:
        split_funtion = lambda row:row[column] == value

    set1 = [row for row in rows if split_funtion(row)]
    set2 = [row for row in rows if not split_funtion(row)]

    return (set1, set2)


def unique_counts(rows):
    results = {}
    for row in rows:
        r = row[len(row) - 1]
        if r not in results:
            results[r] = 0
        results[r] += 1
    return results


def gini_impurity(rows):
    total = len(rows)
    counts = unique_counts(rows)
    imp = 0.0
    for k1 in counts:
        p1 = float(counts[k1]) / total
        for k2 in counts:
            if k1 == k2:
                continue
            p2 = float(counts[k2]) / total
            imp += p1 * p2
    return imp


def entropy(rows):
    from math import log
    log2 = lambda x: log(x) / log(2)
    results = unique_counts(rows)

    ent = 0.0
    for r in results.keys():
        p = float(results[r]) / len(rows)
        ent -= p * log2(p)
    return ent


def build_tree(rows, scoref=entropy):
    if len(rows) == 0:
        return DecisionNode()

    current_score = scoref(rows)
    best_gain = 0.0
    best_criteria = None
    best_sets = None
    column_count = len(rows[0]) - 1
    for c in range(column_count):

        column_values = set([row[c] for row in rows])
        for value in column_values:
            (set1, set2) = divide_set(rows, c, value) 
            p = float(len(set1)) / len(rows)
            gain = current_score - p * scoref(set1) - (1 - p) * scoref(set2)

            if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                best_gain = gain
                best_criteria = (c, value)
                best_sets = (set1, set2)
 
    if best_gain > 0:
        true_branch = build_tree(best_sets[0])
        false_branch = build_tree(best_sets[1])
        return DecisionNode(col=best_criteria[0], value=best_criteria[1],
                tb=true_branch, fb=false_branch)

    else:
        return DecisionNode(results=unique_counts(rows))
