# *************************************************************************************************
# Routine: Modify the .seiscomp3/global.cfg file for a specific server (13, 50, 58, 222, 232 - default)
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
    print('Error: The possible inputs are: "13", "58", "50", "222" or "232" - "default".\nExample: global_set 13')
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
        # Set the global.cfg as default (all servers commented)
    def default(lines):
        for i in range(0, len(lines)):
            # Condition: comment all servers
            if 'xx.xxx.xxx' in lines[i]:
                if lines[i][0] != '#':
                    lines[i] = '#' + lines[i]
        
        # Uncomment the desired server in the global.cfg file
    def set_server(server, lines):
        n_server = 0
        n_58 = 0
        for i in range(0, len(lines)):
            # Condition: the server exists in the global.cfg
            if server in lines[i]:
                n_server =+ 1
                if lines[i][0] == '#':
                    lines[i] = lines[i][1:]
                
                # Condition: server 58 with 2 lines or 3 lines commented
                    # Note: some global.cfg files contain 2 lines and others 3 lines for the server 58, where in some cases the 3th line is associated with the server 232.
                if server == 'xx.xxx.xxx.58' and n_58 < 2:
                    n_58 =+ 1
                    # Condition: if the 3th line exists, maybe it can be associated with the server 232
                    if 'xx.xxx.xxx.232' in lines[i + 1]:
                        if lines[i + 1][0] == '#':
                            lines[i + 1] = lines[i + 1][1:]
            
            # Condition: the server doesn't exists in the global.cfg
            elif i + 1 == len(lines) and n_server == 0:
                print("The global.cfg does not have the server: " + server)
                sys.exit()

        # Overwrite the global.cfg file with the changes
    def overwrite(file_path, lines):
        file = open(file_path, 'w')
        file.writelines(lines)
        file.close()

    # --- Set the desired server (13, 58, 222, or default - 232) ---
        # Condition: server xx.xxx.xxx.13
    if server == '13':
    
        default(lines)                                             # set the global.cfg as default
        set_server('xx.xxx.xxx.13', lines)                         # set xx.xxx.xxx.13          
        overwrite(file_path, lines)                                # overwrite the global.cfg file with the changes
        
        # Condition: server xx.xxx.xxx.50
    elif server == '50':
    
        default(lines)                                             # set the global.cfg as default (xx.xxx.xxx.232)
        set_server('xx.xxx.xxx.50', lines)                         # set xx.xxx.xxx.50
        overwrite(file_path, lines)                                # overwrite the global.cfg file with the changes    
    
        # Condition: server xx.xxx.xxx.58
    elif server == '58':
    
        default(lines)                                             # set the global.cfg as default (xx.xxx.xxx.232)
        set_server('xx.xxx.xxx.58', lines)                         # set xx.xxx.xxx.58
        overwrite(file_path, lines)                                # overwrite the global.cfg file with the changes
        os.system(cmd)                                             # Run the scolv

        # Condition: server xx.xxx.xxx.222
    elif server == '222':
    
        default(lines)                                             # set the global.cfg as default (xx.xxx.xxx.232)
        set_server('xx.xxx.xxx.222', lines)                        # set xx.xxx.xxx.222          
        overwrite(file_path, lines)                                # overwrite the global.cfg file with the changes
            
        # Condition: default - server xx.xxx.xxx.232
    elif server == 'default' or server == '232':
    
        default(lines)                                             # set the global.cfg as default (xx.xxx.xxx.232)
        overwrite(file_path, lines)                                # overwrite the global.cfg file with the changes
    
    else:
        print('Error: The possible inputs are: "13", "50", "58", "222" or "232" - "default".')
    
else:
    print('Error: You must be inside of /home/')  
    
