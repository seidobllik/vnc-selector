import tkinter as tk
import resources.Toplevels as Toplevels
import resources.SelectorTools as SelectorTools
from PIL import ImageTk
import threading
import time


class App(tk.Tk):
    '''
    Main VNC Selector application.
    '''
    # Class Variables.
    hostname, ip = SelectorTools.get_this_pc_info().values()

    def __init__(self):
        tk.Tk.__init__(self)
        self.title(f'VNC Selector on [{App.hostname}]')
        x = int(self.winfo_screenwidth()/2.5) - 10
        y = int(self.winfo_screenheight()/2.5) - 10
        self.geometry(f'360x160+{x}+{y}')
        self.resizable(False, False)

        # Instance Variables.
        self._file_menu = None  # Assigned to tk.Menu in create_widgets().
        self._file_menu_index = {
            'Add Connection': 0,
            'Edit Connection': 1,
            'Delete Connection': 2,
            'Scan Network': 3,
            'Settings': 5,
            'Exit': 7
        }
        self._refresh_image = ImageTk.PhotoImage(file='resources\\refresh.png')
        self._green_led = ImageTk.PhotoImage(file='resources\\green.png')
        self._red_led = ImageTk.PhotoImage(file='resources\\red.png')
        self._grey_led = ImageTk.PhotoImage(file='resources\\grey.png')
        self._status_led = None  # Assigned to tk.Canvas in create_widgets().
        self._connect_button = None  # Assigned to tk.Button in create_widgets().
        self._refresh_button = None  # Assigned to tk.Button in create_widgets().
        self._listbox = None  # Assied to tk.Listbox in create_widgets().
        self._listbox_list = tk.StringVar()
        self.target = {
            'connection': tk.StringVar(),
            'hostname': tk.StringVar(),
            'ip address': tk.StringVar()
            }
        self.available_connections = self.get_saved_connections()
        self.settings = self.get_saved_settings()

        # Start the app.
        self._create_widgets()
        self.run_status_thread(True)

    def _create_widgets(self):
        '''
        Build and place all widgets in the main window.
        '''
        # Build the menubar.
        menu = tk.Menu(self)
        self._file_menu = tk.Menu(menu, tearoff=0)
        self._file_menu.add_command(label='Add Connection', command=self.add_connection)
        self._file_menu.add_command(label='Edit Connection', command=self.edit_connection)
        self._file_menu.add_command(label='Delete Connection', command=self.delete_connection)
        self._file_menu.add_command(label='Scan Network', command=self.scan_network)
        self._file_menu.add_separator()
        self._file_menu.add_command(label='Settings', command=self.show_settings)
        self._file_menu.add_separator()
        self._file_menu.add_command(label='Exit', command=self.destroy)
        menu.add_cascade(label='File', menu=self._file_menu)
        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label='About', command=lambda : Toplevels.About(self))
        menu.add_cascade(label='Help', menu=help_menu)
        self._file_menu.entryconfig(self._file_menu_index['Edit Connection'], state='disabled')
        self._file_menu.entryconfig(self._file_menu_index['Delete Connection'], state='disabled')
        # self._file_menu.entryconfig(self._file_menu_index['Settings'], state='disabled')  # Settings disabled until the feature is added.

        # Build and pack the frames.
        root_frame = tk.Frame(self)
        root_frame.pack(fill=tk.BOTH, padx=2, pady=2)
        list_frame = tk.Frame(root_frame)
        list_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=2, pady=2)
        info_frame = tk.Frame(root_frame)
        info_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True, padx=2, pady=2)
        info_frame_subframe = tk.Frame(info_frame)
        info_frame_subframe.pack(fill=tk.X, side=tk.TOP, expand=True)
        button_frame = tk.Frame(info_frame)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, expand=True)

        # Build and pack the list frame widgets.
        tk.Label(list_frame, text='Select a connection:').pack(anchor=tk.NW)
        self._listbox = tk.Listbox(list_frame, listvariable=self._listbox_list)
        self._listbox.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=2, pady=2)
        self._listbox.bind('<<ListboxSelect>>', self.update_info)
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        # Build and pack the info frame widgets.
        tk.Label(info_frame_subframe, text='Connection').pack(fill=tk.X, side=tk.LEFT, padx=(55, 0))
        self._status_led = tk.Canvas(info_frame_subframe, width=19, height=19)
        self._status_led.pack(side=tk.RIGHT)
        self._status_led.create_image(11, 11, image=self._red_led)
        tk.Label(info_frame, textvariable=self.target['connection'], borderwidth=2, relief='sunken').pack(fill=tk.X, expand=True)
        tk.Label(info_frame, text='Target Hostname').pack(fill=tk.X)
        tk.Label(info_frame, textvariable=self.target['hostname'], borderwidth=2, relief='sunken').pack(fill=tk.X, expand=True)
        tk.Label(info_frame, text='Target IP').pack(fill=tk.X)
        tk.Label(info_frame, textvariable=self.target['ip address'], borderwidth=2, relief='sunken').pack(fill=tk.X, expand=True)
        self._refresh_button = tk.Button(button_frame, image=self._refresh_image, compound=tk.LEFT, command=lambda : self.run_status_thread())
        self._refresh_button.pack(side=tk.LEFT)
        Toplevels.Tooltip(self._refresh_button, 'Refresh all servers status')
        self._connect_button = tk.Button(button_frame, text='Connect', command=self.connect)
        self._connect_button.pack(padx=(0, 20))

        # Widget config settings.
        self.config(menu=menu)
        self._listbox_list.set(sorted([key for key in self.available_connections.keys()]))
        scrollbar.config(command=self._listbox.yview)
        self._listbox.config(yscrollcommand=scrollbar.set)
        self._connect_button.config(state='disabled')
        self.update_widget_visibility()
    
    def update_widget_visibility(self):
        '''
        Update widget visibility based on saved settings.

        scan button, led indicator.
        '''
        if self.settings['enable scan']:
            self._refresh_button.config(state='normal')
            self._status_led.config(state='normal')
        else:
            self._refresh_button.config(state='disabled')
            self._status_led.config(state='disabled')
            self._status_led.create_image(11, 11, image=self._grey_led)
            self._connect_button.config(state='normal')

    def update_info(self, event=None):
        '''
        Usually called upon listbox <<ListboxSelect>> event. Updates all of the information displayed for 'Connection', 'Hostname', 'IP Address', and
        enables/disables the Connect button and Delete Connection file menu option.

        args:
          event (tk.Event): <<ListboxSelect>> event. (default None)
        '''
        tk.Event
        try:
            selected_target = self._listbox.get(self._listbox.curselection())
            is_alive = self.available_connections[selected_target]['is alive']
            self.target['connection'].set(selected_target)
            self.target['hostname'].set(self.available_connections[selected_target]['hostname'])
            self.target['ip address'].set(self.available_connections[selected_target]['ip address'])
            self._status_led.create_image(11, 11, image=self._green_led if is_alive else self._red_led)
            self._connect_button.config(state='normal' if is_alive else 'disabled')
            self._file_menu.entryconfig(self._file_menu_index['Edit Connection'], state='normal')
            self._file_menu.entryconfig(self._file_menu_index['Delete Connection'], state='normal')
        except Exception as e:
            self.target['connection'].set('')
            self.target['hostname'].set('')
            self.target['ip address'].set('')
            self._status_led.create_image(11, 11, image=self._red_led)
            self._connect_button.config(state='disabled')
            self._file_menu.entryconfig(self._file_menu_index['Edit Connection'], state='disabled')
            self._file_menu.entryconfig(self._file_menu_index['Delete Connection'], state='disabled')
        self.update_widget_visibility()
        
    def connect(self):
        '''
        Method which calls SelectorTools.launch_viewer, passing it the info for the currently
        selected connection.
        '''
        # the server password should be accessed here.
        connection = self.target['connection'].get()
        hostname = self.available_connections[connection]['hostname']
        ip = self.available_connections[connection]['ip address']
        pwd = self.available_connections[connection]['vnc password']
        port = self.available_connections[connection]['vnc port']
        target = hostname if hostname != '' else ip
        SelectorTools.launch_viewer(target, pwd, port)
        if self.settings['enable close']:
            # self.destroy()
            pass  # TODO: Need to fix this. Destroying the app closes VNC as well.
    
    def get_saved_connections(self):
        '''
        Returns connection dict loaded from the data file.
        '''
        return SelectorTools.get_connections_from_file()
    
    def update_connection_status(self, loop=False):
        '''
        WARNING: Auto-refresh (loop=True) is enabled and started during App init, and should not typically
        be started manually.
        
        Background task, and called when 'refresh' button is pressed. Updates the 'is alive' status of 
        each connection listed, then calls update_info().

        Auto-refresh rate is 60 seconds. 

        args:
          loop (bool):  If True, auto-refresh is enabled. (default False)
        '''
        if self.settings['enable scan']:
            for key in self.available_connections.keys():
                try:
                    if self.available_connections[key]['hostname'] != '':
                        self.available_connections[key]['is alive'] = SelectorTools.is_alive(self.available_connections[key]['hostname'])
                    else:
                        self.available_connections[key]['is alive'] = SelectorTools.is_alive(self.available_connections[key]['ip address'])
                except KeyError as e:
                    # KeyErrors may occur in a loop which was running while the user edits a connection.
                    break
            self.update_info()
            if loop:
                time.sleep(60)
                if self.settings['enable scan']:
                    self.update_connection_status(True)
            else:
                self._refresh_button.config(state='normal')


    def run_status_thread(self, loop=False):
        if not loop:
            self._refresh_button.config(state='disabled')
        status_thread = threading.Thread(target=self.update_connection_status, args=(loop,))
        status_thread.setDaemon(True)
        status_thread.start()

    def add_connection(self):
        '''
        Loads the Add Connection window, then updates all available connections and their status.
        '''
        Toplevels.AddConnection(self).wait_window()
        self.available_connections = self.get_saved_connections()
        self._listbox_list.set(sorted([key for key in self.available_connections.keys()]))
        self._listbox.select_clear(0, tk.END)
        self.update_info()
        self.run_status_thread()

    def edit_connection(self):
        '''
        Loads the Edit Connection window, then updates all available connections and their status.
        '''
        connection = self._listbox.get(self._listbox.curselection()[0])
        Toplevels.EditConnection(self, connection).wait_window()
        self.available_connections = self.get_saved_connections()
        self._listbox_list.set(sorted([key for key in self.available_connections.keys()]))
        self._listbox.select_clear(0, tk.END)
        self.update_info()
        self.run_status_thread()

    def delete_connection(self):
        '''
        Loads the Delete Connection window, then updates all available connections and their status.
        '''
        connection = self._listbox.get(self._listbox.curselection()[0])
        self.bell()
        Toplevels.DeleteConnection(connection)
        self.available_connections = self.get_saved_connections()
        self._listbox_list.set(sorted([key for key in self.available_connections.keys()]))
        self._listbox.select_clear(0, tk.END)
        self.update_info()
        self.run_status_thread()

    def scan_network(self):
        '''
        Loads the Scan Network window, then updates all available connections and their status.
        '''
        Toplevels.ScanNetwork(self).wait_window()
        self.available_connections = self.get_saved_connections()
        self._listbox_list.set(sorted([key for key in self.available_connections.keys()]))
        self._listbox.select_clear(0, tk.END)
        self.update_info()
        self.run_status_thread()

    def show_settings(self):
        '''
        Loads the Settings window, then updates the GUI.
        '''
        Toplevels.ShowSettings(self).wait_window()
        self.settings = self.get_saved_settings()
        self.update_info()
        self.run_status_thread()

    def get_saved_settings(self):
        '''
        Returns connection dict loaded from the data file.
        '''
        return SelectorTools.get_settings_from_file()
