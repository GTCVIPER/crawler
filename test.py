import re
from urllib.parse import urlparse

html = '''
<img id=2 src="http://www.example.com/images/logo.png">

<link class='dd' href="/images/logo.png">

<a href="/Correcruit/index.html">企业招聘信息</a>

https://openday.tjcu.edu.cn/#01
file:///D:/pythonProject3/web_crawler/uploads/xcv/tjcu.edu.cn/zs.tjcu.edu.cn/index.htm
https://openday.tjcu.edu.cn

<a id=3 href="images/logo.png">
<a href = '../../../../../../../images/logo.png'>
<script src="images/logo.png">
<script src="//www.example.com/images/logo.png">

<script src=         "//www.example.com/images/logo.png">

<script src =         '//www.example.com/images/logo.png'>
'''
pattern = r'src\s*=\s*[\'"](\S+)[\'"]'
pattern1 = r'href\s*=\s*[\'"](.*?)[\'"]'
base_url = 'D:/root_path'
url_path_ = 'www.example.com/foo/GTC'
subdomain = 'www.example.com'
start_domain = 'example.com'

def conc(html):
    def replace(match):
        # global url_path_1
        global url_path_
        url_path_1 = ''
        url = match.group(1)
        print(url, '--<')
        if '../' in url:
            # print(a_url, '------>', resp_url)
            count = url.count('../')
            for _ in range(count):
                index = url_path_.rfind('/')
                if index != -1:
                    url_path_ = url_path_[0:index]
            url = url.replace('../', '')
        if len(urlparse(url).netloc) == 0 and url.startswith('/') and start_domain not in url:
            url = base_url + '/' + start_domain + '/' + subdomain + url
        elif len(urlparse(url).netloc) == 0 and start_domain not in url:
            url = base_url + '/' + start_domain + '/' + url_path_ + '/' + url

        if 'http://' in url:
            url = url.replace('http://', '')
        elif 'https://' in url:
            url = url.replace('https://', '')
        if subdomain in url and base_url not in url:
            if url.startswith('//'):
                url = url.replace('//', '/')
            elif not url.startswith('/'):
                url = '/' + url
            url = base_url + '/' + start_domain + url
        return f'src="{url}"'

    def replace1(match):
        # global url_path_1
        global url_path_
        url_path_1 = ''
        url = match.group(1)
        print(url, '--<')
        if '../' in url:
            # print(a_url, '------>', resp_url)
            count = url.count('../')
            for _ in range(count):
                index = url_path_.rfind('/')
                if index != -1:
                    url_path_ = url_path_[0:index]
            url = url.replace('../', '')
        if len(urlparse(url).netloc) == 0 and url.startswith('/') and start_domain not in url:
            url = base_url + '/' + start_domain + '/' + subdomain + url
        elif len(urlparse(url).netloc) == 0 and start_domain not in url:
            url = base_url + '/' + start_domain + '/' + url_path_ + '/' + url

        if 'http://' in url:
            url = url.replace('http://', '')
        elif 'https://' in url:
            url = url.replace('https://', '')
        if subdomain in url and base_url not in url:
            if url.startswith('//'):
                url = url.replace('//', '/')
            elif not url.startswith('/'):
                url = '/' + url
            url = base_url + '/' + start_domain + url
        return f'href="{url}"'

    html = re.sub(pattern, replace, html)
    html = re.sub(pattern1, replace1, html)

    print(html)

conc(html)