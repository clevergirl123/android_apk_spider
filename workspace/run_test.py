# coding=utf-8
import requests
import re
from urllib.parse import urljoin
from urllib.request import urlretrieve
from bs4 import BeautifulSoup

count = 9
_root_url = "https://www.coolapk.com/"
# 应用市场主页网址
res_parser = {}
page_num = 1
# while count:
    # 获取排行榜页面的网页内容
wbdata = requests.get("https://www.coolapk.com/apk/tag/%E6%96%B0%E9%97%BB?p=" + str(page_num)).text
print("开始爬取第" + str(page_num) + "页")
# print(type(wbdata))
# 解析页面内容获取 应用下载的 界面连接
soup = BeautifulSoup(wbdata, "html.parser")
link1 = soup.body.find(attrs={"class":"app_list_left"})
links = link1.find_all("a", href=re.compile("/apk/.+\..+"))
print(len(links))
for link in links:
    # print("link : " + str(link))
    detail_link = urljoin(_root_url, str(link["href"]))
    package_name = detail_link.split("/")[-1] + ".apk"
    download_page = requests.get(detail_link).text
    pattern_1 = re.compile("https.+&from=click")
    download_url = re.findall(pattern_1, download_page)[0]
    print("download_url : " + download_url)
    # print("detail_link : " + detail_link + "\npackage_name: " + package_name)
    # 解析后会有重复的结果，下面通过判断去重
    if package_name not in res_parser.keys():
        res_parser[package_name] = download_url
        count -= 1
    if count == 0:
        break
    break
if count > 0:
    page_num += 1
print("爬取apk数量为: " + str(len(res_parser)))

# import os, csv

# # 为防止重复下载
# def read_csv(csv_path):
#     csv_file = csv.reader(open(csv_path, "r"))
#     exist_apk = {}
#     for stu in csv_file:
#         exist_apk[stu[0]] = True
#     return exist_apk

# # 去除版本号，保留包名
# def simplify_apk(apk_name):
#     apk_name = apk_name[:-4]
#     res_name = ".apk"
#     if len(apk_name.split(".")) > 1:
#         pk_list = apk_name.split("_")
#         flag = False
#         for i in pk_list[::-1]:
#             if flag:
#                 res_name = i + "_" + res_name
#                 continue
#             if not i.isdigit():
#                 flag = True
#                 res_name = i + res_name
#     else:
#         res_name = apk_name + res_name
#     return res_name

# name = ['com.qihoo360.news_shellMetroExpress_15_12.apk', 
#     'com.xmrb_113.apk', 'com.link_15_shop.client_29.apk', 
#     '3935_f8b6f4d9-27a4-4271-bbf1-5c13ae8f293f.apk']
# for n in name:
#     print(simplify_apk(n))