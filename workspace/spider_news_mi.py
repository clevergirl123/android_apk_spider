# coding=utf-8
import csv
import requests
import re
import threading
from urllib.parse import urljoin
from urllib.request import urlretrieve, quote
from bs4 import BeautifulSoup


# 为防止重复下载
def read_csv(csv_path):
    csv_file = csv.reader(open(csv_path, "r"))
    exist_apk = {}
    for apk in csv_file:
        exist_apk[simplify_apk(apk[0])] = True
    return exist_apk


def parser_apks(family="news", count=0):
    _root_url = "http://app.mi.com"
    # _category_dict = {"news":"11", "novel":"7"}
    # _search_url = "http://app.mi.com/category/" + _category_dict[family] + "#page="
    _search_url = "http://app.mi.com/category/11#page="
    # 应用市场主页网址
    res_parser = read_csv("./" + family +".csv")
    page_num = 0  # 设置爬取的页面，从第一页开始爬取，第一页爬完爬取第二页，以此类推
    # print(_search_url + str(page_num))
    # print("parser_apks count : ", count)
    while count:
        # 获取排行榜页面的网页内容
        # wbdata = requests.get("http://app.mi.com/category/11").text
        wbdata = requests.get(_search_url + str(page_num)).text
        # print(wbdata)
        print(family + " 开始爬取第" + str(page_num) + "页,当前apk数量为：" + str(len(res_parser)))
        # 解析页面内容获取 应用下载的 界面连接
        soup = BeautifulSoup(wbdata, "lxml")
        links = soup.body.find_all("a", href=re.compile("/details\?id"), class_="", alt="")
        # links = soup.body.find_all("a", href=re.compile("/details\?id"), class_="", alt="")
        for link in links:
            # print(str(count) + " : ", link)
            detail_link = urljoin(_root_url, str(link["href"]))
            package_name = detail_link.split("=")[1] + ".apk"
            download_page = requests.get(detail_link).text
            soup1 = BeautifulSoup(download_page, "html.parser")
            download_link = soup1.body.find(class_="download")["href"]
            download_url = urljoin(_root_url, str(download_link))
            # 解析后会有重复的结果，下面通过判断去重
            if download_url not in res_parser.values():
                # if package_name not in res_parser.keys():
                res_parser[package_name] = download_url
                count -= 1
            if count == 0:
                break
        if count > 0:
            page_num += 1
        if page_num > 60:
            break
    print("爬取 " + family + " apk数量为: " + str(len(res_parser)))
    return res_parser


def craw_apks(en_name, count=1):
    print("craw_apk count : ", count)
    res_dic = parser_apks(en_name, count=count)
    save_path = "../" + en_name + "_new/"
    csv_path = "./" + en_name + "_new.csv"
    for apk in res_dic.keys():
        # if not isinstance(res_dic[apk], bool):
        urlretrieve(res_dic[apk], save_path + apk)
        with open(csv_path, 'a+', encoding='utf-8') as f:
            f.write(apk + "," + en_name + '\n')
        print(apk + " 下载完成")


# 去除版本号，保留包名
def simplify_apk(apk_name):
    apk_name = apk_name[:-4]
    res_name = ".apk"
    if len(apk_name.split(".")) > 1:
        pk_list = apk_name.split("_")
        flag = False
        for i in pk_list[::-1]:
            if flag:
                res_name = i + "_" + res_name
                continue
            if not i.isdigit():
                flag = True
                res_name = i + res_name
    else:
        res_name = apk_name + res_name
    return res_name

if __name__ == "__main__":
    labels = ["news", "novel"]
    for label in labels:
        t = threading.Thread(target=craw_apks, args=(label, 1152))
        t.start()
    # craw_apks(en_name="news", count=1152)
