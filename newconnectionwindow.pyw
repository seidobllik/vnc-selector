import tkinter as tk

from vncselector import addComputer

class NewConnectionWindow:
    
    def __init__(self, parent, title):

        top = self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("+70+120")
        self.top.resizable(0,0)
        self.top.grab_set()

        tk.Label(top, text="Hostname").grid(row=0, column=0, columnspan=3, padx=10)
        tk.Label(top, text="IP Address").grid(row=1, column=0, columnspan=3, padx=10)
        tk.Label(top, text="Password").grid(row=2, column=0, columnspan=3, padx=10)
        

        self.hostname = tk.Entry(top)
        self.hostname.grid(row=0, column=3, columnspan=3, padx=10)
        self.address = tk.Entry(top)
        self.address.grid(row=1, column=3, columnspan=3, padx=10)
        self.password = tk.Entry(top)
        self.password.grid(row=2, column=3, columnspan=3, padx=10)

        okButton = tk.Button(top, text="OK", command=self.ok, width=12)
        okButton.grid(row=3, column=2, columnspan=3)

        parent.wait_window(self.top)
        
    def ok(self):
        if (len(str(self.hostname.get())) > 0
            and len(str(self.address.get())) > 0
            and len(str(self.password.get())) > 0):
            addComputer(self.hostname.get(), self.address.get(), self.password.get())
            self.top.destroy()
        else:
            self.top.destroy()


##root = tk.Tk()
##d = NewConnectionWindow(root, "testing")
##
##root.wait_window(d.top)
