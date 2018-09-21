import random
import messages
from ascii_pictures import gallows


ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
GRAMMAR_CASE = ('', 'ошибку',
                'ошибки', 'ошибки', 'ошибки',
                'ошибок', 'ошибок', 'ошибок', 'ошибок', 'ошибок')


# user chooses topic to play
def choose_topic(*topics):
    correct_ans = False
    while not correct_ans:
        print('Выберите тему:',
              ', '.join(topics[:-1]), 'или {}.'.format(topics[-1]))
        ans = input().lower()
        if ans in topics:
            correct_ans = True
            print('Вы выбрали тему {}.'.format(ans), end='\n\n')
        else:
            print('К сожалению, такой темы нет.')
    return ans


# this function chooses random word from user's topic
def random_word(topic):
    files = {'животные': 'animals.txt',
             'столицы мира': 'capitals.txt',
             'программирование': 'programming.txt'}

    with open(files[topic], 'r', encoding='utf-8') as f:
        return random.choice(f.readlines()).strip()


def get_letter(user_letters):
    is_repeated = (lambda s: s in user_letters)
    checks = {(lambda s: len(s) != 1): 'Нужно ввести одну букву.',
              (lambda s: s not in ALPHABET): 'Это не буква русского алфавита.',
              is_repeated: 'Вы уже вводили эту букву.'}

    counter = 0
    while True:
        letter = input('Введите какую-нибудь букву: ').lower()
        for check, message in checks.items():
            if check(letter):
                print(message)
                if check == is_repeated:
                    counter += 1
                    if counter >= 5:
                        print('Вот все буквы, которые уже были:',
                              ' '.join(user_letters))
                break
        else:
            return letter


# user will see only guessed letters
def print_word(word, letters):
    for char in word:
        if char in letters:
            print(char, end=' ')
        else:
            print('_', end=' ')
    print()


def game():
    # starting game
    topic = choose_topic('животные', 'столицы мира', 'программирование')
    word = random_word(topic)
    user_letters = set()
    is_guessed = False
    lost = False
    right_letters = 0
    mistakes_left = 10

    # main part of the game
    while not is_guessed and not lost:
        print_word(word, user_letters)
        curr_letter = get_letter(user_letters)
        user_letters.add(curr_letter)

        if curr_letter in word:
            print(random.choice(messages.success))
            right_letters += word.count(curr_letter)
        else:
            print(random.choice(messages.failure))
            mistakes_left -= 1
            if mistakes_left == 0:  # checking if game is over
                lost = True
                if topic == 'столицы мира':
                    word = word.title()
                print('Вы проиграли :( Было загадано слово {}.'.format(word))
            else:
                print('Вы можете сделать еще {} {}.'.format(mistakes_left,
                                                            GRAMMAR_CASE[mistakes_left]))
                print(gallows[9 - mistakes_left])

        if right_letters == len(word):  # user guessed all letters
            is_guessed = True
            if topic != 'столицы мира':
                print('Поздравляем, вы отгадали слово! Это {}.'.format(word))
            else:
                print('Поздравляем, вы отгадали город! Это {}.'.format(word.title()))

        '''stop = input('stop?')
        if stop == 'y':
            break'''


while True:
    game()
    play_again = None
    while play_again != 'да' and play_again != 'нет':
        if play_again is None:
            play_again = input('Хотите сыграть еще раз? да/нет ').lower()
        else:
            play_again = input('Введите да или нет: ')
    if play_again == 'да':
        print('Ок, начинаем!', end='\n\n')
    else:
        print('Ладно, до свидания.')
        break
