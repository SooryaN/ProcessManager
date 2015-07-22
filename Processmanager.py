from Tkinter import *
import getpass,psutil
class my_app(Frame):
    """Basic Frame"""
    def __init__(self, master):
        """Init the Frame"""
        Frame.__init__(self,master)
        self.canvas = Canvas(root, borderwidth=0, background="#ffffff")
        self.frame = Frame(self.canvas, background="#ffffff")
        self.vsb = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.processes=[]
        self.getProcess()
        self.Create_Widgets()
    
    def Create_Widgets(self):
        j=0
        for i in reversed(self.processes):
            self.newmessage = Button(self.frame, text= i.name(), anchor=W,
                                     command = lambda i=i: self.access(i.pid))
            self.newmessage.config(height = 3, width = 100)
            self.newmessage.grid(column = 0, row = j, sticky = NW)
            j+=1
        scrollbar = Scrollbar(self)
        scrollbar.grid(sticky=E, column = 1, row = 0, rowspan = len(self.processes),  ipady = 1000)

    def access(self, b_id):
        print b_id
        for process in self.processes:
            if process.pid==b_id:
                process.kill()
                self.getProcess()
                self.Create_Widgets()

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def getProcess(self):
        for process in psutil.process_iter():
            if getpass.getuser()=='root' and process.is_running():
                try:
                    psutil.NoSuchProcess
                    self.processes.append(process)
                except:
                    pass
            elif process.username()==getpass.getuser() and process.is_running():
                try:
                    psutil.NoSuchProcess
                    self.processes.append(process)
                except:
                    pass

#Root Stuff

root = Tk()
root.title("Process Killer")
root.geometry("500x600")
app = my_app(root)

root.mainloop()
