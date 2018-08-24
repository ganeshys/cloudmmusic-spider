# encoding=utf-8
import requests
from bs4 import BeautifulSoup
from lxml import html
import re
import time
import json


class Hiphop_spider(object):

    def __init__(self):
        self.headers = {
            'Host': 'music.163.com',
            'Referer': 'https://music.163.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        self.cookies = {'appver': '1.5.2'}

    # 获取歌单信息（参数：歌单的id)
    def get_playlist_detail(self, playlist_id):
        url = 'http://music.163.com/api/playlist/detail'
        payload = {'id': playlist_id}

        r = requests.get(url, params=payload, headers=self.headers, cookies=self.cookies)
        playlist_detail = r.json()['result']['tracks']
        # print(playlist_detail)
        return playlist_detail

    def get_song_list(self, playlist_id):
        playlist_detail = self.get_playlist_detail(playlist_id)
        songlist = []
        for song_deatil in playlist_detail:
            song = {}
            song['id'] = song_deatil['id']
            song['name'] = song_deatil['name']
            artists_detail = []
            for artist in song_deatil['artists']:
                artist_detail = {}
                artist_detail['name'] = artist['name']
                artist_detail['id'] = artist['id']
                artists_detail.append(artist_detail)
            song['artists'] = artists_detail
            songlist.append(song)
        # print(songlist)
        return songlist

    def get_artists_songlist(self, playlist_id):
        songlist = self.get_song_list(playlist_id)
        singerid = []
        songid = []
        print(songlist)
        for song in songlist:
            singerlist = song['artists']
            for singer in singerlist:
                singerid.append(singer['id'])
            # print(singerid)
        # 删除列表中重复的元素
        singerid_norepeat = list(set(singerid))
        singerid_norepeat.remove(0)
        singerid_norepeat.remove(12118273)
        singerid_norepeat.remove(12139451)
        singerid_norepeat.remove(1049545)
        singerid_norepeat.remove(12295180)
        singerid_norepeat.remove(12119335)
        singerid_norepeat.remove(1949)
        # 拿到歌单中各个艺人的id
        print(singerid_norepeat)
        # 拼接url
        for artists_id in singerid_norepeat:
            url = 'http://music.163.com/artist/{}'.format(artists_id)
            print(url)
            r = requests.get(url, headers=self.headers, cookies=self.cookies).text
            # print(r.text)
            soupObj = BeautifulSoup(r, 'lxml')
            song_ids = soupObj.find('textarea').text
            # print(song_ids)
            jobj = json.loads(song_ids)
            for item in jobj:
                songid.append(item['id'])
        songid = songid
        # print(songid)
        return list(set(songid))

    # 拿到歌词
    def get_song_lyric(self, playlist_id):
        lyric_list = []
        song_id = self.get_artists_songlist(playlist_id)
        # print(song_id)
        for songid in song_id:
            url = 'http://music.163.com/api/song/lyric?' + '&os=pc&' + 'id=' + str(songid) + '&lv=1&kv=1&tv=-1'
            # print(url)
            r = requests.get(url, headers=self.headers, cookies=self.cookies)
            result = r.json()
            # print(result)
            if "lrc" in result:
                lrc = result['lrc']['lyric']
                regex = re.compile(r'\[.*\]')
                final_lrc = re.sub(regex, '', lrc).strip()
                # print(final_lrc)
                lyric_list.append(final_lrc)
        print(lyric_list)
        return lyric_list


if __name__ == '__main__':
    spider = Hiphop_spider()
    test = spider.get_song_lyric(813277600)
    # test = spider.get_artists_songlist(950575570)
    # test = spider.get_artists_songlist(727360991)
    with open('lyric1.json', 'w') as f:
        json.dump(test, f)
    # with open('lyric1.json', 'w', encoding='utf-8') as f:
    #     json.dump(test, f, ensure_ascii=False)
    print('Done')
