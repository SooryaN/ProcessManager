#!/usr/bin/python
from Tkinter import *
import getpass,psutil
class my_app(Frame):
    """Basic Frame"""
    def __init__(self, master):
        """Init the Frame"""
        Frame.__init__(self,master)
        self.frames=[]
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

        #Searchbar
        self.search_var = StringVar()
        self.search_var.trace("w", self.update_list)
        self.entrySearch = Entry(self.frame, textvariable=self.search_var, width=13)
        self.entrySearch.grid(row=0, column=0, sticky='EW', pady=30)

        j=1
        for i in reversed(self.processes):
            self.newmessage = Button(self.frame, text= i.name(), anchor=W,
                                     command = lambda i=i: self.access(i.pid))
            self.newmessage.config(height = 3, width = 100)
            self.newmessage.grid(column = 0, row = j, columnspan=1,sticky=N)
            j+=1
        self.frames=self.frame.grid_slaves()
        print self.frames

        scrollbar = Scrollbar(self)
        scrollbar.grid(sticky='EW', column = 2, row = 0, rowspan = len(self.processes))

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

    def update_list(self, *args):
        search_term = self.search_var.get()
        for i in self.frames[:-1]:
            if search_term.lower() in i.config('text')[-1].lower():
                i.grid();
        print search_term
        if search_term!= '' and search_term!= ' ': 
            for i in self.frame.grid_slaves()[:-1]:
                print search_term.lower() in i.config('text')[-1].lower(),type(i)
                if search_term.lower() not in i.config('text')[-1].lower():
                    i.grid_forget();

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

if __name__ == '__main__':
    root = Tk()
    root.title("Process Killer")
    root.geometry("500x600")
    app = my_app(root)

    root.mainloop()
