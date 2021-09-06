# vnc-selector

## Table of contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)

## General Info
A simple GUI for managing and connecting to Tight VNC servers on a LAN.

## Technologies
This project was developed and tested using **Python 3.9.2** running on **Windows 10**, and with **TightVNC Version 2.6.59**. Refer to the **requirements.txt** for python dependencies.

## Setup
To run VNC Selector:
1. Download [TightVNC](https://www.tightvnc.com/) and install it at *C:\Program Files\TightVNC*.
2. Clone this repo, then navigate to the installation folder using Window Command Line.
3. Run the command `pip install requirements.txt`.
4. Launch **VNC_Selector.pyw**.

## Features
* **Add Connection** - Manually add a connection using a known Hostname and/or IP address. 
* **Scan Network** - Scan the LAN for available TightVNC servers, then add them to your list of known connections.
* **Edit Connection** - Modify the properties of a known connection.
* **Delete Connection** - Removes a connection from your list of known connections.
* **Settings**
  * **Refresh known server status** - Enable or disable the auto scan feature which updates known connection availability status.
  * **Close app after connecting** - Enable or disable feature which closes VNC Selector after connecting.
