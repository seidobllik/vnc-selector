import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import Button, messagebox
from PIL import ImageTk
import webbrowser
import resources.SelectorTools as SelectorTools

DATA_FILE = SelectorTools.DATA_FILE


class Hyperlink(tk.Label):
    
    def __init__(self, parent, text, target=None):
        '''
        Inherits from tk.Label. Enables the label to act as a hyperlink, and open a 
        web browser page to the provided target, or text value. 

        args:
          parent (tk.Frame):  The parent frame of this label.
          text (str):  The text to display in the label. Acts as the url if target is not provided.
          target (str):  The url to open when the label is clicked. (default None)
        '''
        
        tk.Label.__init__(self, parent, text=text)
        self.text = text
        self.target = target or text
        self.font = tkFont.Font(self, self.cget('font'))
        self.font.config(underline=False)
        self.config(fg='blue', font=self.font)
        self.bind('<Button-1>', self.open)
        self.bind('<Enter>', self.enter)
        self.bind('<Leave>', self.leave)
    
    def open(self, event):
        webbrowser.open_new(self.target)

    def enter(self, event):
        self.font.config(underline=True)
        self.config(fg='red', font=self.font)

    def leave(self, event):
        self.font.config(underline=False)
        self.config(fg='blue', font=self.font)


class Tooltip(object):

    def __init__(self, widget, text='widget info'):
        '''
        Creates a tooltip for a provided widget using a tk.Toplevel window with no title bar. 

        args:
          widget (tk widget):  The widget for which the tooltip will appear.
          text (str):  The text to display in the tooltip.
        '''
        self.widget = widget
        self.text = text
        self.widget.bind('<Enter>', self.enter)
        self.widget.bind('<Leave>', self.close)

    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty()
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f'+{x}+{y}')
        label = tk.Label(self.tw, text=self.text, justify=tk.LEFT, relief=tk.SOLID, borderwidth=1, background='white')
        label.pack(ipadx=1)
    
    def close(self, event=None):
        if self.tw:
            self.tw.destroy()


class About(tk.Toplevel):
    '''
    Displays the About info for VNC Selector.
    '''
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title('About')
        self._info_image = ImageTk.PhotoImage(file='resources\\info.png')
        self.resizable(False, False)
        x = int(parent.winfo_screenwidth()/2.5)
        y = int(parent.winfo_screenheight()/2.5)
        self.geometry(f'+{x}+{y}')
        self.grab_set()
        self.create_widgets()
        
    def create_widgets(self):
        root_frame = tk.Frame(self)
        root_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        text_frame = tk.Frame(root_frame)
        text_frame.pack(side=tk.LEFT)
        image_frame = tk.Frame(root_frame)
        image_frame.pack(side=tk.RIGHT)
        info = ['VNC Selector', 'Version 2.0', 'Built by Tom Baker']
        for s in info:
            tk.Label(text_frame, text=s).pack(anchor=tk.NW)
        link = Hyperlink(text_frame, text='See the project on GitHub', target='https://github.com/seidobllik/vnc-selector')
        link.pack(anchor=tk.NW)
        canvas = tk.Canvas(image_frame, width=120, height=120)
        canvas.pack(fill=tk.BOTH)
        canvas.create_image(62, 62, image=self._info_image)
        tk.Button(image_frame, text='Close', command=self.destroy, width=10).pack()


class AddConnection(tk.Toplevel):
    '''
    Displays the input window for the user to provide info for the new connection.
    '''
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title('Add Connection')
        self.resizable(False, False)
        x = int(parent.winfo_screenwidth()/2.5)
        y = int(parent.winfo_screenheight()/2.5)
        self.geometry(f'+{x}+{y}')

        # Instance variables.
        self._hostname_entry = None
        self._ip_entry = None
        self._connection_entry = None
        self._password_entry = None
        self._port_entry = None

        self.grab_set()
        self.create_widgets()
        
    def create_widgets(self):
        # Create and pack the frames.
        root_frame = tk.Frame(self)
        root_frame.pack(fill=tk.BOTH, padx=2, pady=2)
        entry_frame = tk.Frame(root_frame)
        entry_frame.pack()
        required_frame = tk.LabelFrame(entry_frame, text='Require at least one')
        required_frame.pack(side=tk.LEFT, anchor=tk.NW, padx=2, pady=2, ipadx=2, ipady=2)
        optional_frame = tk.LabelFrame(entry_frame, text='Optional')
        optional_frame.pack(side=tk.RIGHT, anchor=tk.NW, padx=2, pady=2, ipadx=2, ipady=2)
        button_frame = tk.Frame(root_frame)
        button_frame.pack(padx=2, pady=2, ipadx=2, ipady=2)

        # Create and pack the widgets.
        tk.Label(required_frame, text='Hostname').pack(anchor=tk.NW)
        self._hostname_entry = tk.Entry(required_frame, width=20)
        self._hostname_entry.pack(anchor=tk.NW)
        tk.Label(required_frame, text='IP Address').pack(anchor=tk.NW)
        self._ip_entry = tk.Entry(required_frame, width=20)
        self._ip_entry.pack(anchor=tk.NW)
        tk.Label(optional_frame, text='Connection Name').pack(anchor=tk.NW)
        self._connection_entry = tk.Entry(optional_frame, width=20)
        self._connection_entry.pack(anchor=tk.NW)
        tk.Label(optional_frame, text='VNC Server Password').pack(anchor=tk.NW)
        self._password_entry = tk.Entry(optional_frame, width=20)
        self._password_entry.pack(anchor=tk.NW)
        tk.Label(optional_frame, text='VNC Server Port').pack(anchor=tk.NW)
        self._port_entry = tk.Entry(optional_frame, width=20, textvariable=tk.StringVar(self, '5900'))
        self._port_entry.pack(anchor=tk.NW)
        tk.Button(button_frame, text='Add', width=10, command=self.add).pack(side=tk.LEFT)
        tk.Button(button_frame, text='Cancel', width=10, command=self.destroy).pack(side=tk.RIGHT)

    def add(self):
        hostname = self._hostname_entry.get()
        ip = self._ip_entry.get()
        connection = self._connection_entry.get()
        password = self._password_entry.get()
        port = self._port_entry.get() or '5900'

        if hostname == '' and ip == '':
            messagebox.showerror('Add Connection Error', 'Failed to add connection. You must include either a Hostname or an IP Address.')
            return
        if connection == '': 
            connection = hostname or ip
        if port == '':
            port = '5900'
        available_connections = SelectorTools.get_connections_from_file(DATA_FILE)
        if connection in available_connections.keys():
            messagebox.showerror('Add Connection Error', 'Failed to add connection. A connection with that name already exists.')
            return
        available_connections[connection] = {
            'hostname': hostname, 
            'ip address': ip, 
            'vnc password': password, 
            'vnc port': port,
            'is alive': False}
        SelectorTools.save_connections_to_file(available_connections, DATA_FILE)
        self.destroy()


class DeleteConnection(object):
    '''
    Displays the messagebox for the user to confirm a connection deletion request.
    '''
    def __init__(self, connection):
        self.title = 'Delete Connection'
        self.message = f'Are you sure you want to delete the connection:\n{connection} ?'
        self._connection = connection
        self._selection = None
        self.show()

    def show(self):
        self._selection = messagebox.askyesno(self.title, self.message)
        if self._selection:
            available_connections = SelectorTools.get_connections_from_file(DATA_FILE)
            del available_connections[self._connection]
            SelectorTools.save_connections_to_file(available_connections, DATA_FILE)


class ScanNetwork(tk.Toplevel):
    '''
    Displays the window to configure and start a network scan, and then select and discovered
    connections to add them to the available connections list.
    '''
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title('Scan Network')
        self.resizable(False, False)
        x = int(parent.winfo_screenwidth()/2.5)
        y = int(parent.winfo_screenheight()/2.5)
        self.geometry(f'+{x}+{y}')

        # Instance Variables.
        self._this_pc = SelectorTools.get_this_pc_info()
        self._known_connections = SelectorTools.get_connections_from_file(DATA_FILE)
        self._connections_found = tk.StringVar()
        self._connections_found.set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'asdfasdf', 'qwerqwer', 'zxvczxvczxvc'])
        self._host_ip = tk.StringVar()
        self._host_ip.set('.'.join(self._this_pc['ip'].split('.')[:-1]) + '.')
        self._start_ip = tk.StringVar(self, '1')
        self._end_ip = tk.StringVar(self, '255')
        self._progress_bar = None  # Assigned to ttk.Progressbar in create_widgets().
        self._progress_text = tk.StringVar()

        self.grab_set()
        self.create_widgets()
        
    def create_widgets(self):
        '''
        The list of discovered connections should omit the current machine as well as any already known connections.
        '''

        # Build and pack the frames.
        root_frame = tk.Frame(self)
        root_frame.pack(fill=tk.BOTH, padx=2, pady=2)
        settings_frame = tk.Frame(root_frame)
        settings_frame.pack(fill=tk.BOTH, side=tk.LEFT, anchor=tk.NW, padx=2, pady=2)
        scan_frame = tk.Frame(root_frame)
        scan_frame.pack(fill=tk.BOTH, side=tk.RIGHT, anchor=tk.NE, padx=2, pady=2)
        progress_frame = tk.Frame(settings_frame)  # Packed with the progress frame widgets.

        # Build and pack the settings frame widgets.
        tk.Label(settings_frame, text='Scan IP Addresses', justify=tk.LEFT).pack(anchor=tk.NW)
        ip_subframe = tk.Frame(settings_frame)
        ip_subframe.pack(anchor=tk.NW)
        tk.Label(ip_subframe, textvariable=self._host_ip, justify=tk.LEFT).pack(side=tk.LEFT, anchor=tk.NW)
        tk.Entry(ip_subframe, textvariable=self._start_ip, justify=tk.RIGHT, width=3).pack(side=tk.LEFT, anchor=tk.NW)
        tk.Label(ip_subframe, text='thru').pack(side=tk.LEFT, anchor=tk.NW)
        tk.Entry(ip_subframe, textvariable=self._end_ip, justify=tk.RIGHT, width=3).pack(side=tk.LEFT, anchor=tk.NW)
        tk.Button(settings_frame, text='Start Scan', command=None).pack(anchor=tk.NE)

        # Build and pack the scan frame widgets.
        tk.Label(scan_frame, text='Available to Add:', justify=tk.LEFT).pack(anchor=tk.NW)
        list_subframe = tk.Frame(scan_frame)
        list_subframe.pack(anchor=tk.NW)
        listbox = tk.Listbox(list_subframe, listvariable=self._connections_found, selectmode=tk.MULTIPLE, height=6)
        listbox.pack(side=tk.LEFT, anchor=tk.NW)
        scrollbar = tk.Scrollbar(list_subframe)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT, anchor=tk.NE)
        button_subframe = tk.Frame(scan_frame)
        button_subframe.pack(anchor=tk.NW)
        tk.Button(button_subframe, text='Add Selected', command=None).pack(side=tk.LEFT, anchor=tk.W)
        tk.Button(button_subframe, text='Close', command=self.destroy).pack(side=tk.RIGHT, anchor=tk.E, padx=(5, 0))

        # Build and pack the progress frame widgets.
        progress_frame.pack(side=tk.BOTTOM, anchor=tk.SE, padx=2, pady=2)
        self._progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', mode='determinate', length=120)
        self._progress_bar.pack(fill=tk.X, anchor=tk.S)
        tk.Label(progress_frame, textvariable=self._progress_text).pack(anchor=tk.S)

        # Widget config settings.
        scrollbar.config(command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)