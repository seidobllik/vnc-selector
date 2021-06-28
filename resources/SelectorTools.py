'''
Library of functions used by the VNC selector GUI.
'''

import os
import socket
import pathlib
import pickle

DATA_FILE = 'resources\\data.dat'

def launch_viewer(target:str, password:str='', port=5900):
    '''
    Launches Tight VNC viewer using the provided host name, optional password and port.

    args:
      target (str):  Hostname or IP of the target PC.
      password (str):  Password of the target PC TightVNC server.
      port (int):  Port number of the target PC TightVNC server. (default 5900)
    '''
    vnc_viewer_path = 'C:\\"Program Files"\\TightVNC\\tvnviewer.exe'
    command = f'cmd /c start {vnc_viewer_path} {target}:{port}'
    if password != '':
        command += f' -password={password}'
    try:
        os.system(command)
    except Exception as e:
        raise e

def get_this_pc_info():
    '''
    Function that provides the PC hostname and IP address.\n
    Returns a {'name': str, 'ip': str} dictionary.
    '''
    try:
        hostname = socket.gethostname()
        ipaddress = socket.gethostbyname(hostname)
    except Exception as e:
        raise e

    return {'name':hostname, 'ip':ipaddress}

def is_alive(address:str, port:int=5900):
    '''
    Attempts to connect to a given IP address and port.\n
    Returns True if connection is successful, otherwise returns False.

    args:
        address (str):  IP address of the target PC. Can also be hostname.
        port (int):  Port which the Tight VNC service is broadcasting.
    '''
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(0.25)
    result = None
    try:
        result = s.connect_ex((address,port))
    except socket.error as e:
        print(e)
    finally:
        s.close()
    if result == 0:
        # connection is alive.
        return True
    else:
        return False

def scan(address:str=get_this_pc_info()['ip'], port:int=5900, address_range:tuple=(2, 255)):
    '''
    Generator.\n
    Scans the LAN for any PCs running a Tight VNC server (on default port 5900).\n
    Yields a {'name': str, 'ip': str, 'port': int, 'alive': bool} dictionary for each PC running a Tight VNC server.

    args:
      address (str):  An IP address that is on the network you'd like to scan. Default to host machine ip.
      port (int):  Port which the Tight VNC service is broadcasting.
      address_range (tuple):  The address range to scan. e.g., (100, 120) results in the range 
                      of 192.168.0.100 to 192.168.0.119.
    '''

    socket.setdefaulttimeout(0.25)
    network = '.'.join(address.split('.')[0:-1])
    network += '.'
    for i in range(address_range[0], address_range[1]):
        name = ''
        address_to_scan = network + str(i)
        alive = False
        if is_alive(address_to_scan, port):
            try:
                name = socket.gethostbyaddr(address_to_scan)[0]
                alive = True
            except Exception as e:
                raise e
        yield {'name':name, 'ip':address_to_scan, 'port':port, 'alive': alive}

def get_connections_from_file(file):
    '''
    Returns connections dict from the provided file.

    args:
      file (str):  The file path and name. 
    '''
    if not pathlib.Path(file).is_file():
        with open(file, 'wb') as f:
            pickle.dump({}, f)
    with open(file, 'rb') as f:
        data = pickle.load(f)
    for key in data.keys():
        data[key]['is alive'] = False
    return data

def save_connections_to_file(data, file):
    '''
    Saves the provided connections to the provided file.

    args:
      data (dict):  The connections dict to save.
      file (str):  The file path and name to save the data to.
    '''
    with open(file, 'wb') as f:
        pickle.dump(data, f)
