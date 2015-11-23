#!/usr/local/bin/python

import json
import os
import io
from glob import glob
from nltk.tokenize import RegexpTokenizer

from nltk.corpus import stopwords

input_root = "deduped"
output_root = "all_articles"

def main():  
  for publication_name in os.listdir(input_root):
    concat_publication(publication_name)

def concat_publication(publication_name):
  print "Processing %s" % publication_name
  all_articles = []

  publication_path = os.path.abspath("%s/%s" % (input_root, publication_name))
  for filename in glob("%s/*.json" % publication_path):
    with open(filename, "rb") as infile:
      data = json.load(infile)
      for article in data:
        del article['body']
      all_articles.extend(data)

  if not os.path.exists(output_root):
      print "\tOutput directory not found, creating %s" % output_root
      os.makedirs(output_root)

  destination = "%s/%s.json" % (output_root, publication_name)
  with io.open(destination, 'w', encoding='utf-8') as outfile:
    outfile.write(unicode(json.dumps(all_articles, ensure_ascii=False)))

if __name__ == "__main__":
  main()