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
"""
Clear the console.

numlines is an optional argument used only as a fall-back.
"""
class LocalCommand:
   def clearscreen(numlines=100):
      import os
      if os.name == "posix":
         # Unix/Linux/MacOS/BSD/etc
         os.system('clear')
      elif os.name in ("nt", "dos", "ce"):
         # DOS/Windows
         os.system('CLS')
      else:
         # Fallback for other operating systems.
         print '\n' * numlines

