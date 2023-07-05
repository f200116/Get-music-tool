import os.path
import re
import sys
import time
from urllib import parse

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}


def utf8_to_url(s: str):
    # 获取一个utf-8，返回url编码
    result = parse.quote(s)
    result1 = ''
    for each in result:
        if each == '%':
            result1 += '_'
        else:
            result1 += each
    return result1


def main(name: str):
    url = f'https://www.hifini.com/search-{utf8_to_url(name)}.htm'  # 汉字转为url编码格式
    response = session.get(url=url, headers=headers)
    # print(session)
    # response = requests.get(url=url, headers=headers)

    result = re.findall(r'<a href="thread-(\d+).*?>(.*?)</a>', response.text)
    # print(result)
    all_list = []
    for each in result:
        id_ = each[0]
        s = each[-1].split('</em>')
        s = ''.join(s)
        s = s.split('<em>')
        name_ = ''.join(s)
        info = {'id_': id_, 'name_': name_}
        # print(info)
        all_list.append(info)
    return all_list


def get_music_url(id_):
    url = f"https://www.hifini.com/thread-{id_}.htm"
    # response = requests.get(url=url, headers=headers)
    response = session.get(url=url, headers=headers)
    # print(session)
    result = re.findall(r"url: 'get_music.php\?key=(.*?)'", response.text)
    # print(result)
    if len(result) == 0:
        result = re.findall(r"url: '(.*?)'", response.text)
        if len(result) == 0:
            return None
        else:
            return result[0]

    key = result[0]
    music_url = f'https://www.hifini.com/get_music.php?key={key}'
    return music_url


def download_music(url, name):
    response = session.get(url=url, headers=headers)
    # print(session)
    # response = requests.get(url=url, headers=headers)
    print(response.headers)
    with open(f'music\\{name}.mp3', mode='wb') as fw:
        fw.write(response.content)


if __name__ == '__main__':
    print('欢迎使用小程序，本应用未保存任何资源，所有资源均为网络查找！\n若想退出，请在任何需要输入的界面输入q')
    print('\n正在初始化...')
    # 创建会话
    try:
        session = requests.session()
        # print(session)
        session.get(url='https://www.hifini.com/', headers=headers)
        # print(session)
    except:
        print('初始化失败！即将退出！')
        time.sleep(3)
        sys.exit(1)
    if not os.path.exists('music\\'):
        os.mkdir('music\\')
    flag = True
    try:
        while flag:

            name = input('\n请输入歌曲名或作者名：')
            if name.lower() == 'q':
                break
            all_info = main(name)
            if len(all_info) == 0:
                print(f'未查询到此音乐：{name}')
                continue
            i = 1
            for each in all_info:
                print(f'{i}. {each["name_"]}')
                i += 1
            id__ = input('请输入序号：')
            if id__.lower() == 'q':
                break
            else:
                if not id__.isdigit():
                    print('你输入的应该为纯数字或“q”')
                    continue
                id__ = int(id__)
                if id__ > len(all_info) or id__ < 1:
                    print('你应该输入准确的序号')
                    continue
            id_, name_ = all_info[id__ - 1]['id_'], all_info[id__ - 1]['name_']
            name_ = name_.split('[')[0]
            music_url = get_music_url(id_=id_)
            if not music_url:
                print('暂未收录此音乐。')
                continue
            url = music_url
            # url = session.get(url=music_url).url
            # print(session)
            # url = requests.get(url=music_url).url
            print('歌曲地址为：', url)
            down = input('是否下载此音乐(Y/N)：')
            if down.lower() == 'y':
                download_music(url=url, name=name_)

                print(f"已下载此音乐：{name_}")
    except BaseException as err:
        print(f'异常退出，原因为：{err}\n若无法解决，请联系作者！')
    print('欢迎使用，正在退出此程序...')
    time.sleep(3)
