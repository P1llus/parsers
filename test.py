import os
import re
import sys

# All regular expressions to look for
PUB_IP = re.compile(r'(\d+)(?<!10)\.(\d+)(?<!192\.168)(?<!172\.(1[6-9]|2\d|3[0-1]))(?<!100\.64)\.(\d+)\.(\d+)')
LOCAL_IP = re.compile(r'\d+.\d+.\d+.\d+')

# Which folders to ignore
IGNORED_FOLDERS = ['.\.git']

ALL_RESULTS = {}

def get_parsers():
  list_of_files = []
  for folder in [f.path for f in os.scandir() if f.is_dir()]:
    if folder not in IGNORED_FOLDERS:
      for root, dir, files in os.walk(folder):
        for file in files:
          if file:
            list_of_files.append(os.path.join(root, file))
  return list_of_files

def get_matches(parser, resultdict):
  line_results = []
  for num, line in enumerate(open(parser, 'rb')):
    for match in PUB_IP.finditer(str(line)):
      if match:
        line_results.append('Public IP {} found on line {}'.format(match.group(), num + 1))
      else:
        break
  if line_results:
    resultdict[parser] = line_results
    line_results = []
  return resultdict

def list_matches(results):
  for parser in results.keys():
      if parser:
        print('{} in file {}'.format(ALL_RESULTS[parser][0], parser))

if __name__ == "__main__":
  parsers = get_parsers()
  for parser in parsers:
    get_matches(parser, ALL_RESULTS)
  if any(v is not None for v in ALL_RESULTS.values()):
    list_matches(ALL_RESULTS)
    sys.exit(1)
  else:
    sys.exit(0)