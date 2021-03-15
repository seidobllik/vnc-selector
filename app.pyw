import tkinter as tk
import tkinter.ttk as ttk
import selector_tools


class Splash(tk.Toplevel):
    '''
    Splash screen with loading bar.
    '''
    def __init__(self, parent):
        width = 300
        height = 70
        tk.Toplevel.__init__(self, parent)
        self.geometry(f'{width}x{height}')
        self.overrideredirect(True)  # Hides the titlebar.
        tk.Label(self, text='Loading...').pack()
        self.progress_bar = ttk.Progressbar(self, orient=tk.HORIZONTAL,
                                            length=200, mode='indeterminate')
        self.progress_bar.pack(expand=True)
        self.message_string = tk.StringVar()
        self.message_string.set('Initializing socket...')
        self.message_label = tk.Label(self, textvariable=self.message_string)
        self.message_label.pack()
        x_location = int(self.winfo_screenwidth()/2 - width/2)
        y_location = int(self.winfo_screenheight()/2 - height/2)
        self.geometry(f'+{x_location}+{y_location}')
        self.update()
    
    def update_progress(self, message=''):
        '''
        Makes the progress bar value progress, and optionally updates the message string.
        '''
        self.update_idletasks()
        self.progress_bar['value'] += 10
        self.message_string.set(message)


class App(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)

        # Instance variables.
        self.hostname, self.ip_address = selector_tools.get_this_pc_info().values()
        self.title(f'VNC Selector v2 - {self.hostname}')
        self.available_connections = {}
        self.listbox_list = tk.StringVar()
        self.target_hostname = tk.StringVar()
        self.target_ip = tk.StringVar()

        # Show splash screen and scan network for available connections.
        self.withdraw()
        splash = Splash(self)
        for pc in selector_tools.scan(self.ip_address):
            splash.update_progress(f'Scanning {pc["ip"]}')
            if pc['alive']:
                self.available_connections[pc['name']] = {'ip':pc['ip'], 'port':pc['port']}
        splash.destroy()
        self.deiconify()

        # Build and pack the frames.
        root_frame = tk.Frame(self)
        root_frame.pack(fill='both', padx=2, pady=2)
        selection_frame = tk.Frame(root_frame)
        selection_frame.pack(side='left', expand=True, padx=2, pady=2)
        button_frame = tk.Frame(root_frame)
        button_frame.pack(anchor=tk.NE, side='right', expand=True, padx=2, pady=2)

        # Build and pack the selection frame widgets.
        tk.Label(selection_frame, text='Select a connection:').pack()
        listbox = tk.Listbox(selection_frame, listvariable=self.listbox_list)
        listbox.pack(side='left', expand=True, padx=2, pady=2)
        listbox.bind('<<ListboxSelect>>', self.update_label_text)
        scrollbar = tk.Scrollbar(selection_frame)
        scrollbar.pack(side='left', fill=tk.Y)

        # Build and pack the button frame widgets.
        tk.Label(button_frame, text='Target Hostname:').pack()
        tk.Label(button_frame, textvariable=self.target_hostname).pack()
        tk.Label(button_frame, text='Target IP').pack()
        tk.Label(button_frame, textvariable=self.target_ip).pack()
        tk.Button(button_frame, text='Connect', command=self.connect).pack()

        # Widget config settings.
        self.listbox_list.set([key for key in self.available_connections.keys()])
        scrollbar.config(command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)
    
    def update_label_text(self, event):
        selected_target = event.widget.get(event.widget.curselection())
        self.target_hostname.set(selected_target)
        self.target_ip.set(self.available_connections[selected_target]['ip'])
    
    def connect(self):
        selector_tools.launch_viewer(self.target_hostname.get())


if __name__ == '__main__':
    app = App()
    app.mainloop()