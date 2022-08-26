import requests
from bs4 import BeautifulSoup
import urllib.request
import argparse
import os
from concurrent.futures import ThreadPoolExecutor
import psutil

names = []
urls = []
pool = ThreadPoolExecutor(max_workers=psutil.cpu_count())

parser = argparse.ArgumentParser(description='download all media from 4chan thread')
parser.add_argument('-d',
                    metavar='DIR',
                    type=str,
                    help='download to DIR')
parser.add_argument('url',
                    type=str,
                    help='thread URL')
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

try:
    page = requests.get(args.url)
except requests.exceptions.MissingSchema:
    print("error: invalid URL") 
    exit(0)
soup = BeautifulSoup(page.text, 'html.parser')

for a in soup.select('div.fileText a'):
    name = a['title'] if a.has_attr('title') else a.text.strip()
    names.append(name)
    urls.append('https:' + a['href'])

def dl(name, url):
    path = os.path.join(args.d, name) if args.d else name
    urllib.request.urlretrieve(url, path)
    print(path)

futures = [pool.submit(dl, name, url) for name, url in zip(names, urls)]
