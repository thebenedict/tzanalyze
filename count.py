#!/usr/local/bin/python

import os
import json
import io
from glob import glob
from collections import defaultdict

terms = ["CCM"]

input_root = "cleaned"
output_root = "counts"

languages = {
  "mwananchi": "SW",
  "habarileo": "SW",
  "nipashe": "SW",
  "citizen": "EN",
  "guardian": "EN",
  "daily_news": "EN"
}

directions = {
  "EN": 1,
  "SW": -1
}

def main():
  counts = []
  text = get_text()
  for term in terms:
    for publication in text.keys():
      counts.append(get_counts_for_publication(publication, text[publication], term))

  if not os.path.exists(output_root):
      print "\tOutput directory not found, creating %s" % output_root
      os.makedirs(output_root)

  destination = "%s/%s.json" % (output_root, term)
  with io.open(destination, 'w', encoding='utf-8') as outfile:
    outfile.write(unicode(json.dumps(counts)))

def get_text():
  text = defaultdict(dict)

  #for publication_name in os.listdir(input_root):
  for publication_name in ['citizen', 'mwananchi']:
    print "Processing %s" % publication_name

    publication_path = os.path.abspath("%s/%s" % (input_root, publication_name))
    for filename in glob("%s/*.json" % publication_path):
      with open(filename, "rb") as infile:
        date_str = os.path.basename(filename).split(".")[0]
        text[publication_name][date_str] = json.load(infile)
  return text

def get_counts_for_publication(name, text, term):
  counts = {'key': name, 'values': []}
  for i, date in enumerate(text.keys()):
    term_count = 0
    word_count = 0
    for article in text[date]:
      term_count += article.count(term.lower())
      word_count += len(article)
    oriented_count = term_count * directions[languages[name]]
    normalized_count = float(oriented_count)/float(word_count)
    counts['values'].append({'date': date, 'x': i, 'y': int(normalized_count * 10000)})
  #return counts
  return {'key': counts['key'], 'values': counts['values'][:31]} 

if __name__ == "__main__":
  main()