import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from vncselector import *
import newconnectionwindow

class Window(ttk.Frame):

    def __init__(self, master=None):
        self.host_text = tk.StringVar()
        self.host_text.set("")

        self.ip_text = tk.StringVar()
        self.ip_text.set("")
        
        tk.Frame.__init__(self, master)
        self.master = master
        master.title("VNC Selector")
        master.geometry("250x225+50+50")
        master.resizable(0,0)

        self.labelA = tk.Label(master, text="Choose connection:")
        self.labelA.grid(row=0, column=0, columnspan=3, sticky=tk.W)

        self.listboxA = tk.Listbox(master)
        self.listboxA.grid(row=1, column=0, rowspan=8, columnspan=3, padx=5)
        self.updateList()
        self.listboxA.bind('<<ListboxSelect>>', self.updateLabelText)

        self.labelB = tk.Label(master, text="Hostname:")
        self.labelB.grid(row=1, column=4, columnspan=2, sticky=tk.W)

        self.host_label = tk.Label(master, textvariable=self.host_text)
        self.host_label.grid(row=2, column=4, columnspan=2, sticky=tk.W)

        self.labelC = tk.Label(master, text="IP Address:")
        self.labelC.grid(row=3, column=4, columnspan=2, sticky=tk.W)

        self.ip_label = tk.Label(master, textvariable=self.ip_text)
        self.ip_label.grid(row=4, column=4, columnspan=2, sticky=tk.W)

        self.vnc_button = tk.Button(master, text="VNC", command=self.connectVNC, width=12)
        self.vnc_button.grid(row=5, column=4, columnspan=2, padx=15)

        self.ssh_button = tk.Button(master, text="SSH", command=self.connectSSH, width=12)
        self.ssh_button.grid(row=6, column=4, columnspan=2, padx=15)

        self.add_button = tk.Button(master, text="Add New", command=self.addNew, width=12)
        self.add_button.grid(row=7, column=4, columnspan=2, padx=15)

        self.remove_button = tk.Button(master, text="Remove", command=self.remove, width=12)
        self.remove_button.grid(row=8, column=4, columnspan=2, padx=15)

        
    def connectVNC(self):
        if self.listboxA.curselection():
            launchViewer(getInfo(self.listboxA.get(self.listboxA.curselection())))

    def connectSSH(self):
        if self.listboxA.curselection():
            launchSSH(getInfo(self.listboxA.get(self.listboxA.curselection())))

    def addNew(self):
        print("add")
        self.pup = newconnectionwindow.NewConnectionWindow(self, "Add New")
        #self.pup.wait_window()  ####
        self.updateList()

    def remove(self):
        if self.listboxA.curselection():
            if messagebox.askyesno("Remove", "Are you sure you want to delete this connection?"):
                messagebox.showinfo("Remove", "Connection removed!")
                removeComputer(self.listboxA.get(self.listboxA.curselection()))
                self.updateList()

    def updateList(self):
        computer_dict = loadComputers()
        self.listboxA.delete('0', 'end')
        for key in computer_dict:
            self.listboxA.insert(tk.END, key)

    def updateLabelText(self, event):
        self.host_text.set(self.listboxA.get(self.listboxA.curselection()))
        self.ip_text.set(getInfo(self.listboxA.get(self.listboxA.curselection()))[0])
        

root = tk.Tk()
app = Window(root)
root.mainloop()

