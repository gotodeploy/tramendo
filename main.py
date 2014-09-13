#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PySide.QtGui import *
from PySide.phonon import Phonon
from jamendo import JamendoRadio


class Tramendo(QDialog):
    def __init__(self):
        super(Tramendo, self).__init__()

        # Menu
        self.trayIconMenu = QMenu(self)

        # Build media player
        self.audioOuptut = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.player = Phonon.MediaObject(self)
        Phonon.createPath(self.player, self.audioOuptut)

        # Jamendo Actions
        self.jamendo = JamendoRadio()
        self.radioActions = QActionGroup(self)
        self.radioActions.setExclusive(True)
        self.radioActions.triggered.connect(self.play_stream_event)

        radio_stations = self.jamendo.get_radio_list()
        for radio in radio_stations:
            action = QAction(radio['dispname'], self)
            action.setCheckable(True)
            action.setData(radio['id'])
            self.radioActions.addAction(action)
            self.trayIconMenu.addAction(action)

        # Exit Action
        self.quitAction = QAction("&Exit", self)
        self.quitAction.triggered.connect(self.exit_event)
        self.trayIconMenu.addAction(self.quitAction)

        # Icon setting
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QApplication.style().standardIcon(QStyle.SP_MediaPlay))
        self.trayIcon.show()

    def exit_event(self):
        qApp.quit()

    def play_stream_event(self, action):
        info = self.jamendo.get_stream_info(action.data())

        self.player.stop()
        self.player.clearQueue()
        self.player.setCurrentSource(Phonon.MediaSource(info[0]['stream']))
        self.player.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if not QSystemTrayIcon.isSystemTrayAvailable():
        raise OSError("System tray is unavailable on this system.")

    tray = Tramendo()
    sys.exit(app.exec_())