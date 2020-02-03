# -*- coding: utf-8 -*-

from PySide2 import QtWidgets


class DirDialog:
    def __init__(self, window, title):
        self._parentWindow = window
        self._title = title

    def __enter__(self):
        self._dialog = QtWidgets.QFileDialog(parent=self._parentWindow,
                                             caption=self._title)
        self._dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptMode.AcceptOpen)
        self._dialog.setFileMode(QtWidgets.QFileDialog.FileMode.DirectoryOnly)
        self._dialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
        return self

    def __exit__(self, exc_type, exc, tb):
        if self._dialog.isVisible():
            self._dialog.close()

    def SetPath(self, path):
        self._dialog.setDirectory(path)

    def GetPath(self):
        return self._dialog.directory().absolutePath()

    def ShowModal(self):
        return self._dialog.exec_()


ID_OK = 1
