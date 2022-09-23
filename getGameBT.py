import os
import requests
import re
# 汇总torrent连接
torrent_url_list = []
# path
work_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'datafile')


def downHtml(url):
    try:
        r = requests.get(url, headers={'Referer': 'http://ce.ysepan.com/f_ht/ajcx/000ht.html?bbh=1164'})
        r.raise_for_status
        return r.text
    except Exception as e:
        print('---请求异常---\n')
        print(e)


def getTorrentUrl():
    new_url = []
    start_url = 'http://ce.ysepan.com/f_ht/ajcx/ml.aspx?cz=ml_dq&_dlmc=gbtgame&_dlmm='
    text = downHtml(start_url)
    re_list = re.findall("ml_\d+", text)
    for id in re_list:
        temp_url = 'http://ce.ysepan.com/f_ht/ajcx/wj.aspx?cz=dq&jsq=0&mlbh=' + \
            id[3:]+'&wjpx=1&_dlmc=gbtgame&_dlmm='
        new_url.append(temp_url)
    if len(new_url) > 0:
        return new_url
    else:
        print("获取Torrent失败")
        return -1


def parserTorrent(*args):
    def parserHtml(html_text):
        # 理想匹配http*?torrent连接
        list_torrent = re.findall("href=\"(.*?)\"", html_text)
        for url in list_torrent:
            # 判断解析url是否合法
            if '.torrent' in url:
                with open(os.path.join(work_path, 'AllTorrentFile.txt'), 'a', encoding='utf-8') as f:
                    f.write(url+'\n')
                # 添加到汇总list中
                torrent_url_list.append(url)

    for url in args[0]:
        html = downHtml(url)
        parserHtml(html)

    print('torrent链接写入完成...')


def getTorrentFile(*args):
    for url in args[0]:
        r = requests.get(url)
        file_name = url.split('/')[-1]
        with open(os.path.join(work_path, file_name), 'wb') as f:
            f.write(r.content)


def main():
    if os.path.exists(work_path) == False:
        os.mkdir(work_path)
    # 预处理
    url_list = getTorrentUrl()
    # 解析torrent链接
    if url_list != -1:
        print('torrent链接写入中...')
        parserTorrent(url_list)
    # 下载torrent文件
    print("下载torrent链接中...")
    print("任务数量：%s" % len(torrent_url_list))
    getTorrentFile(torrent_url_list)
    print("下载完成.")


if __name__ == "__main__":
    main()
