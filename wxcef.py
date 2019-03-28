import wx
from cefpython3 import cefpython as cef

import sys
import os


def group(url, icon, title, size):
    sys.excepthook = cef.ExceptHook
    cef.Initialize(settings={})
    app = CefApp(url, icon, title, size)
    return app, app.frame.browser


def main():
    app, browser = group()
    app.MainLoop()
    del app


class MainFrame(wx.Frame):

    def __init__(self, url, icon, title, size):
        self.browser = None

        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title=title, style=wx.DEFAULT_FRAME_STYLE | wx.WANTS_CHARS)

        self.browser_panel = wx.Panel(self, size=tuple(size))
        self.browser_panel.Bind(wx.EVT_SIZE, self.OnSize)
        wx.Window.Fit(self)

        self.embed_browser(url)

        ic = wx.Icon(icon, wx.BITMAP_TYPE_ICO)
        self.SetIcon(ic)

        self.Show()

    def embed_browser(self, url):
        window_info = cef.WindowInfo()
        width, height = self.browser_panel.GetClientSize().Get()
        assert self.browser_panel.GetHandle(), "Window handle not available"
        window_info.SetAsChild(self.browser_panel.GetHandle(),
                               [0, 0, width, height])
        self.browser = cef.CreateBrowserSync(window_info, url=url)

    def set_browser_object(self, name, obj):
        bindings = cef.JavascriptBindings()
        bindings.SetObject(name, obj)
        self.browser.SetJavascriptBindings(bindings)

    def OnSize(self, _):
        if not self.browser:
            return
        cef.WindowUtils.OnSize(self.browser_panel.GetHandle(),
                               0, 0, 0)
        self.browser.NotifyMoveOrResizeStarted()

    def toggleFullScreen(self):
        if self.IsFullScreen():
            self.ShowFullScreen(False)
        else:
            self.ShowFullScreen(True)


class CefApp(wx.App):

    def __init__(self, url, icon, title, size):
        self.url, self.icon, self.title, self.size = url, icon, title, size

        self.timer = None
        self.timer_id = 1
        self.is_initialized = False

        super(CefApp, self).__init__(redirect=False)

    def OnPreInit(self):
        super(CefApp, self).OnPreInit()

    def OnInit(self):
        if self.is_initialized:
            return True
        self.is_initialized = True
        self.create_timer()
        self.frame = MainFrame(self.url, self.icon, self.title, self.size)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

    def create_timer(self):
        self.timer = wx.Timer(self, self.timer_id)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(10)

    def on_timer(self, _):
        cef.MessageLoopWork()


if __name__ == '__main__':
    main()
