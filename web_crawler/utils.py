from urllib.parse import urlparse


def add_domain(allowed_domains, url):
    domain = urlparse(url).netloc
    if domain not in allowed_domains:
        allowed_domains.append(domain)


def url_handler(url_list, sub_protocol, sub_domain, start_domain, crawled_urls, resp_url):
    for url in set(url_list):
        if 'javascript:' not in url and url.strip() != '#':
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

            if start_domain in url:
                if not url.startswith('http'):
                    url = sub_protocol + ':' + url
                if url not in crawled_urls:
                    crawled_urls.add(url)
                    yield url

# yield Request(url, priority=priority, callback=kwargs['callback'])
