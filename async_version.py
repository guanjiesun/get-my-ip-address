import httpx
import asyncio

LENGTH: int = 10  # LENGTH = max(len(authority) for authority in ['IPIN', 'HTTPBIN', 'WHATISMYIP'])

async def get_ip_by_ipin(async_client: httpx.AsyncClient) -> None:
    """通过 ipin.io 提供的接口获取 IP address"""
    url = httpx.URL("https://ipin.io/_inquiry/v2/get_client_ip")
    r = await async_client.get(url)
    print(f'{"IPIN":<{LENGTH}}: {r.json().get("ip")}')

async def get_ip_by_httpbin(async_client: httpx.AsyncClient) -> None:
    """通过 httpbin.org 提供的接口获取 IP address"""
    url = httpx.URL("https://httpbin.org/ip")
    r = await async_client.get(url)
    print(f'{"HTTPBIN":<{LENGTH}}: {r.json().get("origin")}')

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
    print(f'{"WHATISMYIP":<{LENGTH}}: {r.json().get("ip")}')

async def main():
    async with httpx.AsyncClient() as async_client:
        # gather 会自动将协程（Coroutine）封装成任务并并发运行
        # 它会等待所有传入的协程全部完成后才继续向下执行
        await asyncio.gather(
            get_ip_by_ipin(async_client),
            get_ip_by_httpbin(async_client),
            get_ip_by_whatismyip(async_client),
        )

if __name__ == "__main__":
    asyncio.run(main())
