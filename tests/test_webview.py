import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from librian.librian_util import 文件
from librian.librian本體 import webview窗口
from librian.librian本體.前端API import 山彥API


class 假事件:
    def __init__(self):
        self.handlers = []

    def __iadd__(self, handler):
        self.handlers.append(handler)
        return self

    def 觸發(self):
        for handler in self.handlers:
            handler()


class 假山彥:
    def 取檔(self):
        return [{'path': '/tmp/game'}]

    def 狀態回調(self, 步進):
        return {'步進': 步進}

    def 初始化(self):
        return {'path': '/tmp/game'}


class WebViewTests(unittest.TestCase):
    def test_local_paths_become_valid_encoded_file_urls(self):
        path = Path.cwd() / '有 空格'
        self.assertEqual(文件.轉爲網址路徑(path), path.resolve().as_uri())

    def test_api_exposes_explicit_methods_without_callbacks(self):
        api = 山彥API(假山彥())

        self.assertEqual(api.取檔(), [{'path': '/tmp/game'}])
        self.assertEqual(api.狀態回調(True), {'步進': True})
        self.assertEqual(api.初始化(), {'path': '/tmp/game'})
        self.assertFalse(hasattr(api, '讀者'))

    def test_windows_and_linux_share_the_public_pywebview_adapter(self):
        for system in ('Windows', 'Linux'):
            with self.subTest(system=system):
                fake_webview, native_window = self._fake_webview()
                with patch('platform.system', return_value=system), patch.dict(
                    sys.modules,
                    webview=fake_webview,
                ):
                    window = self._create_window()
                    window.運行()

                create_kwargs = fake_webview.create_window.call_args.kwargs
                self.assertEqual(create_kwargs['width'], 800)
                self.assertEqual(create_kwargs['height'], 600)
                self.assertEqual(
                    create_kwargs['url'],
                    'file:///tmp/custom-title.html?_librian_webview=1',
                )
                self.assertNotIn('gui', fake_webview.start.call_args.kwargs)
                self._assert_bridge_was_injected(fake_webview, native_window)

    def test_exit_url_closes_the_window_on_load(self):
        fake_webview, native_window = self._fake_webview()
        native_window.get_current_url.return_value = 'file:///title.html?_librian_exit=1'
        with patch.dict(sys.modules, webview=fake_webview):
            window = self._create_window()
            window.運行()

        native_window.destroy.assert_called_once()
        native_window.run_js.assert_not_called()

    def test_macos_preserves_content_size_without_private_webkit_apis(self):
        appkit = SimpleNamespace(
            NSWindowStyleMaskTitled=1,
            NSWindowStyleMaskClosable=2,
            NSWindowStyleMaskMiniaturizable=4,
            NSWindowStyleMaskResizable=8,
            NSMakeRect=lambda *_: object(),
            NSWindow=SimpleNamespace(
                frameRectForContentRect_styleMask_=lambda *_: SimpleNamespace(
                    size=SimpleNamespace(width=800, height=628),
                ),
            ),
        )
        fake_webview, native_window = self._fake_webview()

        with patch('platform.system', return_value='Darwin'), patch.dict(
            sys.modules,
            AppKit=appkit,
            webview=fake_webview,
        ):
            window = self._create_window()
            window.運行()

        create_kwargs = fake_webview.create_window.call_args.kwargs
        self.assertEqual(create_kwargs['width'], 800)
        self.assertEqual(create_kwargs['height'], 628)
        self.assertNotIn('gui', fake_webview.start.call_args.kwargs)
        self._assert_bridge_was_injected(fake_webview, native_window)

    def _fake_webview(self):
        loaded = 假事件()
        native_window = SimpleNamespace(
            events=SimpleNamespace(loaded=loaded),
            run_js=Mock(),
            evaluate_js=Mock(),
            toggle_fullscreen=Mock(),
            get_current_url=Mock(return_value='file:///title.html'),
            destroy=Mock(),
        )
        webview = SimpleNamespace(
            create_window=Mock(return_value=native_window),
            start=Mock(side_effect=lambda **_: loaded.觸發()),
        )
        return webview, native_window

    def _create_window(self):
        window = webview窗口.創建窗口(
            url='file:///tmp/custom-title.html',
            icon=None,
            title='Librian',
            size=(800, 600),
            storage_path='/tmp/librian-test-cache',
        )
        window.綁定(假山彥())
        return window

    def _assert_bridge_was_injected(self, fake_webview, native_window):
        create_kwargs = fake_webview.create_window.call_args.kwargs
        self.assertIsInstance(create_kwargs['js_api'], 山彥API)
        native_window.run_js.assert_called_once()


if __name__ == '__main__':
    unittest.main()
