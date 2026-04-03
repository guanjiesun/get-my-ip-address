import httpx
import asyncio

async def get_ip_by_httpbin(async_client: httpx.AsyncClient) -> None:
    """通过 httpbin.org 提供的接口获取 IP address"""
    url = httpx.URL("https://httpbin.org/ip")
    r = await async_client.get(url)
    print(f'HTTPBin: {r.json().get("origin")}')

async def get_ip_by_whatismyip(async_client: httpx.AsyncClient) -> None:
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
    r = await async_client.post(url, headers=headers)
    print(f'WhatISMyIP: {r.json().get("ip")}')

async def main():
    async with httpx.AsyncClient() as async_client:
        # 创建任务（task被创建之后就会启动，这一点和线程不同）
        task1 = asyncio.create_task(get_ip_by_whatismyip(async_client))
        task2 = asyncio.create_task(get_ip_by_httpbin(async_client))

        # 主线程等待所有任务执行完毕
        await task1
        await task2

if __name__ == "__main__":
    asyncio.run(main())
