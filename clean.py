#!/usr/local/bin/python

import json
import os
import io
from glob import glob
from collections import defaultdict
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

input_root = "deduped"
output_root = "cleaned"
tokenizer = RegexpTokenizer(r'\w+')

def main():  
  for publication_name in os.listdir(input_root):
    clean_publication(publication_name)

def clean_publication(publication_name):
  print "Processing %s" % publication_name
  cleaned = defaultdict(list)

  publication_path = os.path.abspath("%s/%s" % (input_root, publication_name))
  for filename in glob("%s/*.json" % publication_path):
    with open(filename, "rb") as infile:
      data = json.load(infile)
      date_str = os.path.basename(filename).split(".")[0]
      cleaned[date_str] = clean_articles(data)

  output_dir = "%s/%s" % (output_root, publication_name)
  if not os.path.exists(output_dir):
      print "\tOutput directory not found, creating %s" % output_dir
      os.makedirs(output_dir)

  for date in cleaned:
    destination = "%s/%s.json" % (output_dir, date)
    with io.open(destination, 'w', encoding='utf-8') as outfile:
      outfile.write(unicode(json.dumps(cleaned[date], ensure_ascii=False)))

def clean_articles(articles):
  cleaned_articles = []
  for article in articles:
    cleaned_article = []
    for paragraph in article['body']:
      cleaned_article.append(clean_paragraph(paragraph))
    cleaned_articles.append(" ".join(cleaned_article).strip())
  return cleaned_articles
   
def clean_paragraph(paragraph):
  text = paragraph.lower().encode("ascii", errors="ignore")
  words = tokenizer.tokenize(text)
  return " ".join(words).strip()
  #clean_words = [w for w in words if (w not in stopwords.words('english'))]
  #return " ".join(clean_words).strip()

if __name__ == "__main__":
  main()