const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const bridgePath = path.join(__dirname, '../librian/librian本體/前端/pywebview橋.js');
const bridge = fs.readFileSync(bridgePath, 'utf8');

function loadBridge(search, api) {
    const window = {
        location: { search, href: `file:///title.html${search}` },
        pywebview: { api },
        addEventListener() {},
    };
    vm.runInNewContext(bridge, { window, URL, URLSearchParams, Promise, Proxy, Array });
    return window;
}

async function main() {
    const calls = [];
    const api = {
        slow() {
            calls.push('slow:start');
            return new Promise(resolve => setTimeout(() => {
                calls.push('slow:end');
                resolve();
            }, 10));
        },
        fail() {
            calls.push('fail');
            return Promise.reject(new Error('expected'));
        },
        fast() {
            calls.push('fast');
            return Promise.resolve();
        },
    };
    const window = loadBridge('?_librian_webview=1', api);
    const 山彥 = window.山彥;

    const results = await Promise.allSettled([山彥.slow(), 山彥.fail(), 山彥.fast()]);

    assert.deepStrictEqual(calls, ['slow:start', 'slow:end', 'fail', 'fast']);
    assert.deepStrictEqual(results.map(result => result.status), ['fulfilled', 'rejected', 'fulfilled']);
    for (const method of ['回標題', '開始', '讀檔畫面', '從劇本開始']) {
        api[method] = () => Promise.resolve('file:///game/adv.html?入口=讀檔');
        await 山彥[method]();
        assert.strictEqual(window.location.href, 'file:///game/adv.html?%E5%85%A5%E5%8F%A3=%E8%AE%80%E6%AA%94&_librian_webview=1');
    }
    await 山彥.退出();
    assert.strictEqual(window.location.href, 'file:///game/adv.html?%E5%85%A5%E5%8F%A3=%E8%AE%80%E6%AA%94&_librian_webview=1&_librian_exit=1');
    assert.strictEqual(loadBridge('', api).山彥, undefined);
    console.log('pywebview bridge tests passed');
}

main().catch(error => {
    console.error(error);
    process.exitCode = 1;
});
