# coding=utf-8
import requests
import re
from urllib.parse import urljoin
from urllib.request import urlretrieve
from bs4 import BeautifulSoup


def parser_apks(count=0):
    '''小米应用市场'''

    _root_url = "http://app.mi.com"
    # 应用市场主页网址
    res_parser = {}
    page_num = 1  # 设置爬取的页面，从第一页开始爬取，第一页爬完爬取第二页，以此类推
    print("parser_apks count : ", count)
    while count:
        # 获取排行榜页面的网页内容
        wbdata = requests.get("http://app.mi.com/topList?page=" + str(page_num)).text
        print("开始爬取第" + str(page_num) + "页")
        # 解析页面内容获取 应用下载的 界面连接
        soup = BeautifulSoup(wbdata, "html.parser")
        links = soup.body.contents[5].find_all("a", href=re.compile("/details?"), class_="",
                                               alt="")  # BeautifullSoup的具体用法请百度一下吧。。。
        print("type(links):", type(links))
        for link in links:
            print("link : ", link)
            detail_link = urljoin(_root_url, str(link["href"]))
            package_name = detail_link.split("=")[1]
            # 在下载页面中获取 apk下载的地址
            download_page = requests.get(detail_link).text
            soup1 = BeautifulSoup(download_page, "html.parser")
            download_link = soup1.find(class_="download")["href"]
            download_url = urljoin(_root_url, str(download_link))
            # 解析后会有重复的结果，下面通过判断去重
            if download_url not in res_parser.values():
                res_parser[package_name] = download_url
                count -= 1
            if count == 0:
                break
        if count > 0:
            page_num += 1
    print("爬取apk数量为: " + str(len(res_parser)))
    return res_parser


def craw_apks(count=1, save_path="../test/"):
    print("craw_apk count : ", count)
    res_dic = parser_apks(count)
    for apk in res_dic.keys():
        print("正在下载应用: " + apk)
        urlretrieve(res_dic[apk], save_path + apk + ".apk")
        print("下载完成")


if __name__ == "__main__":
    craw_apks(20)
