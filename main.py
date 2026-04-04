import httpx
import threading

def get_ip_by_ipin(client: httpx.Client) -> None:
    """通过 ipin.io 提供的接口获取 IP address"""
    url = httpx.URL("https://ipin.io/_inquiry/v2/get_client_ip")
    r = client.get(url)
    print(f'IPIN: {r.json().get("ip")}')

def get_ip_by_httpbin(client: httpx.Client) -> None:
    """通过 httpbin.org 提供的接口获取 IP address"""
    url = httpx.URL("https://httpbin.org/ip")
    r = client.get(url)
    print(f'HTTPBin: {r.json().get("origin")}')

def get_ip_by_whatismyip(client: httpx.Client) -> None:
    """通过 whatismyip.com 提供的接口获取 IP address"""
    url = httpx.URL("https://api.whatismyip.com/hp.php")

    # headers 是必要的
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
    print(f'WhatISMyIP: {r.json().get("ip")}')

def main():
    with httpx.Client() as client:
        # 创建线程
        t1 = threading.Thread(target=get_ip_by_httpbin, args=(client,))
        t2 = threading.Thread(target=get_ip_by_whatismyip, args=(client,))
        t3 = threading.Thread(target=get_ip_by_ipin, args=(client,))

        # 启动线程
        t1.start()
        t2.start()
        t3.start()

        # 主线程等待所有线程执行完毕
        t1.join()
        t2.join()
        t3.join()

if __name__ == "__main__":
    main()
