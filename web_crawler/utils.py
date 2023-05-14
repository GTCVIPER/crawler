import os.path
from urllib.parse import urlparse
import time
from datetime import datetime
import tldextract
from urllib.parse import parse_qsl
import re

email_regex = r'mailto:[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
src_pattern = r'src\s*=\s*[\'"](\S+)[\'"]'
href_pattern = r'href\s*=\s*[\'"](.*?)[\'"]'

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


def replace_TEXT(texts, url_path_, start_domain, sub_domain, root_u):
    def replace_SRC(match):
        url = match.group(1)
        url = overwriteURL(url, url_path_, start_domain, sub_domain, root_u)
        return f'src="{url}"'

    def replace_HREF(match):
        url = match.group(1)
        url = overwriteURL(url, url_path_, start_domain, sub_domain, root_u)
        return f'href="{url}"'

    texts = re.sub(src_pattern, replace_SRC, texts)
    texts = re.sub(href_pattern, replace_HREF, texts)
    return texts


def overwriteURL(url, url_path_, start_domain, sub_domain, root_u):

    domain_str = tldextract.extract(url).registered_domain
    if 'javascript:' in url:
        return url
    elif domain_str != '' and start_domain !=  domain_str:
        return url
    if '#' in url:
        url = url.rsplit('#')[0]
    if ';' in url:
        url = url.split(';')[0]
    if '../' in url:
        # print(a_url, '------>', resp_url)
        count = url.count('../')
        for _ in range(count):
            index = url_path_.rfind('/')
            if index != -1:
                url_path_ = url_path_[0:index]
        url = url.replace('../', '')
    if len(urlparse(url).netloc) == 0 and url.startswith('/') and start_domain not in url:
        url = root_path + '/' + root_u + '/' + start_domain + '/' + sub_domain + url
    elif len(urlparse(url).netloc) == 0 and start_domain not in url:
        url = root_path + '/' + root_u + '/' + start_domain + '/' + url_path_ + '/' + url

    if 'http://' in url:
        url = url.replace('http://', '')
    elif 'https://' in url:
        url = url.replace('https://', '')
    if start_domain in url and root_path not in url:
        if url.startswith('//'):
            url = url.replace('//', '/')
        elif not url.startswith('/'):
            url = '/' + url
        url = root_path + '/' + root_u + '/' + start_domain + url

    url_params = dict(parse_qsl(urlparse(url).query))
    if '?' in url:
        url = url.rsplit('?')[0]
    if len(url_params) != 0:
        # url = url.rsplit('?')[0]
        # if not url.endswith('/'):
        #     url += '/'
        path_str_ = url.split(start_domain)[-1]
        for key, value in url_params.items():
            if key in ['page', 'file', 'id', 'cat', 'product', 'category', 'blog', 'act', 'action', 'tags',
                       'page_id', 'p']:
                if not url.endswith('/'):
                    url += '/'
                if '.' in path_str_:
                    path_str_ = path_str_.replace('.', '_')
                    url = url.split(url.split(start_domain)[-1])[0] + path_str_
                    url += '/' + key + '/' + value + '.html'
                else:
                    url += key + '/' + value + '.html'

    path_str = url.split(start_domain)[-1]
    if '.' not in path_str:
        if not url.endswith('/'):
            url += '/'
        url += 'index.html'
    # elif url.endswith('htm'):
    #     url = url.replace('htm', 'html')
    return url


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
            if len(urlparse(url).netloc) == 0 and url.startswith('/') and start_domain not in url:
                url = sub_protocol + '://' + sub_domain + url
            elif len(urlparse(url).netloc) == 0 and start_domain not in url:
                url = sub_protocol + '://' + resp_url + '/' + url
                # print('-------->',resp_url)
                # url = resp_url + '/' + url

            if start_domain in url:
                if not url.startswith('http') and url.startswith('//'):
                    url = sub_protocol + ':' + url
                elif not url.startswith('http') and url.startswith('/'):
                    url = sub_protocol + ':/' + url
                elif not url.startswith('http'):
                    url = sub_protocol + '://' + url

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
    if not os.path.exists(p):
        os.makedirs(p)
    file = os.path.join(p, 'email.txt')
    with open(file, 'a', encoding='utf-8') as f:
        f.writelines(emails + '\n')


def is_url(s):
    try:
        result = urlparse(s)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
