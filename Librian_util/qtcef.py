# -*- coding: utf-8 -*-

import logging
import platform
import urllib
import ctypes
import os
import platform
import sys

import PySide2
from PySide2 import QtCore
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

ld_library_path = os.environ.get("LD_LIBRARY_PATH")
from cefpython3 import cefpython as cef


def group(url, icon, title, size):
    sys.excepthook = cef.ExceptHook
    settings = {}
    if WINDOWS:
        settings["external_message_pump"] = True
    elif MAC:
        # Issue #442 requires enabling message pump on Mac
        # in Qt example. Calling cef.DoMessageLoopWork in a timer
        # doesn't work anymore.
        settings["external_message_pump"] = True
    cef.Initialize(settings=settings,
                   commandLineSwitches={
                       "autoplay-policy": "no-user-gesture-required",
                       "lang": 'zh-CN'
                   })
    app = CefApp(url, icon, title, size)
    return app, app.frame.browser


# Fix for PyCharm hints warnings when using static methods
WindowUtils = cef.WindowUtils()

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")


def main():
    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    settings = {}
    if WINDOWS:
        settings["external_message_pump"] = True
    elif MAC:
        # Issue #442 requires enabling message pump on Mac
        # in Qt example. Calling cef.DoMessageLoopWork in a timer
        # doesn't work anymore.
        settings["external_message_pump"] = True

    cef.Initialize(settings)
    app = CefApp("http://localhost:8080", None, "localhost", (800, 600))
    app.MainLoop()
    del app.main_window  # Just to be safe, similarly to "del app"
    del app  # Must destroy app object before calling Shutdown
    cef.Shutdown()


def check_versions():
    print("[qt.py] CEF Python {ver}".format(ver=cef.__version__))
    print("[qt.py] Python {ver} {arch}".format(
        ver=platform.python_version(), arch=platform.architecture()[0]))
    print("[qt.py] PySide2 {v1} (qt {v2})".format(v1=PySide2.__version__,
                                                  v2=QtCore.__version__))
    # CEF Python version requirement
    assert cef.__version__ >= "55.4", "CEF Python v55.4+ required to run this"


class MainWindow(QMainWindow):
    def __init__(self, url, icon, title, size):
        # noinspection PyArgumentList
        super(MainWindow, self).__init__(None)
        self.url = url

        logging.debug("[qt.py] MainWindow DPI scaled size: %s" % str(size))
        width, height = tuple(size)
        self.resize(width, height)

        self.setWindowTitle(title)

        ic = QIcon(icon)
        self.setWindowIcon(ic)

        self.cef_widget = None
        self.setFocusPolicy(Qt.StrongFocus)
        self.setupLayout()

    def setupLayout(self):
        self.cef_widget = CefWidget(self)
        layout = QGridLayout()
        # noinspection PyArgumentList
        layout.addWidget(self.cef_widget, 1, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 1)
        # noinspection PyArgumentList
        frame = QFrame()
        frame.setLayout(layout)
        self.setCentralWidget(frame)

        if WINDOWS:
            # On Windows with PyQt5 main window must be shown first
            # before CEF browser is embedded, otherwise window is
            # not resized and application hangs during resize.
            self.show()

        # Browser can be embedded only after layout was set up
        self.cef_widget.embed_browser(self.url)

        if LINUX:
            # On Linux with PyQt5 the QX11EmbedContainer widget is
            # no more available. An equivalent in Qt5 is to create
            # a hidden window, embed CEF browser in it and then
            # create a container for that hidden window and replace
            # cef widget in the layout with the container.
            # noinspection PyUnresolvedReferences, PyArgumentList
            self.container = QWidget.createWindowContainer(
                self.cef_widget.hidden_window, parent=self)
            # noinspection PyArgumentList
            layout.addWidget(self.container, 1, 0)

    def closeEvent(self, event):
        # Close browser (force=True) and free CEF reference
        if self.cef_widget.browser:
            self.cef_widget.browser.CloseBrowser(True)
            self.clear_browser_references()

    def clear_browser_references(self):
        # Clear browser references that you keep anywhere in your
        # code. All references must be cleared for CEF to shutdown cleanly.
        self.cef_widget.browser = None

    def set_browser_object(self, name, obj):
        bindings = cef.JavascriptBindings()
        bindings.SetObject(name, obj)
        self.cef_widget.browser.SetJavascriptBindings(bindings)

    def toggleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    @property
    def browser(self):
        return self.cef_widget.browser


class CefWidget(QWidget):
    def __init__(self, parent=None):
        # noinspection PyArgumentList
        super(CefWidget, self).__init__(parent)
        self.parent = parent
        self.browser = None
        self.hidden_window = None  # Required for PyQt5 on Linux
        self.show()

    def focusInEvent(self, event):
        # This event seems to never get called on Linux, as CEF is
        # stealing all focus due to Issue #284.
        if cef.GetAppSetting("debug"):
            print("[qt.py] CefWidget.focusInEvent")
        if self.browser:
            if WINDOWS:
                WindowUtils.OnSetFocus(self.getHandle(), 0, 0, 0)
            self.browser.SetFocus(True)

    def focusOutEvent(self, event):
        # This event seems to never get called on Linux, as CEF is
        # stealing all focus due to Issue #284.
        if cef.GetAppSetting("debug"):
            print("[qt.py] CefWidget.focusOutEvent")
        if self.browser:
            self.browser.SetFocus(False)

    def embed_browser(self, url):
        if LINUX:
            # noinspection PyUnresolvedReferences
            self.hidden_window = QWindow()
        window_info = cef.WindowInfo()
        rect = [0, 0, self.width(), self.height()]
        window_info.SetAsChild(self.getHandle(), rect)
        self.browser = cef.CreateBrowserSync(window_info, url=url, browserSettings={'web_security_disabled': True})
        self.browser.SetClientHandler(FocusHandler(self))

    def getHandle(self):
        if self.hidden_window:
            # PyQt5 on Linux
            return int(self.hidden_window.winId())
        try:
            # PyQt4 and PyQt5
            return int(self.winId())
        except:
            # PySide:
            # | QWidget.winId() returns <PyCObject object at 0x02FD8788>
            # | Converting it to int using ctypes.
            ctypes.pythonapi.PyCapsule_GetPointer.restype = (ctypes.c_void_p)
            ctypes.pythonapi.PyCapsule_GetPointer.argtypes = ([
                ctypes.py_object
            ])
            return ctypes.pythonapi.PyCapsule_GetPointer(self.winId(), None)

    def moveEvent(self, _):
        self.x = 0
        self.y = 0
        if self.browser:
            if WINDOWS:
                WindowUtils.OnSize(self.getHandle(), 0, 0, 0)
            elif LINUX:
                self.browser.SetBounds(self.x, self.y, self.width(),
                                       self.height())
            self.browser.NotifyMoveOrResizeStarted()

    def resizeEvent(self, event):
        size = event.size()
        if self.browser:
            if WINDOWS:
                WindowUtils.OnSize(self.getHandle(), 0, 0, 0)
            elif LINUX:
                self.browser.SetBounds(self.x, self.y, size.width(),
                                       size.height())
            self.browser.NotifyMoveOrResizeStarted()


class CefApp(QApplication):
    def __init__(self, url, icon, title, size):
        super(CefApp, self).__init__([])
        if cef.GetAppSetting("external_message_pump") or \
                cef.GetAppSetting("multi_threaded_message_loop"):
            self.timer = None
        else:
            self.timer = self.createTimer()

        self.url, self.icon, self.title, self.size = url, icon, title, size

        self.main_window = MainWindow(url, icon, title, size)
        self.main_window.show()
        self.main_window.activateWindow()
        self.main_window.raise_()
        self.frame = self.main_window

    def MainLoop(self):
        self.exec_()
        if self.timer is not None:
            self.stopTimer()

    def createTimer(self):
        timer = QTimer()
        # noinspection PyUnresolvedReferences
        timer.timeout.connect(self.onTimer)
        timer.start(10)
        return timer

    def onTimer(self):
        cef.MessageLoopWork()

    def stopTimer(self):
        # Stop the timer after Qt's message loop has ended
        self.timer.stop()


class FocusHandler(object):
    def __init__(self, cef_widget):
        self.cef_widget = cef_widget

    def OnTakeFocus(self, **_):
        if cef.GetAppSetting("debug"):
            print("[qt.py] FocusHandler.OnTakeFocus")

    def OnSetFocus(self, **_):
        if cef.GetAppSetting("debug"):
            print("[qt.py] FocusHandler.OnSetFocus")

    def OnGotFocus(self, browser, **_):
        if cef.GetAppSetting("debug"):
            print("[qt.py] FocusHandler.OnGotFocus")
        self.cef_widget.setFocus()
        # Temporary fix no. 1 for focus issues on Linux (Issue #284)
        if LINUX:
            browser.SetFocus(True)


if __name__ == '__main__':
    main()
