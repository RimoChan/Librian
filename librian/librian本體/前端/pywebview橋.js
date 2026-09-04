(function () {
    'use strict';

    if (new URLSearchParams(window.location.search).get('_librian_webview') !== '1') {
        return;
    }
    if (window.山彥 && window.山彥.傳輸 === 'promise') {
        return;
    }

    var api就緒 = new Promise(function (resolve) {
        if (window.pywebview && window.pywebview.api) {
            resolve(window.pywebview.api);
            return;
        }
        window.addEventListener('pywebviewready', function () {
            resolve(window.pywebview.api);
        }, { once: true });
    });
    var 調用隊列 = Promise.resolve();
    function 導航(網址) {
        var 目標 = new URL(網址, window.location.href);
        目標.searchParams.set('_librian_webview', '1');
        window.location.href = 目標.href;
    }
    function 退出() {
        var 目標 = new URL(window.location.href);
        目標.searchParams.set('_librian_exit', '1');
        window.location.href = 目標.href;
    }
    async function 忽略錯誤(結果) {
        try {
            await 結果;
        } catch (錯誤) {}
    }
    var 完成操作 = {
        回標題: 導航,
        開始: 導航,
        讀檔畫面: 導航,
        從劇本開始: 導航
    };
    async function 執行調用(上一次調用, 方法, 參數) {
        await 上一次調用;
        var api = await api就緒;
        var 返回值 = await api[方法].apply(api, 參數);
        if (完成操作[方法]) {
            return 完成操作[方法](返回值);
        }
        return 返回值;
    }

    window.山彥 = new Proxy({ 傳輸: 'promise', 退出: 退出 }, {
        get: function (目標, 方法) {
            if (方法 in 目標) {
                return 目標[方法];
            }
            return async function () {
                var 參數 = Array.prototype.slice.call(arguments);
                var 結果 = 執行調用(調用隊列, 方法, 參數);
                調用隊列 = 忽略錯誤(結果);
                return await 結果;
            };
        }
    });
})();
