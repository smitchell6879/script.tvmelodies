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
home = xbmcgui.Window(10000)

class Monitor(xbmc.Monitor):
    def __init__(self):
        xbmc.log(msg='{}:{}'.format(addonID, "is running"), level=xbmc.LOGINFO)
        self.nowplaying = ""
        self.nowplayingp = ""
        self.timer = 0
        while not self.abortRequested():
            self.enable = addon.getSetting("enable")
            self.delay = int(addon.getSetting("delay"))
            self.debug = addon.getSetting("debug")
            self.vtwelve = addon.getSetting("volume12")  # Get the volume from the settings file JL
            self.vorg = "100"  # Figure out how to get the original volume and place it here JL
            if self.enable == "true":
                try:
                    self.cw = xbmcgui.getCurrentWindowId()
                    self.cw2 = xbmc.executebuiltin("Window.IsActive(musicinformation)")
                    self.xml = xbmc.getInfoLabel("Window.Property(xmlfile)")
                    self.p = xbmc.getInfoLabel('Container({}).ListItem().Path'.format(xbmc.getInfoLabel('System.CurrentControlID')))
                    self.pi = xbmc.getInfoLabel('ListItem().FolderPath')
                    if not self.p:
                        self.p = xbmc.getInfoLabel('Container({}).ListItem.Property(originalpath)'.format(xbmc.getInfoLabel('System.CurrentControlID')))
                    if player.isPlaying():
                        if "theme" in player.getPlayingFile():
                            if self.xml != "DialogVideoInfo.xml":
                                if self.p != self.nowplayingp:
                                    player.stop()
                                    home.clearProperty("TVMelodies.isPlaying")
                                    self.timer = 0
                                    self.acommand="SetVolume("+self.vorg+")"  # Build the python code for exec JL
                                    xbmc.executebuiltin(self.acommand)  # Restore the original volume JL

                    '''Does not seem to work when trying to play after
                        DialogVideoInfo has been opened'''
                    # if self.xml == "DialogVideoInfo.xml":
                    #     self.dirs, self.files = xbmcvfs.listdir(self.pi)
                    self.dirs, self.files = xbmcvfs.listdir(self.p)
                    for self.i in self.files:
                        if "theme" in self.i:
                            self.fnp = os.path.join(self.p, self.i)
                            if self.fnp != self.nowplaying:
                                if self.timer == self.delay:
                                    if player.isPlaying():
                                        if "theme" in player.getPlayingFile():
                                            self.play()
                                    else:
                                        self.play()
                                else:
                                    self.timer+=.5
                            if self.debug:
                                xbmc.log(msg='{}: {}'.format(addonID, self.fnp), level=xbmc.LOGDEBUG)
                                xbmc.log(msg='{}: {}'.format(addonID, self.timer), level=xbmc.LOGDEBUG)
                                xbmc.log(msg='{}: {}'.format(addonID, self.vtwelve), level=xbmc.LOGDEBUG) # JSR
                    if self.debug:
                        xbmc.log(msg='{}: {}'.format(addonID, self.p), level=xbmc.LOGDEBUG)
                        xbmc.log(msg='{}: {}'.format(addonID, self.pi), level=xbmc.LOGDEBUG)
                        xbmc.log(msg='{}: {}'.format(addonID, self.cw), level=xbmc.LOGDEBUG)
                except Exception as err:
                    xbmc.log(msg='{}: {}'.format(addonID, err), level=xbmc.LOGERROR)
            if self.waitForAbort(.5):
                xbmc.log(msg='{}:{}'.format(addonID, "is exiting"), level=xbmc.LOGINFO)
                sys.exit(0)
    def play(self):
        if self.cw == 10025:
            self.nowplaying = self.fnp
            self.nowplayingp = self.p
            #self.acommand="SetVolume("+self.vtwelve+",false)"
            self.acommand="SetVolume("+self.vtwelve+")" # Build volume command code JL
            if self.debug: xbmc.log(addonID+" play: ("+self.vtwelve+") "+self.acommand+" "+self.fnp, level=xbmc.LOGINFO) # JL
            xbmc.executebuiltin(self.acommand) # Set clip volume JL
            home.setProperty("TVMelodies.isPlaying", "True")
            player.play(item=self.fnp, windowed=True)
        '''Does not seem to work when trying to play after
            DialogVideoInfo has been opened'''
        # else:
        #     if self.xml == "DialogVideoInfo.xml":
        #         self.nowplaying = self.fnp
        #         self.nowplayingp = self.pi
        #         home.setProperty("TVMelodies.isPlaying", "True")
        #         player.play(item=self.fnp, windowed=True)



if __name__ == '__main__':
    Monitor()