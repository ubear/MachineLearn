#!/usr/bin/env python
# encoding: utf-8

from math import log


def cals_shannon_ent(data_set):
    num_entries = len(data_set)
    label_counts = {}
    for feature_vector in data_set:
        current_label = feature_vector[-1]
        if current_label not in label_counts.keys():
            label_counts[current_label] = 0
        label_counts[current_label] += 1
    shannon_ent = 0.0
    for key in label_counts:
        prob = float(label_counts[key]) / num_entries
        shannon_ent -= prob * log(prob, 2)
    return shannon_ent


def split_dataset(dataset, axis, value):
    ret_dataset = []
    for feature_vector in dataset:
        if feature_vector[axis] == value:
            reduced_feacture_vec = feature_vector[:axis]
            reduced_feacture_vec.extend(feature_vector[axis+1:])
            ret_dataset.append(reduced_feacture_vec)
    return ret_dataset


def create_dataset():
    dataset = [
        [1, 1, 'yes'],
        [1, 1, 'yes'],
        [1, 0, 'no'],
        [0, 1, 'no'],
        [0, 1, 'no']
    ]
    labels = ['no surfacing', 'flippers']
    return dataset, labels


def get_majority_classify(class_list):
    class_count = {}
    for key in class_list:
        if key not in class_count:
            class_count[key] = 0
        class_count[key] += 1
        return sorted(class_count.iteritems(), lambda x:x[1], reverse=True)[0][0]


def choose_best_spilt_feature(dataset):
    num_features = len(dataset[0]) - 1
    base_entropy = cals_shannon_ent(dataset)
    best_info_gain = 0.0 # Info Gain
    best_feature = -1 # default
    for i in xrange(num_features):
        feature_list = [x[i] for x in dataset]
        unique_values = set(feature_list)
        new_entropy = 0.0
        for value in unique_values:
            sub_dataset = split_dataset(dataset, i, value)
            prob = len(sub_dataset) / float(len(dataset))
            new_entropy += prob * cals_shannon_ent(sub_dataset)
        info_gain = base_entropy - new_entropy

        if(info_gain > best_info_gain):
            best_info_gain = info_gain
            best_feature = i
    return best_feature


def create_tree(dataset, labels):
    class_list = [x[-1] for x in dataset]
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]

    if len(dataset[0]) == 1:
        return get_majority_classify(class_list)

    best_feature = choose_best_spilt_feature(dataset)
    best_label = labels[best_feature]
    decide_tree = {best_label: {}}
    del labels[best_feature]
    feature_values = [x[best_feature] for x in dataset]
    unique_values = set(feature_values)
    for value in unique_values:
        sub_labels = labels[:]
        decide_tree[best_label][value] = create_tree(
                split_dataset(dataset, best_feature, value), sub_labels)
    return decide_tree


def classify(input_tree, feature_labels, test_vector):
    first_labels = input_tree.keys()[0]
    feature_index = feature_labels.index(first_labels)
    second_dict = input_tree[first_labels]
    for key in second_dict:
        if test_vector[feature_index] == key:
            if type(second_dict[key]).__name__ == 'dict':
                class_label = classify(second_dict[key], feature_labels, test_vector)
            else:
                class_label = second_dict[key]
    return class_label


if __name__ == '__main__':
    dataset, labels = create_dataset()
    # print cals_shannon_ent(dataset)
    # print cals_shannon_ent(dataset)
    # print split_dataset(dataset, 0, 0)
    # print choose_best_spilt_feature(dataset)
    decide_tree = create_tree(dataset, labels[:])
    print labels
    print decide_tree
    print classify(decide_tree, labels, [1, 1])
