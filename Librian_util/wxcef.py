import logging
import platform
import sys
import os

import wx
from cefpython3 import cefpython as cef


def group(url, icon, title, size):
    sys.excepthook = cef.ExceptHook
    cef.Initialize(settings={}, commandLineSwitches={
        "autoplay-policy": "no-user-gesture-required",
        "lang": 'zh-CN'
    })
    app = CefApp(url, icon, title, size)
    return app, app.frame.browser


# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

if MAC:
    try:
        # noinspection PyUnresolvedReferences
        from AppKit import NSApp
    except ImportError:
        logging.debug("[wxpython.py] Error: PyObjC package is missing, "
                      "cannot fix Issue #371")
        logging.debug("[wxpython.py] To install PyObjC type: "
                      "pip install -U pyobjc")
        sys.exit(1)

if LINUX:
    import gi
    gi.require_version('Gtk','3.0')
    from gi.repository import Gtk,Gdk,GdkX11

# Globals
g_count_windows = 0


def main():
    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    settings = {}
    if MAC:
        # Issue #442 requires enabling message pump on Mac
        # and calling message loop work in a timer both at
        # the same time. This is an incorrect approach
        # and only a temporary fix.
        settings["external_message_pump"] = True
    if WINDOWS:
        # noinspection PyUnresolvedReferences, PyArgumentList
        cef.DpiAware.EnableHighDpiSupport()
    cef.Initialize(settings=settings)
    app = CefApp(False)
    app.MainLoop()
    del app  # Must destroy before calling Shutdown
    if not MAC:
        # On Mac shutdown is called in OnClose
        cef.Shutdown()


def check_versions():
    logging.debug("[wxpython.py] CEF Python {ver}".format(ver=cef.__version__))
    logging.debug("[wxpython.py] Python {ver} {arch}".format(
        ver=platform.python_version(), arch=platform.architecture()[0]))
    logging.debug("[wxpython.py] wxPython {ver}".format(ver=wx.version()))
    # CEF Python version requirement
    assert cef.__version__ >= "66.0", "CEF Python v66.0+ required to run this"


class MainFrame(wx.Frame):

    def __init__(self, url, icon, title, size):
        self.browser = None

        # Must ignore X11 errors like 'BadWindow' and others by
        # installing X11 error handlers. This must be done after
        # wx was intialized.
        if LINUX:
            cef.WindowUtils.InstallX11ErrorHandlers()

        global g_count_windows
        g_count_windows += 1

        if WINDOWS:
            # noinspection PyUnresolvedReferences, PyArgumentList
            logging.debug("[wxpython.py] System DPI settings: %s"
                          % str(cef.DpiAware.GetSystemDpi()))
        if hasattr(wx, "GetDisplayPPI"):
            logging.debug("[wxpython.py] wx.GetDisplayPPI = %s" % wx.GetDisplayPPI())
        logging.debug("[wxpython.py] wx.GetDisplaySize = %s" % wx.GetDisplaySize())

        logging.debug("[wxpython.py] MainFrame DPI scaled size: %s" % str(size))

        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY,
                          title=title)
        # wxPython will set a smaller size when it is bigger
        # than desktop size.
        logging.debug("[wxpython.py] MainFrame actual size: %s" % self.GetSize())

        ic = wx.Icon(icon, wx.BITMAP_TYPE_ICO)
        self.SetIcon(ic)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Set wx.WANTS_CHARS style for the keyboard to work.
        # This style also needs to be set for all parent controls.
        self.browser_panel = wx.Panel(self, size=tuple(size))
        self.browser_panel.Bind(wx.EVT_SIZE, self.OnSize)
        wx.Window.Fit(self)

        if MAC:
            # Make the content view for the window have a layer.
            # This will make all sub-views have layers. This is
            # necessary to ensure correct layer ordering of all
            # child views and their layers. This fixes Window
            # glitchiness during initial loading on Mac (Issue #371).
            NSApp.windows()[0].contentView().setWantsLayer_(True)

        if LINUX:
            self.Show()
            self.embed_browser(url)
        else:
            self.embed_browser(url)
            self.Show()

    def embed_browser(self, url):
        window_info = cef.WindowInfo()
        (width, height) = self.browser_panel.GetClientSize().Get()
        assert self.browser_panel.GetHandle(), "Window handle not available"
        if LINUX:
            handle_to_use = self.browser_panel.GetHandle()
            display = Gdk.Display.get_default()
            window = GdkX11.X11Window.foreign_new_for_display(display,handle_to_use)
            self.gtk_window = gtk_window = Gtk.Window()
            def callback(gtk_window,window):
                print("inside callback")
                gtk_window.set_window(window)
                gtk_window.set_visual( gtk_window.get_screen().lookup_visual(0x21))
            gtk_window.connect("realize",callback,window)
            gtk_window.set_has_window(True)
            gtk_window.show()
            sw = Gtk.ScrolledWindow()
            sw.show()
            gtk_window.add(sw)
            sw.set_visual( sw.get_screen().lookup_visual(0x21))
            self.sw = sw
            self.Show()
            window_info.SetAsChild(sw.get_window().get_xid(),[0, 0, width, height])
        else:
            window_info.SetAsChild(self.browser_panel.GetHandle(), [0, 0, width, height])
        self.browser = cef.CreateBrowserSync(window_info,url=url,browserSettings={'web_security_disabled': True,})
        self.browser.SetClientHandler(FocusHandler())

    def set_browser_object(self, name, obj):
        bindings = cef.JavascriptBindings()
        bindings.SetObject(name, obj)
        self.browser.SetJavascriptBindings(bindings)

    def OnSetFocus(self, _):
        if not self.browser:
            return
        if WINDOWS:
            cef.WindowUtils.OnSetFocus(self.browser_panel.GetHandle(),
                                       0, 0, 0)
        self.browser.SetFocus(True)

    def OnSize(self, _):
        if not self.browser:
            return
        if WINDOWS:
            cef.WindowUtils.OnSize(self.browser_panel.GetHandle(),
                                   0, 0, 0)
        elif LINUX:
            (x, y) = (0, 0)
            (width, height) = self.browser_panel.GetSize().Get()
            self.browser.SetBounds(x, y, width, height)
            self.sw.get_window().move_resize(x,y,width,height)
        self.browser.NotifyMoveOrResizeStarted()

    def OnClose(self, event):
        logging.debug("[wxpython.py] OnClose called")
        if not self.browser:
            # May already be closing, may be called multiple times on Mac
            return

        if MAC:
            # On Mac things work differently, other steps are required
            self.browser.CloseBrowser()
            self.clear_browser_references()
            self.Destroy()
            global g_count_windows
            g_count_windows -= 1
            if g_count_windows == 0:
                cef.Shutdown()
                wx.GetApp().ExitMainLoop()
                # Call _exit otherwise app exits with code 255 (Issue #162).
                # noinspection PyProtectedMember
                os._exit(0)
        else:
            # Calling browser.CloseBrowser() and/or self.Destroy()
            # in OnClose may cause app crash on some paltforms in
            # some use cases, details in Issue #107.
            self.browser.ParentWindowWillClose()
            event.Skip()
            self.clear_browser_references()

    def clear_browser_references(self):
        # Clear browser references that you keep anywhere in your
        # code. All references must be cleared for CEF to shutdown cleanly.
        self.browser = None

    def toggleFullScreen(self):
        if self.IsFullScreen():
            self.ShowFullScreen(False)
        else:
            self.ShowFullScreen(True)


class FocusHandler(object):
    def OnGotFocus(self, browser, **_):
        # Temporary fix for focus issues on Linux (Issue #284).
        if LINUX:
            logging.debug("[wxpython.py] FocusHandler.OnGotFocus:"
                          " keyboard focus fix (Issue #284)")
            browser.SetFocus(True)


class CefApp(wx.App):
    def __init__(self, url, icon, title, size):
        self.url, self.icon, self.title, self.size = url, icon, title, size

        self.timer = None
        self.timer_id = 1
        self.is_initialized = False

        super(CefApp, self).__init__(redirect=False)

    def OnPreInit(self):
        super(CefApp, self).OnPreInit()
        # On Mac with wxPython 4.0 the OnInit() event never gets
        # called. Doing wx window creation in OnPreInit() seems to
        # resolve the problem (Issue #350).
        if MAC and wx.version().startswith("4."):
            logging.debug("[wxpython.py] OnPreInit: initialize here"
                          " (wxPython 4.0 fix)")
            self.initialize()

    def OnInit(self):
        self.initialize()
        return True

    def initialize(self):
        if self.is_initialized:
            return
        self.is_initialized = True
        self.create_timer()
        self.frame = MainFrame(self.url, self.icon, self.title, self.size)
        self.SetTopWindow(self.frame)
        self.frame.Show()

    def create_timer(self):
        # See also "Making a render loop":
        # http://wiki.wxwidgets.org/Making_a_render_loop
        # Another way would be to use EVT_IDLE in MainFrame.
        self.timer = wx.Timer(self, self.timer_id)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(10)  # 10ms timer

    def on_timer(self, _):
        cef.MessageLoopWork()

    def OnExit(self):
        self.timer.Stop()
        return 0


if __name__ == '__main__':
    main()
