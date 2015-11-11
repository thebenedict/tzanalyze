#!/usr/local/bin/python

import os
import json
import io
import time
import datetime
from glob import glob
from collections import defaultdict
from operator import itemgetter

terms = [
  ["seif","seif"],
  ["poll","uchaguzi"],
  ["twaweza","twaweza"], 
  ["CCM","CCM"],
  ["CHADEMA","CHADEMA"],
  ["Magufuli","Magufuli"],
  ["Lowassa","Lowassa"],
  ["Slaa","Slaa"],
  ["TFDA","TFDA"],
  ["TCRA","TCRA"],
  ["corruption","rushwa"],
  ["obama","obama"],
  ["usaid","usaid"],
  ["msd","msd"],
  ["kenya","kenya"],
  ["MCC","MCC"],
  ["elephant","tembo"],
  ["Zanzibar","Zanzibar"],
  ["riots","ghasia"],
  ["vote","vote"],
  ["election","uchaguzi"],
  ["ukawa", "ukawa"]
]

input_root = "cleaned"
output_root = "./pages/data"

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
  text = get_text()
  all_counts = {}

  if not os.path.exists(output_root):
      print "\tOutput directory not found, creating %s" % output_root
      os.makedirs(output_root)  

  for term in terms:
    counts = []
    for publication in text.keys():
      counts.append(get_counts_for_publication(publication, text[publication], term))
    pad_counts(counts);
    sort_counts(counts);
    all_counts["%s-%s" % (term[1], term[0])] = counts

  destination = "%s/counts.json" % (output_root)
  with io.open(destination, 'w', encoding='utf-8') as outfile:
    outfile.write(unicode(json.dumps(all_counts, indent=2, sort_keys=True)))

def get_text():
  text = defaultdict(dict)

  for publication_name in os.listdir(input_root):
    print "Processing %s" % publication_name

    publication_path = os.path.abspath("%s/%s" % (input_root, publication_name))
    for filename in glob("%s/*.json" % publication_path):
      with open(filename, "rb") as infile:
        date_str = os.path.basename(filename).split(".")[0]
        text[publication_name][date_str] = json.load(infile)
  return text

def get_counts_for_publication(name, text, term):
  if languages[name] == "SW":
    term = term[1]
  else:
    term = term[0]

  counts = {'key': name.title().replace("_"," "), 'values': []}
  for i, date in enumerate(text.keys()):
    term_count = 0
    word_count = 0
    for article in text[date]:
      term_count += article.count(" " + term.lower() + " ")
      word_count += len(article)
    oriented_count = term_count * directions[languages[name]]
    if word_count > 0:
      oriented_count = float(oriented_count) / float(word_count) * 100000
    counts['values'].append({'date': date, 'x': get_timestamp(date), 'y': oriented_count})
  return counts

def pad_counts(counts):
  values_list = [c['values'] for c in counts]
  longest_values = max(enumerate(values_list), key = lambda tup: len(tup[1]))[1]
  for c in counts:
    dates = [v['x'] for v in c['values']]
    for v in longest_values:
      if v['x'] not in dates:
        c['values'].append({'x': v['x'], 'y': 0})

def sort_counts(counts):
  for c in counts:
    c['values'] = sorted(c['values'], key=itemgetter('x')) 

def get_timestamp(date):
  date = datetime.datetime.strptime(date, "%Y-%m-%d")
  return time.mktime(date.timetuple()) * 1000

if __name__ == "__main__":
  main()
