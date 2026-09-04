import platform
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from .前端API import 山彥API


橋腳本 = Path(__file__).parent / '前端/pywebview橋.js'


class WebView窗口:
    def __init__(self, webview, url, icon, title, size, storage_path):
        self._webview = webview
        self._url = _本地網址(url)
        self._icon = str(icon) if icon else None
        self._title = title
        self._size = tuple(size)
        self._storage_path = str(storage_path) if storage_path else None
        self._api = None
        self._window = None

    def 綁定(self, 山彥):
        self._api = 山彥API(山彥)

    def 執行js(self, script):
        return self._window.evaluate_js(script)

    def 切換全屏(self):
        return self._window.toggle_fullscreen()

    def 運行(self):
        if self._api is None:
            raise RuntimeError('啓動窗口前必須綁定山彥')

        width, height = self._窗口尺寸()
        self._window = self._webview.create_window(
            title=self._title,
            url=self._url,
            js_api=self._api,
            width=width,
            height=height,
        )
        self._window.events.loaded += self._注入橋
        self._webview.start(
            private_mode=False,
            storage_path=self._storage_path,
            icon=self._icon,
        )

    def _窗口尺寸(self):
        if platform.system() != 'Darwin':
            return self._size

        import AppKit

        內容寬, 內容高 = self._size
        樣式 = (
            AppKit.NSWindowStyleMaskTitled
            | AppKit.NSWindowStyleMaskClosable
            | AppKit.NSWindowStyleMaskMiniaturizable
            | AppKit.NSWindowStyleMaskResizable
        )
        內容矩形 = AppKit.NSMakeRect(0, 0, 內容寬, 內容高)
        外框矩形 = AppKit.NSWindow.frameRectForContentRect_styleMask_(內容矩形, 樣式)
        return round(外框矩形.size.width), round(外框矩形.size.height)

    def _注入橋(self):
        當前網址 = urlsplit(self._window.get_current_url())
        if dict(parse_qsl(當前網址.query)).get('_librian_exit') == '1':
            self._window.destroy()
        else:
            self._window.run_js(橋腳本.read_text(encoding='utf8'))


def _本地網址(url):
    區段 = urlsplit(str(url))
    查詢 = parse_qsl(區段.query, keep_blank_values=True)
    查詢.append(('_librian_webview', '1'))
    return urlunsplit(區段._replace(query=urlencode(查詢)))


def 創建窗口(url, icon, title, size, storage_path):
    import webview

    return WebView窗口(webview, url, icon, title, size, storage_path)
