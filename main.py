import httpx
import threading
from lxml import html

LENGTH: int = 10  # LENGTH = max(len(authority) for authority in ['IPIN', 'HTTPBIN', 'WHATISMYIP', 'IPCN'])

def get_ip_by_ipcn(client: httpx.Client) -> None:
    """通过 ip.cn 提供的接口获取 IP address"""
    url = httpx.URL("https://ip.cn")

    # headers 是必要的（copyed from Chrome DevTools）
    headers = {
        "Host": "ip.cn",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    # 向请求发送 GET 请求，并解析响应中的 HTML 来提取 ticket
    r = client.get(url, headers=headers)
    tree = html.fromstring(r.text)
    script = tree.xpath('//script')[0]
    ticket = script.text.strip().split('=')[1].strip(' ;"')

    # 使用 ticket 获取 IP address
    url = httpx.URL(f"https://my.ip.cn/json/?ticket={ticket}")
    r = client.get(url)
    print(f'{"IPCN":<{LENGTH}}: {r.json().get("data").get("ip")}', flush=True)

def get_ip_by_ipin(client: httpx.Client) -> None:
    """通过 ipin.io 提供的接口获取 IP address"""
    url = httpx.URL("https://ipin.io/_inquiry/v2/get_client_ip")
    r = client.get(url)
    print(f'{"IPIN":<{LENGTH}}: {r.json().get("ip")}', flush=True)

def get_ip_by_httpbin(client: httpx.Client) -> None:
    """通过 httpbin.org 提供的接口获取 IP address"""
    url = httpx.URL("https://httpbin.org/ip")
    r = client.get(url)
    print(f'{"HTTPBIN":<{LENGTH}}: {r.json().get("origin")}', flush=True)

def get_ip_by_whatismyip(client: httpx.Client) -> None:
    """通过 whatismyip.com 提供的接口获取 IP address"""
    url = httpx.URL("https://api.whatismyip.com/hp.php")

    # headers 是必要的（copyed from Chrome DevTools）
    headers = {
        "Host": "api.whatismyip.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://www.whatismyip.com/",
        "Origin": "https://www.whatismyip.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=4",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }
    r = client.post(url, headers=headers)
    print(f'{"WhatISMyIP":<{LENGTH}}: {r.json().get("ip")}', flush=True)

def main():
    with httpx.Client() as client:
        # 创建线程
        t1 = threading.Thread(target=get_ip_by_httpbin, args=(client,))
        t2 = threading.Thread(target=get_ip_by_whatismyip, args=(client,))
        t3 = threading.Thread(target=get_ip_by_ipin, args=(client,))
        t4 = threading.Thread(target=get_ip_by_ipcn, args=(client,))

        # 启动线程
        t1.start()
        t2.start()
        t3.start()
        t4.start()

        # 主线程等待所有线程执行完毕
        t1.join()
        t2.join()
        t3.join()
        t4.join()

if __name__ == "__main__":
    main()
