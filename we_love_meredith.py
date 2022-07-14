import random
import requests
from os.path import exists
from bs4 import BeautifulSoup
import re
import os

def pick():
    with open('lyrics.txt', 'r', encoding="utf-8") as f:
        print(r"{}".format((random.choice(f.readlines())[:-1])))

def pull_songs():
    print('lyrics.txt not found, pulling lyrics...')
    songs = []
    loop = 1
    while True:
        r = requests.get(f'https://genius.com/api/artists/196665/songs?page={str(loop)}&sort=popularity').json()['response']['songs']
        if len(r) == 0:
            break
        for song in r:
            songs.append('https://genius.com'+song['path'])
        loop += 1

    raw_lyrics = []
    for url in songs:
        print(url)
        text = BeautifulSoup(requests.get(url).text, 'html.parser').find('div', class_="Lyrics__Container-sc-1ynbvzw-6 YYrds")
        if text == None:
            continue
        song_lyrics = os.linesep.join([s for s in re.sub(r'[\(\[].*?[\)\]]', '', text.get_text(separator='\n')).splitlines() if s])
        raw_lyrics.extend(song_lyrics.split('\n'))
        raw_lyrics[-1] +='\n'

    lyrics = []
    for lyric in raw_lyrics:
        if lyric not in lyrics: lyrics.append(lyric)
    write = ''
    with open('lyrics.txt', 'w', encoding="utf-8") as f:
        for line in lyrics:
            write = write + line
        f.write(write)
    pick()
if exists('lyrics.txt'):
    pick()
else:
    pull_songs()
