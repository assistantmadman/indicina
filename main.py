import os
import subprocess
import sys
import re
import string
import shlex
import urllib.request
import tmdbsimple as tmdb
from imdbpie import Imdb


def GetMeta(t, y):
    tmdb.API_KEY = 'b888b64c9155c26ade5659ea4dd60e64'
    search = tmdb.Search()
    search.movie(query=t)
    for s in search.results:
        year = s['release_date'].split('-', 2)
        if year[0] == y:
            d = s
            state = True
            break
        else:
            state = False

    imdb = Imdb()
    results = imdb.search_for_title(t)
    if state is True:
        for i in results:
            if i['type'] == 'feature' and i['year'] == y:
                result = i
                g = imdb.get_title_genres(result['imdb_id'])
                d['genre_ids'] = g['genres']
                break
            else:
                d['genre_ids'] = ''
        return d
    else:
        d = {}
        return d


def DownloadFile(u):
    urllib.request.urlretrieve(u, d['poster_path'].lstrip('/'))


def ProcessWriteMeta(f, a, d):
    g = ','.join(map(str, d['genre_ids']))

    cmd = (
        'AtomicParsley ' +
        shlex.quote(f) +
        ' --title "' + d['title'] + '"' +
        ' --genre "' + g + '"' +
        ' --comment "' + d['overview'] + '"' +
        ' --year "' + d['release_date'] + '"' +
        ' --artwork "' + a + '"' +
        ' --stik value=9'
    )
    process = subprocess.run(
        cmd,
        # stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
        # check=True,
        shell=True
    )
    return process.returncode


# Get movie title and year from filename
arg = sys.argv
if len(arg) == 0:
    sys.stdout.write(
        "Syntax error - example: main.py FILENAME"
    )
f = arg[1]
fdate = re.findall('\d\d\d\d', f)

for n in range(len(fdate)):
    if fdate[n] not in ['1080', '2160']:
        y = fdate[n]
    else:
        break
fsplit = f.split(y)

ftitle = fsplit[0]

for char in string.punctuation:
    ftitle = ftitle.replace(char, ' ')

t = ftitle.strip()
d = GetMeta(t, y)

DownloadFile(
    'https://image.tmdb.org/t/p/w780' + d['poster_path']
)

ProcessWriteMeta(f, d['poster_path'].lstrip('/'), d)
