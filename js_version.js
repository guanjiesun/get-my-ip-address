/*通过 ipin.io 获取 IP*/
async function getIpByIpIn() {
    const url = "https://ipin.io/_inquiry/v2/get_client_ip";
    try {
        const response = await fetch(url);
        const data = await response.json();
        console.log(`IPIN: ${data.ip}`);
    } catch (err) {
        console.error("IPIN 请求失败:", err.message);
    }
}

/*通过 httpbin.org 获取 IP*/
async function getIpByHttpBin() {
    const url = "https://httpbin.org/ip";
    try {
        const response = await fetch(url);
        const data = await response.json();
        console.log(`HTTPBin: ${data.origin}`);
    } catch (err) {
        console.error("HTTPBin 请求失败:", err.message);
    }
}

async function main() {
    // Promise.all 会同时启动两个任务，并等待它们全部完成
    // 类似于 Python 中的 asyncio.gather(*tasks) 或等待多个 tasks
    await Promise.all([getIpByIpIn(), getIpByHttpBin()]);
}

main();

