import axios from 'axios'

/*通过 ipin.io 获取 IP*/
async function byIPIN() {
    const url = "https://ipin.io/_inquiry/v2/get_client_ip";
    try {
        const r = await axios.get(url, {timeout: 5000});
        console.log(`IPIN   : ${r.data.ip}`);
    } catch (err) {
        console.error("IPIN 请求失败:", err.message);
    }
}

/*通过 httpbin.org 获取 IP*/
async function byHTTPBin() {
    const url = "https://httpbin.org/ip";
    try {
        const r = await axios.get(url, {timeout: 5000});
        console.log(`HTTPBin: ${r.data.origin}`);
    } catch (err) {
        console.error("HTTPBin 请求失败:", err.message);
    }
}

async function main() {
    // Promise.all 会同时启动两个任务，并等待它们全部完成
    // 类似于 Python 中的 asyncio.gather(*tasks) 或等待多个 tasks
    await Promise.all([byIPIN(), byHTTPBin()]);
}

await main();

