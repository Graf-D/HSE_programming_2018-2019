import os


def make_copies():
    for root, dirs, files in os.walk('plain'):
        if not dirs:
            for file in files:
                with open(root + os.sep + file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                copy_name = root + os.sep + 'onlytext' + file
                with open(copy_name, 'w', encoding='utf-8') as f:
                    for i in range(5, len(lines)):
                        print(lines[i], end='', file=f)


def gen_mystem_files():
    start_dir = os.getcwd() + os.sep + 'plain'
    dirs = os.listdir(start_dir)
    for root, dirs, files in os.walk(start_dir):
        if files:
            for file in files:
                if 'onlytext' in file:
                    filename = file[9:-4]
                    source = root + os.sep + file
                    save_to = os.path.join(*[start_dir[:-6],
                                             'mystem-plain',
                                             root[62:],
                                             filename + '.txt'])
                    os.system(' '.join(['C:\mystem.exe', source, save_to,
                              '-i', '-l', '-c', '-d', '--eng-gr']))

                    save_to = os.path.join(*[start_dir[:-6],
                                             'mystem-xml',
                                             root[62:],
                                             filename + '.xml'])
                    os.system(' '.join(['C:\mystem.exe', source, save_to,
                                        '-i', '-l', '-c', '-d', '--eng-gr',
                                        '--format=xml']))
