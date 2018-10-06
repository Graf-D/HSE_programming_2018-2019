import requests
from collections import defaultdict, Counter


BASE_URL = 'https://api.github.com'
TOKEN = open('token.txt', 'r').read()


'''
# uncomment it if Counter would be bad
class MyDict(dict):
    def __add__(self, other):
        for key, value in other.items():
            if key in self.keys():
                self[key] += value
            else:
                self[key] = value
        return self
'''


def choose_user(all_users):
    print('Список всех доступных пользователей:\n',
          ', '.join(all_users), sep='', end='\n\n')
    username = input('Введите имя пользователя из этого списка: ')
    while username not in all_users:
        username = input('Такого пользователя нет в списке. Введите заново: ')
    return username


def get_repos(username):
    repos = []
    page = 1
    while True:
        curr_repos = requests.get(
            '{}/users/{}/repos?page={}&per_page=100&access_token={}'.format(BASE_URL, username, page, TOKEN)
        ).json()
        if not curr_repos:
            break

        repos += curr_repos
        page += 1
    return repos


def print_names_and_descr(repos):
    # красивый вывод названий и описаний репозиториев
    print('\nСписок репозиториев с описаниями:\n')
    for rep in repos:
        description = rep['description']
        if description is None:
            description = 'No description :('
        print(rep['name'], description, sep='\n', end='\n\n')


def count_languages(repos):
    languages_using = defaultdict(int)
    for rep in repos:
        languages_using[rep['language']] += 1
    try:
        del languages_using[None]  # отсутствие языка – не язык
    except KeyError:
        pass
    return languages_using


def get_followers(username):
    followers = []
    page = 1
    while True:
        curr_followers = requests.get(
            '{}/users/{}/followers?page={}&per_page=100&access_token={}'.format(BASE_URL, username, page, TOKEN)
        ).json()
        if not curr_followers:
            break
        followers += curr_followers
        page += 1
    return followers


def right_grammar_case(number):
    if number % 10 == 1:
        return 'репозитории'
    else:
        return 'репозиториях'


# в users.txt лежит список всех юзеров
with open('users.txt', 'r') as f:
    users = f.read().split()

# выбор пользователя из списка
username = choose_user(users)
print('Вы выбрали пользователя {}. Загружаю репозитории.'.format(username))

# вывод названий и описаний
repos = get_repos(username)
print_names_and_descr(repos)

languages_stat = count_languages(repos)

# все языки пользователя
print('{} пишет на'.format(username),
      ', '.join(languages_stat.keys()), end='.\n')

# статистика по использованию языков в репозиториях
for lang, counter in languages_stat.items():
    print('{} используется в {} {}.'.format(lang, counter, right_grammar_case(counter)))

users_repos = {}
for user in users:
    users_repos[user] = get_repos(user)

# поиск пользователя с максимальным кол-вом репозиториев
max_user = max(users, key=(lambda user: len(users_repos[user])))
max_repos = len(users_repos[max_user])

print()
print('Больше всего ({}) репозиториев у {}.'.format(max_repos, max_user))

# поиск самого популярного языка
all_users_languages = sum((Counter(count_languages(users_repos[user])) for user in users), Counter())

'''
all_users_languages = Counter()
for user in users:
    curr_languages = count_languages(users_repos[user])
    all_users_languages += Counter(curr_languages)
'''

max_lang = max(all_users_languages, key=all_users_languages.get)
max_uses = all_users_languages[max_lang]
print('Самый популярный язык – {}.'.format(max_lang))

# поиск наибольшего кол-ва подписчиков
max_followers = 0
max_user = ''
for user in users:
    curr_followers = get_followers(user)
    if len(curr_followers) > max_followers:
        max_followers = len(curr_followers)
        max_user = user
print('Больше всего подписчиков ({}) у {}'.format(max_followers, max_user))
