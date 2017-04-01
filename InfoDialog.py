"""
Copyright 2011 Wissarut Yuttachai, Pratkasem Vesarach, Poompat Saengudomlert
======================================================================
    This file is part of WDMPlanner.

    WDMPlanner is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    WDMPlanner is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with WDMPlanner.  If not, see <http://www.gnu.org/licenses/>.
======================================================================
"""
from Tkinter import *

def InfoDialog(self, frame, title = None, labelText = None, distText = None):
      if title:
         frame.title(title)
      if labelText:
         self.labelText = []
         self.nboxl = len(labelText)
         for i in range(self.nboxl):
            self.labelText.append(labelText[i])
      if distText:
         self.distText = []
         self.nboxd = len(distText)
         for i in range(self.nboxd):
            self.distText.append(distText[i])
      for i in range(self.nboxl):
         Label(frame, text=self.labelText[i]+": ").grid(row=i)
         Label(frame, text=self.distText[i]).grid(row=i,column=1)
         Label(frame, text='km').grid(row=i, column=2)

