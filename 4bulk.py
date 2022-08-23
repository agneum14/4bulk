import requests
from bs4 import BeautifulSoup
import urllib.request
import argparse
import os

names = []
urls = []

parser = argparse.ArgumentParser(description='download all media from 4chan thread')
parser.add_argument('-d',
                    metavar='DIR',
                    type=str,
                    help='download to DIR')
parser.add_argument('url',
                    type=str,
                    help='thread url')
args = parser.parse_args()

if args.d:
    if os.path.isfile(args.d):
        print('error:', args.d, 'is a file')
        exit(0)
    elif not os.path.isdir(args.d):
        try:
            os.mkdir(args.d)
        except PermissionError:
            print('error: insufficient permissions to create', args.d)
            exit(0)

page = requests.get(args.url)
soup = BeautifulSoup(page.text, 'html.parser')

for a in soup.select('div.fileText a'):
    name = a['title'] if a.has_attr('title') else a.text.strip()
    names.append(name)
    urls.append('https:' + a['href'])

for i, (url, name) in enumerate(zip(urls, names)):
    path = os.path.join(args.d, name) if args.d else name
    urllib.request.urlretrieve(url, path)
    print(path)