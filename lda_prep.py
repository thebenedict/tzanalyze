#!/usr/local/bin/python

import json
import os
import io
from glob import glob
from nltk.tokenize import sent_tokenize, RegexpTokenizer

from nltk.corpus import stopwords

input_root = "deduped"
output_root = "lda_ready"
tokenizer = RegexpTokenizer(r'\w+')

selected_term = "election"

def main():  
  for publication_name in os.listdir(input_root):
    clean_publication(publication_name)

def clean_publication(publication_name):
  print "Processing %s" % publication_name
  cleaned_sentences = []

  publication_path = os.path.abspath("%s/%s" % (input_root, publication_name))
  for filename in glob("%s/*.json" % publication_path):
    with open(filename, "rb") as infile:
      data = json.load(infile)
      cleaned_sentences.extend(clean_articles(data))

  if not os.path.exists(output_root):
      print "\tOutput directory not found, creating %s" % output_root
      os.makedirs(output_root)

  destination = "%s/%s.json" % (output_root, publication_name)
  with io.open(destination, 'w', encoding='utf-8') as outfile:
    outfile.write(unicode(json.dumps(cleaned_sentences, ensure_ascii=False)))

def clean_articles(articles):
  cleaned_articles = []
  for article in articles:
    current_article = []
    for paragraph in article['body']:
      current_article.extend(clean_paragraph(paragraph))
    for sentence in current_article:
      if selected_term in sentence:
        cleaned_articles.extend(current_article)
        break
  return cleaned_articles
   
def clean_paragraph(paragraph):
  clean_sentences = []
  text = paragraph.lower().encode("ascii", errors="ignore")
  raw_sentences = sent_tokenize(text)
  for sent in raw_sentences:
    words = tokenizer.tokenize(sent)
    clean_sentences.append([w.strip() for w in words if (w not in stopwords.words('english'))])
  return clean_sentences

if __name__ == "__main__":
  main()