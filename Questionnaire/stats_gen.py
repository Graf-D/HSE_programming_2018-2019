import pandas as pd
from collections import defaultdict, OrderedDict
from conf import CSV_FILENAME


def get_average_age():
    df = pd.read_csv(CSV_FILENAME, sep='\t')
    sum_age = 0
    unknown_age = 0
    for index, row in df.iterrows():
        sum_age += row['Возраст']
    return (sum_age / (df.shape[0] - unknown_age))


def sort_languages():
    df = pd.read_csv(CSV_FILENAME, sep='\t')
    lang_usage = defaultdict(int)
    for index, row in df.iterrows():
        lang_usage[row['Язык']] += 1

    sorted_langs = OrderedDict(sorted(lang_usage.items(), key=lambda x: x[1],
                                      reverse=True))
    return sorted_langs
