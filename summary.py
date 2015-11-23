#!/usr/local/bin/python

# TODO accept command line agruments
# TODO allow date range instead of single date

import os
import json
import argparse
from collections import defaultdict
from nltk.tokenize import RegexpTokenizer

input_root = "deduped"

tokenizer = RegexpTokenizer(r'\w+')

def main():
  args = get_args()
  date_string = args.date
  term = args.term.lower()

  data = get_data(date_string)
  print "SUMMARY for %s\n" % date_string

  for publication in data.keys():
    total_count = 0
    article_count = 0
    print publication
    print "-----------"
    for article in data[publication]:
      cleaned_paragraphs = []
      for paragraph in article['body']:
        cleaned_paragraphs.append(clean_paragraph(paragraph))
      cleaned_article = " ".join(cleaned_paragraphs).strip()

      term_count = cleaned_article.count(term)
      if term_count > 0:
        title = article['title'][0].encode("ascii", errors="ignore")
        print "{:80}{:2}".format(title.strip(), term_count)
        print "{:100}".format(article['url'])
        total_count += term_count
        article_count += 1
    print "\n%s mentions in %s articles" % (total_count, article_count)
    print "\n"

def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("term", help="term to search for, not case sensitive e.g. 'zanzibar'")
  parser.add_argument("date", help="date as YYYY-MM-DD, eg. 2015-09-14")
  return parser.parse_args()
   
def clean_paragraph(paragraph):
  text = paragraph.lower().encode("ascii", errors="ignore")
  words = tokenizer.tokenize(text)
  return " ".join(words).strip()

def get_data(date_string):
  data = defaultdict(dict)

  for publication_name in os.listdir(input_root):
    filename = os.path.abspath("%s/%s/%s.json" % (input_root, publication_name, date_string))
    with open(filename, "rb") as infile:
      data[publication_name] = json.load(infile)
  
  print "\n"
  return data

if __name__ == "__main__":
  main()