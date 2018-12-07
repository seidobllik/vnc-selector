import json, os, subprocess

def chooseComputer():
    computers = loadComputers()
    while True:
        try:
            print("Choose a computer")
            for item in computers:
                print(list(computers.keys()).index(item), ": ", item)
            selection = input("> ")
            if selection in computers:
                new_selection = list(computers.keys()).index(selection)
                selection = new_selection
            elif (selection.isdigit() and
                  int(selection) in range(len(list(computers.keys())))):
                pass
            else:
                raise KeyError(selection)
            
            print("---------")
            print("IP Address: {}\t".format(computers[list(computers.keys())[int(selection)]][0]))
            print("Hostname: {}\t".format(list(computers.keys())[int(selection)]))
            print("Viewer PW: {}\t".format(computers[list(computers.keys())[int(selection)]][1]))
            print("---------")
            return computers[list(computers.keys())[int(selection)]]
            
        except (KeyError, IndexError, ValueError) as err:
            print("Invalid Selection - ", err)
            continue

def getInfo(hostname):
    computers = loadComputers()
    try:
        if hostname in list(computers.keys()):
            return computers[hostname]
        else:
            raise KeyError(hostname)
    except (KeyError) as err:
        print("KeyError: ", err)
        return ['','']
    

def addComputer():
    computers = loadComputers()
    new_name = input("Enter new computer name: ")
    new_ip = input("Enter new IP address: ")
    new_pw = input("Enter new viewer password:")
    computers.update({new_name:[new_ip, new_pw]})
    with open('computers-list.json', 'w') as f:
        json.dump(computers, f)
    print(new_name, " added!")

def addComputer(name, ip, pw):
    computers = loadComputers()
    computers.update({name:[ip, pw]})
    with open('computers-list.json', 'w') as f:
        json.dump(computers, f)
    print(name, " added!")

def removeComputer():
    computer_to_del = chooseComputer()
    computers = loadComputers()
    name = (list(computers.keys())[list(computers.values()).index(computer_to_del)])
    del computers[name]
    with open("computers-list.json", 'w') as f:
        json.dump(computers, f)
    print(name, " removed!")

def removeComputer(computer_to_del):
    print(computer_to_del)
    computers = loadComputers()
    del computers[computer_to_del]
    with open("computers-list.json", 'w') as f:
        json.dump(computers, f)
    print(computer_to_del, " removed!")

def loadComputers():
    with open('computers-list.json') as f:
        dictionary = json.load(f)
    return dictionary

def launchViewer(computerInfo):
    batch_code = "@ECHO OFF\ncd C:\Program Files\TightVNC && start tvnviewer {}::5901 -password={}".format(computerInfo[0], computerInfo[1])
    with open('temp-bat.bat', 'w') as f:
        f.write(batch_code)
    os.system("temp-bat.bat")
    os.remove('temp-bat.bat')

def launchSSH(computerInfo):
    batch_code = "@ECHO OFF\nssh pi@{}".format(computerInfo[0])
    with open('temp-bat.bat', 'w') as f:
        f.write(batch_code)
##    os.system("python3 batch.py")
##    os.system("temp-bat.bat")
    subprocess.call("temp-bat.bat")
    os.remove("temp-bat.bat")
    

##while True:
##    print("~-Menu-~")
##    print("0: Connect")
##    print("1: Add Computer")
##    print("2: Remove Computer")
##    print("3: SSH")
##    print("Q: Quit")
##    selection = input("> ").lower()
##
##    if selection == '0' or selection == 'connect':
##        computer = chooseComputer()
##        launchViewer(computer)
####        break
##    elif selection == '1' or selection == 'add' or selection == 'add computer':
##        addComputer()
##    elif selection == '2' or selection == 'remove' or selection == 'remove computer':
##        removeComputer()
##    elif selection == '3' or selection == 'ssh':
##        computer = chooseComputer()
##        launchSSH(computer)
##    elif selection == 'q' or selection == 'quit':
##        break
##    else:
##        print("Invalid Selection")
