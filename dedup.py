#!/usr/local/bin/python

import json
import io
import os
from glob import glob
from collections import defaultdict

#Deduplicate scraped articles from tz press
#
#input: json files in a root directory named "feeds", one per scrape, with
#       filenames formatted <PUBLICATION_NAME>_<ISO_8601_DATE>.json
#
#output: json files of unique artcles, one file per day, in a directory
#        named "deduped"
#
#usage: first sync output files if needed:
#
#         s3cmd sync s3://tzscrape . 
#
#       then run this script to deduplicate:       
#
#         ./dedup.py

input_root = "feeds"
output_root = "deduped"

def main():  
  for publication_name in os.listdir(input_root):
    dedup_publication(publication_name)

def dedup_publication(publication_name):
  print "Processing %s" % publication_name
  processed_count = 0
  output_count = 0
  titles = set()
  dated = defaultdict(list)

  publication_path = os.path.abspath("%s/%s" % (input_root, publication_name))
  for filename in glob("%s/*.json" % publication_path):
    with open(filename, "rb") as infile:
      data = json.load(infile)
      processed_count += len(data)
      for article in data:
        has_title = len(article["title"])
        try:
          title = article["title"][0]
          if title not in titles:
            dated[article["scraped_at"][:10]].append(article)
            titles.add(title)
            output_count += 1
        except IndexError:
          print "article does not have title: %s" % article["url"]

  output_dir = "%s/%s" % (output_root, publication_name)
  if not os.path.exists(output_dir):
      print "\tOutput directory not found, creating %s" % output_dir
      os.makedirs(output_dir)

  for date in dated:
    destination = "%s/%s.json" % (output_dir, date)
    with io.open(destination, 'w', encoding='utf-8') as outfile:
      outfile.write(unicode(json.dumps(dated[date], ensure_ascii=False)))

  print "%s:" % publication_name
  print "\t%s articles processed" % processed_count
  print "\t%s unique articles output" % output_count

if __name__ == "__main__":
    main()


