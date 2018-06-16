# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
"""
Main service module

This module handles all TV Melodies services in Kodi

This file is part of TV Melodies.

TV Melodies is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

TV Melodies is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with TV Melodies. If not, see <http://www.gnu.org/licenses/>.

@author: smitchell6879
@license: GPL-3.0
"""
import os
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

addon = xbmcaddon.Addon()
player = xbmc.Player()
addonID = addon.getAddonInfo("id")

class Monitor(xbmc.Monitor):
    def __init__(self):
        xbmc.log(msg='{}:{}'.format(addonID, "is running"), level=xbmc.LOGINFO)
        self.nowplaying = ""
        while not self.abortRequested():
            self.enable = addon.getSetting("enable")
            self.debug = addon.getSetting("debug")
            if self.enable == "true":
                try:
                    self.cw = xbmcgui.getCurrentWindowId()
                    self.p = xbmc.getInfoLabel('Container({}).ListItem().Path'.format(xbmc.getInfoLabel('System.CurrentControlID')))
                    self.dirs, self.files = xbmcvfs.listdir(self.p)
                    for self.i in self.files:
                        if "theme" in self.i:
                            self.fnp = os.path.join(self.p, self.i)
                            if self.fnp != self.nowplaying:
                                if player.isPlaying():
                                    if "theme" in player.getPlayingFile():
                                        self.play()
                                else:
                                    self.play()
                            if self.debug:
                                xbmc.log(msg='{}: {}'.format(addonID, self.fnp), level=xbmc.LOGDEBUG)
                    if self.debug:
                        xbmc.log(msg='{}: {}'.format(addonID, self.p), level=xbmc.LOGDEBUG)
                        xbmc.log(msg='{}: {}'.format(addonID, self.cw), level=xbmc.LOGDEBUG)
                except Exception as err:
                    xbmc.log(msg='{}: {}'.format(addonID, err), level=xbmc.LOGERROR)
            if self.waitForAbort(.5):
                xbmc.log(msg='{}:{}'.format(addonID, "is exiting"), level=xbmc.LOGINFO)
                sys.exit(0)
    def play(self):
        if self.cw == 10025:
            self.nowplaying = self.fnp
            player.play(item=self.fnp, windowed=True)
            return

if __name__ == '__main__':
    Monitor()
