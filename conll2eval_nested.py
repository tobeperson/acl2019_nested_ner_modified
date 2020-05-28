#!/usr/bin/env python3
# coding=utf-8
#
# Copyright 2019 Institute of Formal and Applied Linguistics, Faculty of
# Mathematics and Physics, Charles University, Czech Republic.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Creates an evaluation file with named entities.

Input: CoNLL file with linearized (encoded) nested named entity labels
delimited with |.

Output: One entity mention per line, two columns per line separated by table.
First column are entity mentino token ids separated by comma, second column is
a BIO or BILOU label.

The output can be then evaluated with compare_nested_entities.py.
""" 

import sys

COL_SEP = "\t"

def raw(label):
    return label[2:]


if __name__ == "__main__":

    i = 0
    running_ids= []
    running_forms= []
    running_labels = []
    pall = 0
    for line in sys.stdin:
        line = line.rstrip("\r\n")
        if not line: # flush entities  \n
            pass
        else:
            form, _, _, ne = line.split("\t")
            if ne == "O": # flush entities
                pall=0
                running_ids = []
                running_forms = []
                running_labels = []
            else:
                labels = ne.split("|")
                for j in range(len(labels)): # for each label
                    label = labels[j]
                    if label.startswith("B-") or label.startswith("U-"):
                        pall = pall + 1
                        running_ids.append([str(i)])
                        running_forms.append([form])
                        running_labels.append([raw(label)])
                    else:
                        # previous running entity ends here, print and insert new entity instead
                        flag=0
                        for pal in range(0,len(running_ids)):
                            if label.startswith("L-") and running_labels[pal][0]== raw(label):
                                running_ids[pal][0] += "," + str(i)
                                running_forms[pal][0] += " " + form
                                running_labels[pal][0] = raw(label)
                                flag=flag+1
                            elif running_labels[pal][0]==raw(label):
                                    running_ids[pal][0]+= "," + str(i)
                                    running_forms[pal][0] += " " + form
                                    running_labels[pal][0] = raw(label)
                        pal=0
                        while flag>=1 :
                            if running_labels[pal][0]== raw(label):
                                print(running_ids[pal][0] + COL_SEP + running_labels[pal][0] + COL_SEP + running_forms[pal][0])
                                del running_ids[pal]
                                del running_labels[pal]
                                del running_forms[pal]
                                pall -= 1
                                flag=flag-1
                            else :pal=pal+1

        i += 1
