#!/usr/local/bin/python

import json
import os
import io
from glob import glob
from collections import defaultdict
from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer

input_root = "deduped"
output_root = "sentences"
word_tokenizer = RegexpTokenizer(r'\w+')

def main():  
  for publication_name in os.listdir(input_root):
    clean_sentences(publication_name)

def clean_sentences(publication_name):
  print "Processing %s" % publication_name
  publication_sentences = []

  publication_path = os.path.abspath("%s/%s" % (input_root, publication_name))
  for filename in glob("%s/*.json" % publication_path):
    with open(filename, "rb") as infile:
      data = json.load(infile)
      publication_sentences.extend(articles_to_sentences(data))

  if not os.path.exists(output_root):
      print "\tOutput directory not found, creating %s" % output_root
      os.makedirs(output_root)

  destination = "%s/%s.json" % (output_root, publication_name)
  with io.open(destination, 'w', encoding='utf-8') as outfile:
    outfile.write(unicode(json.dumps(publication_sentences, ensure_ascii=False)))

def articles_to_sentences(articles):
  daily_sentences = []
  for article in articles:
    for paragraph in article['body']:
      daily_sentences.extend(paragraph_to_sentences(paragraph))
  return daily_sentences
   
def paragraph_to_sentences(paragraph):
  sentence_list = []
  text = paragraph.lower().encode("ascii", errors="ignore")
  sentences = sent_tokenize(text)
  for sent in sentences:
    sentence_list.append(word_tokenizer.tokenize(sent))
  return sentence_list

if __name__ == "__main__":
  main()
