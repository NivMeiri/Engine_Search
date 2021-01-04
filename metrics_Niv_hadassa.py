import traceback

import pandas as pd
from functools import reduce

df = pd.DataFrame(
    {'query': [1, 1, 2, 2, 3], 'Tweet_id': [12345, 12346, 12347, 12348, 12349],
     'label': [1, 0, 1, 1, 0]})

test_number = 0
results = []


# precision(df, True, 1) == 0.5
# precision(df, False, None) == 0.5
def precision(df, single=False, query_number=None):
    """
        This function will calculate the precision of a given query or of the entire DataFrame
        :param df: DataFrame: Contains query numbers, tweet ids, and label
        :param single: Boolean: True/False that tell if the function will run on a single query or the entire df
        :param query_number: Integer/None that tell on what query_number to evaluate precision or None for the entire DataFrame
        :return: Double - The precision
    """
    query_num = df.get("query")
    rel = df.get("label")
    rel_list = []
    if (single):
        for i in range(len(query_num)):
            if (query_num[i] == query_number):
                rel_list.append(rel[i])
        rel = rel_list
        num_of_return = len(rel)
        num_of_Rel = len([x for x in rel if x == 1])
        if(num_of_return!=0):
            return (num_of_Rel / num_of_return)
        else:
            return 0
    else:
        set_of_query = set(query_num)
        dict = {x: [0, 0] for x in set_of_query}
        for i in range(len(query_num)):
            dict[query_num[i]][0] += (rel[i])
            dict[query_num[i]][1] += 1
        total_sum = 0
        for value in dict.values():
            total_sum += value[0] / value[1]
        return (total_sum / len(set_of_query))


# recall(df, {1:0}, True) == 0.5
# recall(df, {1:2, 2:3, 3:1}, False) == 0.388
def recall(df, num_of_relevant):
    if (len(num_of_relevant)==1 and list(num_of_relevant.values())[0]==0):
        return None
    query_num=df.get("query")
    rel=df.get("label")
    sum_rel=0
    sum_recall=0
    relevant_query=0
    for key in num_of_relevant.keys():
        for i  in range (len(query_num)):
            if(query_num[i]==key):
                sum_rel+=rel[i]
        if(num_of_relevant[key]!=0):
            relevant_query+=1
            if sum_rel>num_of_relevant[key]:
                sum_recall+=1
            else:
                sum_recall+=(sum_rel / num_of_relevant[key])
        sum_rel=0
    if(len(num_of_relevant))==0:
        return None
    return (sum_recall/relevant_query)
    """
        This function will calculate the recall of a specific query or of the entire DataFrame
        :param df: DataFrame: Contains query numbers, tweet ids, and label
        :param num_of_relevant: Dictionary: number of relevant tweets for each query number. keys are the query number and values are the number of relevant.
        :return: Double - The recall
    """


# precision_at_n(df, 1, 2) == 0.5
# precision_at_n(df, 3, 1) == 0
def precision_at_n(df, query_number=1, n=5):
    """
        This function will calculate the precision of the first n files in a given query.
        :param df: DataFrame: Contains query numbers, tweet ids, and label
        :param query_number: Integer that tell on what query_number to evaluate precision
        :param n: Total document to splice from the df
        :return: Double: The precision of those n documents
    """
    query_num = df.get("query")
    rel = df.get("label")
    rel_list = []
    for i in range(len(query_num)):
        if (query_num[i] == query_number):
            rel_list.append(rel[i])
    if (len(rel_list) > n):
        rel_list = rel_list[:n]
    sum_1 = sum(rel_list)
    if(len(rel_list)>0):
        return sum_1 / len(rel_list)
    else:
        return 0

# map(df) == 2/3
def map(df):
    """
        This function will calculate the mean precision of all the df.
        :param df: DataFrame: Contains query numbers, tweet ids, and label
        :return: Double: the average precision of the df
    """
    rel = df.get("label")
    query_num = df.get("query")
    set_query = set(query_num)
    query_dict = {x: [] for x in set_query}
    for i in range(len(query_num)):
        query_dict[query_num[i]].append(rel[i])
    re_sum = 0
    for val in query_dict.values():
        query_sum = 0
        num_of_rel = 0
        for j in range(len(val)):
            if (val[j] == 1):
                num_of_rel += 1
                query_sum += num_of_rel / (j + 1)
        if (num_of_rel != 0):
            re_sum += query_sum / num_of_rel
    return re_sum / len(set_query)


def test_value(func, expected, variables):
        """
            This function is used to test your code. Do Not change it!!
            :param func: Function: The function to test
            :param expected: Float: The expected value from the function
            :param variables: List: a list of variables for the function
        """
        global test_number, results
        test_number += 1
        result = func(*variables)
        try:
            result = float(f'{result:.3f}')
            if abs(result - float(f'{expected:.3f}')) <= 0.01:
                results.extend([f'Test: {test_number} passed'])
            else:
                results.extend([f'Test: {test_number} Failed running: {func.__name__}'
                                f' expected: {expected} but got {result}'])
        except ValueError as ve:
            results.extend([f'Test: {test_number} Failed running: {func.__name__}'
                            f' value return is not a number'])
        except:
            d = traceback.format_exc().splitlines()
            results.extend([f'Test: {test_number} Failed running: {func.__name__} with the following error: {" ".join(d)}'])

# test_value(precision, 0.5, [df, True, 1])
# test_value(precision, 0.5, [df, False, None])
# test_value(recall, 0.5, [df, {1: 2}])
# test_value(recall, 0.388, [df, {1: 2, 2: 3, 3: 1}])
# test_value(precision_at_n, 0.5, [df, 1, 2])
# test_value(precision_at_n, 0, [df, 3, 1])
# test_value(map, 2 / 3, [df])
# df = pd.read_csv('311277438.csv')
#
# precision
# test_value(precision, 3 / 8, [df, True, 1])
# test_value(precision, 7 / 8, [df, True, 2])
# test_value(precision, 1, [df, True, 3])
# test_value(precision, 0, [df, True, 88])
# test_value(precision, 0.659375, [df, False, None])
#
# # recall
# test_value(recall, 3 / 20, [df, {1: 20}])
# test_value(recall, 3 / 5, [df, {1: 5}])
# test_value(recall, 0, [df, {100: 5}])
# test_value(recall, (3 / 20 + 7 / 8 + 8 / 10) / 3, [df, {1: 20, 2: 8, 3: 10}])
# test_value(recall, (6 / 17 + 0.5 + 2 / 9) / 3, [df, {27: 17, 30: 8, 39: 9}])
# test_value(recall, None, [df, {1: 0}])  # check the value for 0 relevant docs and correct the function
#
#
# # precision_at_n
# test_value(precision_at_n, 3 / 8, [df, 1, 8])
# test_value(precision_at_n, 3 / 8, [df, 1, 20])
# test_value(precision_at_n, 2 / 3, [df, 1, 3])
# test_value(precision_at_n, 4 / 7, [df, 5, 7])
# test_value(precision_at_n, 0, [df, 6, 0])
# test_value(precision_at_n, 0, [df, 7, 1])
# test_value(precision_at_n, 1, [df, 8, 1])
# test_value(precision_at_n, 0, [df, 88, 1])
for res in results:
    print(res)
