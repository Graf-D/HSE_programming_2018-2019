import stemmer
import links_parser
import text_parser
import files_writing
import os
import pandas as pd


metadata = pd.read_csv('metadata.csv', sep='\t')

# get all articles from site
articles = links_parser.get_articles()
for article in articles:
    curr_text = text_parser.get_paragraphs(article.link)
    article.text = text_parser.clean_paragraphs(curr_text)

words = 0  # counting how much words are in all articles
for article in articles:
    for elem in article.text:
        words += len(elem.split())

    file_path = files_writing.gen_file_path(article)
    files_writing.article_to_file(article, file_path)

    new_row = files_writing.make_dataframe_dict(file_path, article.author,
                                                article.header, article.date,
                                                article.topic, article.link)

    metadata = metadata.append(new_row, ignore_index=True)

metadata.to_csv('test_metadata.csv', sep='\t')

stemmer.make_copies()
stemmer.gen_mystem_files()
