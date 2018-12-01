import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from flask import Markup
from collections import defaultdict, OrderedDict
from conf import CSV_FILENAME


def get_average_age():
    df = pd.read_csv(CSV_FILENAME, sep='\t')
    sum_age = 0
    unknown_age = 0
    for index, row in df.iterrows():
        sum_age += row['Возраст']
    return (sum_age / (df.shape[0] - unknown_age))


def draw_age_bar():
    df = pd.read_csv(CSV_FILENAME, sep='\t')
    ages = defaultdict(int)
    for index, row in df.iterrows():
        ages[int(row['Возраст'])] += 1
    bar = plt.bar(list(ages.keys()), list(ages.values()))

    imgdata = StringIO()
    plt.savefig(imgdata, format='svg')
    imgdata.seek(0)
    svg_bar = imgdata.read()

    return Markup(svg_bar)


def sort_languages():
    df = pd.read_csv(CSV_FILENAME, sep='\t')
    lang_usage = defaultdict(int)
    for index, row in df.iterrows():
        lang_usage[row['Язык']] += 1

    sorted_langs = OrderedDict(sorted(lang_usage.items(), key=lambda x: x[1],
                                      reverse=True))
    return sorted_langs
