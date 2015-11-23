#!/usr/local/bin/python

# TODO accept command line agruments
# TODO allow date range instead of single date

import os
import json
import argparse
from collections import defaultdict
from nltk.tokenize import RegexpTokenizer
from datetime import timedelta, date

input_root = "deduped"

tokenizer = RegexpTokenizer(r'\w+')
swahili_publications = ["mwananchi", "habarileo", "nipashe"]
start_date = date(2015, 10, 28)
end_date = date(2015, 11, 18)

def main():
  args = get_args()
  term = args.term.lower()
  
  for d in daterange(start_date, end_date):
    date_string = d.strftime("%Y-%m-%d")
    data = get_data(date_string)

    for publication in data.keys():
      if publication in swahili_publications:
        language = "SW"
      else:
        language = "EN"

      for article in data[publication]:
        cleaned_paragraphs = []
        for paragraph in article['body']:
          cleaned_paragraphs.append(clean_paragraph(paragraph))
        cleaned_article = " ".join(cleaned_paragraphs).strip()

        term_count = cleaned_article.count(term.lower())
        if term_count > 0:
          title = article['title'][0].encode("ascii", errors="ignore")
          print "\"%s\",\"%s\",\"%s\",\"%s\"" % (date_string, publication, language, title)

def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("term", help="term to search for, not case sensitive e.g. 'zanzibar'")
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
  
  return data

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

if __name__ == "__main__":
  main()