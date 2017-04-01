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
import tkSimpleDialog

class EditDialog(tkSimpleDialog.Dialog):
   def __init__(self, parent, title = None, labelText = None, dialogText = None, typeText=None):
      Toplevel.__init__(self, parent)
      self.transient(parent)
      if title:
         self.title(title)
      if labelText:
         self.labelText = []
         self.nboxl = len(labelText)
         for i in range(self.nboxl):
            self.labelText.append(labelText[i])
      if dialogText:
         self.dialogText = []
         self.nboxd = len(dialogText)
         for i in range(self.nboxd):
            self.dialogText.append(dialogText[i])
      self.typeText = None
      if typeText:
         self.typeText = typeText
      self.parent = parent
      self.result = []
      body = Frame(self)
      self.initial_focus = self.body(body)
      body.pack(padx=5, pady=5)
      self.buttonbox()
      #self.grab_set()
      if not self.initial_focus:
         self.initial_focus = self
      self.protocol("WM_DELETE_WINDOW", self.cancel)
      self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))
      self.initial_focus.focus_set()
      self.wait_window(self)
   def body(self, parent):
      self.e = []
      for i in range(self.nboxl):
         Label(parent, text=self.labelText[i]).grid(row=i)
         self.e.append(None)
         self.e[i] = Entry(parent)
         self.e[i].insert(0, self.dialogText[i])
         self.e[i].grid(row=i, column=1)
         if self.typeText == "line":
            Label(parent, text='km').grid(row=i, column=2)
      return self.e[0] # initial focus
   def apply(self):
      #first = string.atoi(self.e1.get())
      #second = string.atoi(self.e2.get())
      for i in range(self.nboxl):
         self.result.append(self.e[i].get())
