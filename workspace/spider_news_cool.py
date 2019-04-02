# coding=utf-8
import csv
import requests
import re
import time
import random
from urllib.parse import urljoin
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

USER_AGENTS = (
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7_0; en-US) AppleWebKit/534.21 (KHTML, like Gecko) Chrome/11.0.678.0 Safari/534.21",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:0.9.2) Gecko/20020508 Netscape6/6.1",
    "Mozilla/5.0 (X11;U; Linux i686; en-GB; rv:1.9.1) Gecko/20090624 Ubuntu/9.04 (jaunty) Firefox/3.5",
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
    'Opera/9.80 (X11; U; Linux i686; en-US; rv:1.9.2.3) Presto/2.2.15 Version/10.10'
)


# 获取HTML页面，这个才是好的MDZZ！
def getHtml(url):
    html = urlopen(url).read()
    return html.decode("utf-8")


def parser_apks_page(page_num=1):
    _root_url = "https://www.coolapk.com/"
    _search_url = "https://www.coolapk.com/apk/tag/%E6%96%B0%E9%97%BB?p=" + str(page_num)
    res_parser = {}
    headers = {"User-Agent": USER_AGENTS[random.randint(0, len(USER_AGENTS) - 1)]}
    wbdata = requests.get(_search_url, headers=headers).text
    print(_search_url)
    # print(wbdata)
    soup = BeautifulSoup(wbdata, "html.parser")
    link1 = soup.body.find(attrs={"class": "app_list_left"})
    links = link1.find_all("a", href=re.compile("/apk/.+\..+"))

    for link in links:
        detail_link = urljoin(_root_url, str(link["href"]))
        package_name = detail_link.split("/")[-1] + ".apk"
        time.sleep(3)
        try:
            download_page = requests.get(detail_link).text
            pattern_1 = re.compile("https.+&from=click")
            download_url = re.findall(pattern_1, download_page)[0]
            print("package_name: " + package_name)
            res_parser[package_name] = download_url
        except:
            print("Error!!! Can't find " + package_name)
            continue
    return res_parser


def parser_apks(family="news", count=0):
    _root_url = "https://www.coolapk.com/"
    _search_url = "https://www.coolapk.com/apk/tag/%E6%96%B0%E9%97%BB?p="
    # 应用市场主页网址
    res_parser = {}
    page_num = 1  # 设置爬取的页面，从第一页开始爬取，第一页爬完爬取第二页，以此类推
    # print(_search_url + str(page_num))
    # print("parser_apks count : ", count)
    num = 0
    while count and page_num < 10:
        # 获取排行榜页面的网页内容
        # wbdata = getHtml(_search_url + str(page_num))
        headers = {"User-Agent": USER_AGENTS[random.randint(0, len(USER_AGENTS) - 1)]}
        wbdata = requests.get(_search_url + str(page_num), headers=headers).text
        print(_search_url + str(page_num))
        # print(wbdata)
        print("开始爬取第" + str(page_num) + "页")
        # show_dict(res_parser)
        # 解析页面内容获取 应用下载的 界面连接
        soup = BeautifulSoup(wbdata, "html.parser")
        link1 = soup.body.find(attrs={"class": "app_list_left"})
        links = link1.find_all("a", href=re.compile("/apk/.+\..+"))
        for link in links:
            num += 1
            # print(str(count) + " : ", link)
            # detail_link = urljoin(_root_url, str(link["href"]))
            detail_link = urljoin(_root_url, str(link["href"]))
            package_name = detail_link.split("/")[-1] + ".apk"
            try:
                download_page = requests.get(detail_link).text
                pattern_1 = re.compile("https.+&from=click")
                download_url = re.findall(pattern_1, download_page)[0]
                # print("download_url : " + download_url)
                # print("detail_link : " + detail_link)
                print(str(num) + "  package_name: " + package_name)
                # 解析后会有重复的结果，下面通过判断去重
                if package_name not in res_parser.keys():
                    res_parser[package_name] = download_url
                    count -= 1
                if count == 0:
                    break
            except Exception as e:
                print(str(e))
                continue
        page_num += 1
        time.sleep(5)
        print("---------------------当前apk数量为: " + str(len(res_parser)))
        # break
    print("爬取 " + family + " apk数量为: " + str(len(res_parser)))
    return res_parser


def craw_apks(en_name, count=1):
    print("craw_apk count : ", count)
    res_dic = parser_apks(en_name, count=count)
    # return
    save_path = "../" + en_name + "_new/"
    csv_path = "./" + en_name + "_new.csv"
    for apk in res_dic.keys():
        if down_apk(res_dic[apk], save_path + apk):
            with open(csv_path, 'a+', encoding='utf-8') as f:
                f.write(apk + "," + en_name + '\n')
            print(apk + " 下载完成")
        time.sleep(4)
        print(apk + " 下载完成")


def down_apk(url, path):
    try:
        headers = {"User-Agent": USER_AGENTS[random.randint(0, len(USER_AGENTS) - 1)]}
        req = Request(url, headers=headers)
        data = urlopen(req).read()
        with open(path, 'wb') as f:
            f.write(data)
            f.close()
            return True
    except Exception as e:
        print(str(e))
        return False


def craw_apks_page(en_name, count=1):
    page_num = 1
    save_path = "../" + en_name + "_new/"
    csv_path = "./" + en_name + "_new.csv"
    with open(csv_path, 'a+', encoding='utf-8') as f:
        f.write("--------------- " + en_name + " ----------------" + '\n')
    while page_num < 69:
        res_dic = parser_apks_page(page_num)
        for apk in res_dic.keys():
            # urlretrieve(res_dic[apk], save_path + apk)
            if down_apk(res_dic[apk], save_path + apk):
                with open(csv_path, 'a+', encoding='utf-8') as f:
                    f.write(apk + "," + en_name + '\n')
                print(apk + " 下载完成")
            time.sleep(4)
        count -= len(res_dic)
        print("第 " + str(page_num) + " 已下载，还差 " + str(count) + " 个")
        if count <= 0:
            break
        page_num += 1


def show_dict(dictionary):
    for item in dictionary.keys():
        print(item)


if __name__ == "__main__":
    craw_apks_page(en_name="news", count=1152)
