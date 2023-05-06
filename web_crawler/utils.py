import os.path
from urllib.parse import urlparse
import time
from datetime import datetime


import re

email_regex = r'mailto:[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
from proj_path import path_

root_path = path_ + '/uploads'

# email_sets = set()


def add_domain(allowed_domains, url):
    domain = urlparse(url).netloc
    if domain not in allowed_domains:
        allowed_domains.append(domain)


def getCurrentTime():
    # 获取当前的时间戳
    timestamp = time.time()

    # 将时间戳转换为本地时间
    local_time = datetime.fromtimestamp(timestamp)

    # 按照指定的格式输出时间
    return local_time.strftime("%Y-%m-%d %H:%M:%S")


def getCurrentTimes():
    # 获取当前的时间戳
    timestamp = time.time()

    # 将时间戳转换为本地时间
    local_time = datetime.fromtimestamp(timestamp)

    # 按照指定的格式输出时间
    return local_time.strftime("%Y-%m-%d-%H%M%S")


def url_handler(url_list, sub_protocol, sub_domain, start_domain, crawled_urls, resp_url, root_u):
    for url in set(url_list):
        if 'javascript:' not in url and url.strip() != '#':
            # print('-------->', resp_url)
            if '../' in url:
                print(url, '------>', resp_url)
                count = url.count('../')
                for _ in range(count):
                    index = resp_url.rfind('/')
                    if index != -1:
                        resp_url = resp_url[0:index]
                url = url.replace('../', '')
            if len(urlparse(url).netloc) == 0 and url.startswith('/'):
                url = sub_protocol + '://' + sub_domain + url
            elif len(urlparse(url).netloc) == 0:
                url = sub_protocol + '://' + resp_url + '/' + url
                # print('-------->',resp_url)
                # url = resp_url + '/' + url

            if start_domain in url:
                if not url.startswith('http'):
                    url = sub_protocol + ':' + url

                if url not in crawled_urls:
                    crawled_urls.add(url)
                    result = re.search(email_regex, url)
                    print('result： ------>', result)
                    if result:
                        print(result)
                        email_handler(root_path + '/' + root_u, result.group().split(':')[-1])
                    else:
                        yield url


def email_handler(p, emails):
    file = os.path.join(p, 'email.txt')
    with open(file, 'a', encoding='utf-8') as f:
        f.writelines(emails + '\n')



def is_url(s):
    try:
        result = urlparse(s)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
