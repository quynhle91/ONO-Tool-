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

class ScrolledCanvas():
   def __init__(self, parent=None, wg=None):
      self.scrollY = Scrollbar ( parent, orient=VERTICAL, command=wg.yview )
      self.scrollY.grid ( row=0, column=1, sticky=N+S )

      self.scrollX = Scrollbar ( parent, orient=HORIZONTAL, command=wg.xview )
      self.scrollX.grid ( row=1, column=0, sticky=E+W )

      wg["xscrollcommand"]  =  self.scrollX.set
      wg["yscrollcommand"]  =  self.scrollY.set
      self.scrollX.pack(side=BOTTOM, fill=X)
      self.scrollY.pack(side=RIGHT, fill=Y)
