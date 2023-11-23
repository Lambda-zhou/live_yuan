# import 自己看不需要的可以#批注掉
# invalids, valids  list用于收集检测失败或成功的直播源,已检测的同样的host,不再检测,提高效率!
# filename,newfile路径设置，win和linux肯定不一样
# newfile将是检测后可用的直播源，后缀_ttd，如需自行修改
import time, re, json, requests, random
import os.path
from urllib.parse import urlparse
from pprint import pprint
from lxml import etree
import pandas as pd


def get_lives_data(filename):
    f = open(filename, 'r+')
    r = f.readlines()
    lives_data = [x.strip() for x in r if x.strip() != '']
    # lives_data= list(map(lambda x: x.strip(), r))
    # lives_data=lives_data.remove('')
    f.close()
    return lives_data


def test_url(newfile, lives_data):
    # ll是电视直播源的链接列表
    # ll=['http://........','https://.......']
    invalids, valids = [], []
    # 用于检测失败或成功的net,不再检测,提高效率
    # l=lives_data.index('&#127795;电影直播,#genre#')
    with open(newfile, 'a+') as f:
        # for line in lives_data[:]:
        for line in lives_data:
            if line.find(',http') != -1:
                name = line.split(',http')[0]
                urls = 'http' + line.split(',http')[-1]
                if urls.find('#') != -1:
                    hrefs = urls.split('#')
                else:
                    hrefs = [urls]

                if len(hrefs) == 1:
                    url_parse = urlparse(hrefs[0]).netloc
                    # print(url_parse,invalids,valids)
                    if url_parse not in invalids:
                        # print('url_parse not in invalids')
                        result = get_parse_href_result(name, hrefs[0], valids, f)
                        invalids = list(set(invalids + result[0]))
                        valids = list(set(valids + result[1]))
                    else:
                        print(f'[无效] {name} -')
                # print(f'{hrefs[0]}')
                else:  # 包含#
                    content = name + ','
                    for i in range(len(hrefs)):
                        url_parse = urlparse(hrefs[i]).netloc
                        if url_parse not in invalids:
                            result2 = \
                                get_parse_href_result2(name, hrefs[i], valids, f)
                            nvalids = list(set(invalids + result2[0]))
                            valids = list(set(valids + result2[1]))
                            content += result2[2]
                    else:
                        print(f'[无效] {name} -')
                    # print(f'{hrefs[i]}')
                    if content[:-1] != name:
                        f.write(content[:-1] + '\n')
            else:
                if line[-7:] == '#genre#':
                    f.write('\n' + line + '\n')
                else:
                    f.write(line + '\n')
        f.close()
        print(f'\n&#127514;效集合√:\n{invalids}')
        print(f'\n&#127542;效集合X:\n{valids}')


def local_live_check():
    filename = '/kaggle/working/live_local.txt'
    path = os.path.abspath(filename)
    print(path)
    dir, file = os.path.split(path)
    # dir,file = os.path.split(file_path)
    # print(dir,file)“
    # basename=os.path.basename(filename)
    files = os.path.splitext(file)
    newfile = os.path.join(dir, files[0] + '_ttd' + files[1])
    print(newfile)
    if not os.path.isfile(newfile):
        f = open(newfile, 'w')
        f.close()
    # print(os.path.isfile(newfile))
    lives_data = get_lives_data(filename)
    # print(lives_data)
    test_url(newfile, lives_data)


if __name__ == '__main__':
    local_live_check()