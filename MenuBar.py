from Tkinter import *
import tkMessageBox
import os

class MenuBar(Menu):
   def __init__(self, parent, callback_close,show_newedittopo,show_wellknowntopo,\
                show_randomtopo, show_kshort,callback_find_border,show_protectiononly,callback_nomap, callback_loadmap_jp,callback_loadmap_vn, callback_demo, callback_showtrf):
      Menu.__init__(self, parent)
      self.myParent = parent
      self.filename = None
      #--------------------------------------------------#
      self.menu = Menu(self.myParent)
      parent.config(menu=self.menu)
      #parent.config(self.menu=self.menu)
      # self.filemenu = Menu(self.menu)
      # self.menu.add_cascade(label="File", menu=self.filemenu)
      # self.filemenu.add_command(label="New", command=callback_clear)
      # self.filemenu.add_command(label="Open...", command=callback_open)
      # self.filemenu.add_separator()
      # self.filemenu.add_command(label="Exit", command=callback_close)
      ##################
      self.topologymenu = Menu(self.menu)
      self.menu.add_cascade(label="Topology", menu=self.topologymenu)
      self.topologymenu.add_command(label="New/Edit Topology", command= show_newedittopo)
      self.topologymenu.add_command(label="Well-known Topology", command= show_wellknowntopo)
      self.topologymenu.add_command(label="Random Topology", command=show_randomtopo)
      ##################
      self.basictoolmenu = Menu(self.menu)
      self.menu.add_cascade(label="Basic Tools", menu=self.basictoolmenu)
      self.basictoolmenu.add_command(label="k-shorted paths", command=show_kshort)
      self.basictoolmenu.add_command(label="Finding boundary", command=callback_find_border)
      ##################
      self.linkprotectionmenu = Menu(self.menu)
      self.menu.add_cascade(label="Link Protection", menu=self.linkprotectionmenu)
      self.linkprotectionmenu.add_command(label="Protection Only", command=show_protectiononly)
      self.linkprotectionmenu.add_command(label="Joint Working & Protection", command=None)
      ##################
      self.mapmenu = Menu(self.menu)
      self.menu.add_cascade(label="Maps", menu=self.mapmenu)
      self.mapmenu.add_command(label="None", command=callback_nomap)
      self.mapmenu.add_command(label="Japan", command=callback_loadmap_jp)
      self.mapmenu.add_command(label="Vietnam", command=callback_loadmap_vn)
      ##################
      self.helpmenu = Menu(self.menu)
      self.menu.add_cascade(label="Help", menu=self.helpmenu)
      self.helpmenu.add_command(label="Demo", command=callback_demo)
      self.helpmenu.add_command(label="Example of traffic file", command=callback_showtrf)
      self.helpmenu.add_command(label="About...", command=self.callback_about)
      parent.protocol("WM_DELETE_WINDOW", callback_close)
   def callback_about(self):
      tkMessageBox.showinfo("ONO tool",
                            "Program for creating network topology and performing optimization on network resource.")
