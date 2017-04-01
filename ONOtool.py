from Tkinter import *
#local functions
from LocalCommand import *
#from MainApp import *
from MainApp_random_graph import *

# initialize Tkinter
root = Tk()
root.title('ONO Tool')
root.resizable(width=FALSE, height=FALSE)  #not resizable
############################ LOCAL COMMAND #########################
command = LocalCommand()
############################## MYAPP ###############################
myapp = MainApp_random_graph(root)
####################################################################
# enter the Tkinter event loop
command.clearscreen()
print "Ready to start executing the event loop."
root.mainloop()
print "Finished       executing the event loop."
