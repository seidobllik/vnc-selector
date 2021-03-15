'''
Library of functions used by the VNC selector GUI.
'''

import os
import socket

def launch_viewer(host_name:str, password:str=''):
    '''
    Launches Tight VNC viewer using the provided host name, and optional password.

    args:
      host_name:  Host name of the target PC.
      password:  Password of the target PC TightVNC server.
    '''
    vnc_viewer_path = 'C:\\"Program Files"\\TightVNC\\tvnviewer.exe'
    command = f'cmd /c start {vnc_viewer_path} -host={host_name}'
    if password != '':
        command += f' -password={password}'
    try:
        os.system(command)
    except Exception as e:
        raise e

def scan(address:str, port:int=5900, address_range:tuple=(100, 120)):
    '''
    Generator.\n
    Scans the LAN for any PCs running a Tight VNC server (on default port 5900).\n
    Yields a {'name', 'ip', 'port', 'alive'} dictionary for each PC running a Tight VNC server.

    args:
      address:  An IP address that is on the network you'd like to scan.
      port:  Port which the Tight VNC service is broadcasting.
      address_range:  The address range to scan. e.g., (100, 120) results in the range 
                      of 192.168.0.100 to 192.168.0.120.
    '''

    def is_alive(address, port):
        '''
        Helper function for scan().\n
        Connects a given IP address and port.\n
        Returns True if connection is alive, otherwise returns False.

        args:
          address:  IP address of the target PC.
          port:  Port which the Tight VNC service is broadcasting.
        '''
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(.25)  # Seconds.
        try:
            result = s.connect_ex( (address,port) )
        except Exception as e:
            raise e
        if result == 0:
            # connection is alive.
            return True
        else:
            return False

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

def get_this_pc_info():
    '''
    Function that provides the PC hostname and IP address.\n
    Returns a {'name', 'ip'} dictionary.
    '''
    try:
        hostname = socket.gethostname()
        ipaddress = socket.gethostbyname(hostname)
    except Exception as e:
        raise e

    return {'name':hostname, 'ip':ipaddress}
