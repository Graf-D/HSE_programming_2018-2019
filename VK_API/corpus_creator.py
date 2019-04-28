import os.path
from main import posts


dir_ = os.path.join(os.path.dirname(__file__), 'corpus')
plain_corpus = os.path.normpath(os.path.join(dir_, 'plain.txt'))
lemma_corpus = os.path.normpath(os.path.join(dir_, 'lemmatized.txt'))

plain_file = open(plain_corpus, 'w', encoding='utf-8')
lemma_file = open(lemma_corpus, 'w', encoding='utf-8')

for post in posts:
    print(post.text, end='\n\n', file=plain_file)
    print(post.lemmatized_text, end='\n\n', file=lemma_file)
    for comment in post.comments:
        print(comment.text, end='\n\n', file=plain_file)
        print(comment.lemmatized_text, end='\n\n', file=lemma_file)

plain_file.close()
lemma_file.close()
