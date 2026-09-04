import platform
from pathlib import Path

from .前端API import 山彥API


橋腳本 = Path(__file__).parent / '前端/pywebview橋.js'


class WebView窗口:
    def __init__(self, webview, url, icon, title, size, storage_path):
        self._webview = webview
        self._url = str(url)
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

    def 關閉(self):
        if self._window:
            self._window.destroy()

    def 運行(self):
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
        if platform.system() == 'Darwin':
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

        if platform.system() == 'Windows':
            import ctypes
            from ctypes import wintypes

            class RECT(ctypes.Structure):
                _fields_ = [
                    ('left', wintypes.LONG),
                    ('top', wintypes.LONG),
                    ('right', wintypes.LONG),
                    ('bottom', wintypes.LONG),
                ]

            內容寬, 內容高 = self._size
            rect = RECT(0, 0, 內容寬, 內容高)
            ctypes.windll.user32.AdjustWindowRectEx(ctypes.byref(rect), 0x00CF0000, False, 0)
            return rect.right - rect.left, rect.bottom - rect.top

        return self._size

    def _注入橋(self):
        self._window.run_js(橋腳本.read_text(encoding='utf8'))


def 創建窗口(url, icon, title, size, storage_path):
    import webview

    return WebView窗口(webview, url, icon, title, size, storage_path)
