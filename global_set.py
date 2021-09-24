# *************************************************************************************************
# Routine: Modify the .seiscomp3/global.cfg file for a specific server (13, 58, 222, 232 - default)
# 
# Emmanuel Guzman Vitola 
# emguzmanvi@unal.edu.co - eguzmanv@sgc.gov.co
# 2021-09-24
# *************************************************************************************************

# *** Useful libreries ***
import os
import sys

try:
    server = sys.argv[1]                                           # input server
except:
    print('Error: The possible inputs are: "13", "58", "222" or "232" - "default".\nExample: global_set 13')
    sys.exit()

cwd = os.getcwd()                                                  # full path of the current directory

# *** Condition: inside or outside of /home/username directory ***
if '/home/' in cwd:                                                # inside /home/user directory
    
    # --- Find the user name using the full path from os.getcwd() ---
    slash_index = [i for i, x in enumerate(cwd) if x == '/']       # list of indices of '/' symbol
    
        # Condition: /home/username or /home/username/directory1/...
    if len(slash_index) == 2:                                      # example: /home/username                                  
        user = cwd[slash_index[1] + 1:]
    else:
        user = cwd[slash_index[1] + 1 : slash_index[2]]            # example: /home/username/directory1/...
        
    cmd = 'scolv -u ' + user + ' --debug'                          # Linux command to open the scolv module
    
    # --- Read the global.cfg lines ---
    file_path = '/home/' + user + '/.seiscomp3/global.cfg'         # File path: /home/username/.seiscomp3/global.cfg
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # --- Useful functions ---
        # Uncomment the desired server in the global.cfg file
    def set_server(server, lines):
        for i in range(0, len(lines)):
            if server in lines[i]:
                if lines[i][0] == '#':
                    lines[i] = lines[i][1:]
        
        # Set the global.cfg as default (all servers commented)
    def default(lines):
        for i in range(0, len(lines)):
            # Condition: comment servers 13 and 58 
            if '10.100.100.13' in lines[i] or '10.100.100.58' in lines[i] or '10.100.100.222' in lines[i]:
                if lines[i][0] != '#':
                    lines[i] = '#' + lines[i]
        
        # Overwrite the global.cfg file with the changes
    def overwrite(file_path, lines):
        file = open(file_path, 'w')
        file.writelines(lines)
        file.close()

    # --- Set the desired server (13, 58, 222, or default - 232) ---
        # Condition: server 10.100.100.13
    if server == '13':
    
        default(lines)                                             # set the global.cfg as default
        set_server('10.100.100.13', lines)                         # set 10.100.100.13          
        overwrite(file_path, lines)                                # overwrite the global.cfg file with the changes
        
        # Condition: server 10.100.100.58
    elif server == '58':
    
        default(lines)                                             # set the global.cfg as default (10.100.100.232)
        set_server('10.100.100.58', lines)                         # set 10.100.100.58          
        overwrite(file_path, lines)                                # overwrite the global.cfg file with the changes
        os.system(cmd)
    
        # Condition: server 10.100.100.222
    elif server == '222':
    
        default(lines)                                             # set the global.cfg as default (10.100.100.232)
        set_server('10.100.100.222', lines)                        # set 10.100.100.222          
        overwrite(file_path, lines)                                # overwrite the global.cfg file with the changes
            
        # Condition: default - server 10.100.100.232
    elif server == 'default' or server == '232':
    
        default(lines)                                             # set the global.cfg as default (10.100.100.232)
        overwrite(file_path, lines)                                # overwrite the global.cfg file with the changes
    
    else:
        print('Error: The possible inputs are: "13", "58", "222" or "232" - "default".')
    
else:
    print('Error: You must be inside of /home/')
    
