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
from Tkinter import Canvas, Frame, Scrollbar

class ScrolledFrame(Frame):
   def __init__(self, master=None, width=1000, height=1000):
      #create scrolling canvas
      canvas = Canvas(master, height=height, width=width)
      canvas.grid(row=0, column=0, sticky='nswe')

      #call super class using scrolling canvas as master
      Frame.__init__(self, master=canvas)

      #crete scrollbars for the canvas
      hScroll = Scrollbar(master, orient='horizontal', command=canvas.xview)
      hScroll.grid(row=1, column=0, sticky='we')
      vScroll = Scrollbar(master, orient='vertical', command=canvas.yview)
      vScroll.grid(row=0, column=1, sticky='ns')
      canvas.configure(xscrollcommand=hScroll.set, yscrollcommand=vScroll.set)
      
      #embed frame within the scrolling canvas
      canvas.create_window(0,0, window=self, anchor='nw')
      
      #save reference to scrolling canvas
      self.canvas=canvas
      
   def updateScrollers(self):
      '''update the canvas scrollregion based on size of embedded frame'''
      self.update_idletasks()
      self.canvas.configure(scrollregion=self.canvas.bbox('all'))
   
