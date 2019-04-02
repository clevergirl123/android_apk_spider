# coding=utf-8
import requests
import re
import threading
from urllib.request import urlretrieve, quote
from bs4 import BeautifulSoup


def parser_apks(count=0, family="123"):
    _root_url = "http://zhushou.360.cn/"
    _search_url = "http://zhushou.360.cn/search/index/?kw=" + family + "&page="
    # 应用市场主页网址
    res_parser = {}
    page_num = 1  # 设置爬取的页面，从第一页开始爬取，第一页爬完爬取第二页，以此类推
    print("parser_apks count : ", count)
    while count:
        # 获取排行榜页面的网页内容
        wbdata = requests.get(_search_url + str(page_num)).text
        print(family + " 开始爬取第" + str(page_num) + "页")
        # 解析页面内容获取 应用下载的 界面连接
        soup = BeautifulSoup(wbdata, "html.parser")
        links = soup.body.find_all("a", class_=re.compile("dbtn .+ normal"))
        for link in links:
            # print(str(count) + " : ", link)
            detail_link = link["href"]
            download_url = detail_link
            package_name = detail_link.split("/")[-1]
            # 解析后会有重复的结果，下面通过判断去重
            if download_url not in res_parser.values():
                res_parser[package_name] = download_url
                count -= 1
            if count == 0:
                break
        if count > 0:
            page_num += 1
        if len(links) == 0:
            break
    print("爬取 " + family + " apk数量为: " + str(len(res_parser)))
    return res_parser


def craw_apks(cn_name, en_name, count=1):
    print("craw_apk count : ", count)
    res_dic = parser_apks(count=count, family=quote(cn_name, encoding="utf-8"))
    save_path = "../" + en_name + "/"
    csv_path = "./" + en_name + ".csv"
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("package_name,family\n")
    for apk in res_dic.keys():
        urlretrieve(res_dic[apk], save_path + apk)
        with open(csv_path, 'a+', encoding='utf-8') as f:
            f.write(apk + "," + en_name + '\n')
        print(apk + " 下载完成")


if __name__ == "__main__":
    name_dict = {
        "运动": "sports",
        "购物": "shopping",
        "拍照": "photo",
        # "": "",
        # "": "",
        # "浏览器": "browser",
        # "时钟": "clock",
        # "文档": "document",
        # "游戏": "games",
        # "邮件": "mail",
        # "音乐": "music",
        # "新闻": "news",
        # "小说": "novel",
        # "视频": "video",
        # "天气": "weather",
    }
    for key in name_dict.keys():
        t = threading.Thread(target=craw_apks, args=(key, name_dict[key], 512))
        t.start()
        print("key : " + key +" ,开始多线程……")
        # craw_apks(cn_name=key, en_name=name_dict[key], count=512)
