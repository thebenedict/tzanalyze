#!/usr/local/bin/python

import json
import os
import io
from glob import glob
from nltk.tokenize import RegexpTokenizer

from nltk.corpus import stopwords

input_root = "deduped"
output_root = "lda_ready_articles"
tokenizer = RegexpTokenizer(r'\w+')

def main():  
  for publication_name in os.listdir(input_root):
    clean_publication(publication_name)

def clean_publication(publication_name):
  print "Processing %s" % publication_name
  cleaned_articles = []

  publication_path = os.path.abspath("%s/%s" % (input_root, publication_name))
  for filename in glob("%s/*.json" % publication_path):
    with open(filename, "rb") as infile:
      data = json.load(infile)
      cleaned_articles.extend(clean_articles(data))

  if not os.path.exists(output_root):
      print "\tOutput directory not found, creating %s" % output_root
      os.makedirs(output_root)

  destination = "%s/%s.json" % (output_root, publication_name)
  with io.open(destination, 'w', encoding='utf-8') as outfile:
    outfile.write(unicode(json.dumps(cleaned_articles, ensure_ascii=False)))

def clean_articles(articles):
  cleaned_articles = []
  for article in articles:
    current_article = []
    for paragraph in article['body']:
      current_article.extend(clean_paragraph(paragraph))
    cleaned_articles.append(current_article)
  return cleaned_articles
   
def clean_paragraph(paragraph):
  text = paragraph.lower().encode("ascii", errors="ignore")
  words = tokenizer.tokenize(text)
  
  #remove stopwords and a few other common words
  to_remove = stopwords.words('english')
  to_remove.extend(['says', 'said', 'told', 'also'])
  clean_words = [w.strip() for w in words if w not in to_remove]

  return clean_words

if __name__ == "__main__":
  main()