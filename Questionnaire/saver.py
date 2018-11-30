import json
from conf import *


def save_to_csv(data={}):
    with open(CSV_FILENAME, 'a', encoding='utf-8') as f:
        print()
        print('\t'.join(data.values()), file=f, end='')


def gen_json(csv_file=CSV_FILENAME, this_sep='\t',
             must_contain=[], min_age=0, max_age=150):

    with open(csv_file, 'r', encoding='utf-8') as f:
        data = f.read().split('\n')

    json_ = {'answers': []}
    for i in range(1, len(data)):
        #  (for search) checking that current row contains all necessary words
        for elem in must_contain:
            if elem not in data[i]:
                break
        #  if there are all the words, proceed
        else:
            lang, age, apple, axe, horse = data[i].split(this_sep)
            if min_age <= int(age) <= max_age:
                curr_data = {'lang': lang,
                             'age': age,
                             'apple': apple,
                             'axe': axe,
                             'horse': horse}

                json_['answers'].append(curr_data)

    return json.dumps(json_, ensure_ascii=False)
