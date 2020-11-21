# -*- coding: utf-8 -*-

"""
NAME:    pybullet.py
AUTHOR:  Ulyouth
VERSION: 1.0.0
DATE:    15.10.2020 
DESC:    A framework to extract data from lists and query their status on 
         websites using third-party scripts.
USAGE:   pybullet.py [CSV] [SCR]
         Where:
         CSV  is a .csv file containing the script's parameters. Syntax below.
         SCR  is the path of the script to be executed.
        
         The syntax of the CSV file is:
             [path  lib  test  ss_rst  list_rst  threads  list_wait  err_wait  
              list  delim  align  agents  ua_mtd  proxy  px_mtd  captcha  
              alert]
         Where:
         path       The script's path.
         lib        Module to be used. Can be blank or the following options:
                    ['socks', 'requests', 'chrome' or 'firefox']
         test       Toogles test mode. [0=off; 1=on]
         ss_rst     Toogles session reset between list items. [0=off; 1=on]
         list_rst   Toogles list repetition when done. [0=off; 1=on]
         threads    Number of threads to run in parallel.
         list_wait  Time (in s) to wait between every list item.
         err_wait   Time (in s) to wait after an error occurs.
         list       File containing the list to be checked.
         delim      List's delimiter
         align      Number elements in every list item.
         agents     File containing a list of User-Agents.
         ua_mtd     How User-Agents should be selected. Options:
                    ['list' or 'random']
         proxy      File containing a list of proxies. Format: 
                    <protocol>://<ip>:<port> 
         px_mtd     How proxies should be selected. Same options as 'ua_mtd'.
         captcha    A 2Captcha API key.
         alert      A sound file to be played when a match is found.
"""

import time, sys, os.path
import pandas as pd
from requests.exceptions import RequestException
from selenium.common.exceptions import WebDriverException
from random import seed, randint
from threading import Thread
from chkutils import ChkUtils
from qlist import QList

# Handler function for working threads
def chkThreadProc(args):
    try:
        [ss, x, i, test, rst, captcha, data] = args[:]
        
        [r, log] = chkMain(ss, test, rst, captcha, data) 
        return [r, log, x, i]
    except RequestException:
        return [-100, 'Connection problems', x, i]
    except WebDriverException:
        return [-100, 'Connection problems', x, i]
    except Exception as e:
        return [-200, e, x, i]
            
# Check if all args where passed
if len(sys.argv) < 3:
    print(__doc__)
    sys.exit(0)

# Read the config file
config = pd.read_csv(sys.argv[1])

# Define the name of the procedure to be executed
path = os.path.normpath(sys.argv[2])
name = os.path.basename(path)

# Locate the index of the procedure
i = config[config['path'] == path].index.values[0]

# Load the checker's main function
path = os.path.abspath(path)

if not repr(path) in str(sys.path):
    sys.path.append(path)

f = open(path + '\\' + name + '.py', 'rb')
exec(f.read(), globals())

# Library to be used
lib = str(config['lib'][i]) if not pd.isnull(config['lib'][i]) else ''

# Test mode on or off
test = int(config['test'][i])

# Reset session every new request or not
ss_opt = int(config['ss_rst'][i])

# Reset list from the beginning when done
list_opt = int(config['list_rst'][i])

# Number of threads to run in parallel
tr_count = 1 if test == 1 else int(config['threads'][i])

# Define the wait times and connection's timeout
tlst = int(config['list_wait'][i])
terr = int(config['err_wait'][i])

# Get the lists' filenames
list_file = str(config['list'][i])
list_delim = config['delim'][i]
list_align = int(config['align'][i])
ua_file = str(config['agents'][i])
ua_mtd = str(config['ua_mtd'][i])
proxy_file = str(config['proxy'][i])
proxy_mtd = str(config['px_mtd'][i])

# Use newline as delimiter if none was passed
list_delim = list_delim if list_delim == list_delim else '\n' 

# 2Captcha API Key
captcha = str(config['captcha'][i])

m_data = []
m_uas = []
m_proxy = []

# Log the config info   
rep = '=========================CONFIG INFO========================\n'\
      '> SCRIPT NAME:   ' + name + '\n'\
      '> LIB:           ' + lib + '\n'\
      '> TEST:          ' + ('Yes' if test == 1 else 'No') + '\n'\
      '> SESSION RESET: ' + ('Yes' if ss_opt == 1 else 'No') + '\n'\
      '> LIST RESET:    ' + ('Yes' if list_opt == 1 else 'No') + '\n'\
      '> THREAD COUNT:  ' + str(tr_count) + '\n'\
      '> LIST WAIT:     ' + str(tlst) + 's\n'\
      '> ERROR WAIT:    ' + str(terr) + 's\n'\
      '> LIST NAME:     ' + list_file + '\n'\
      '> LIST DELIM:    ' + ('\\n' if list_delim == '\n' else list_delim) + '\n'\
      '> LIST ALIGN:    ' + str(list_align) + '\n'\
      '> UA LIST:       ' + ua_file + '\n'\
      '> UA METHOD:     ' + ua_mtd + '\n'\
      '> PROXY LIST:    ' + proxy_file + '\n'\
      '> PROXY METHOD:  ' + proxy_mtd + '\n'\
      '> 2CAPTCHA KEY:  ' + captcha + '\n'\
      '============================BEGIN==========================='
end = '\n=============================END============================\n'

chk = ChkUtils()

# Read the checker's list
if chk.readListDelim(list_file, list_delim, list_align, m_data) == 0:
    rep = '> [ERROR] Invalid or empty list to be checked.' + end
    chk.writeLog('log.txt', name, '', rep, 'at')
    print(rep)
    sys.exit(0)

# Read the User-agent's list, if any
if len(ua_file) == 0 or not os.path.isfile(ua_file) or\
    chk.readListDelim(ua_file, '\n', 0, m_uas) == 0:
    m_uas.append('')
    
# Read the proxy list, if any
if len(proxy_file) == 0 or not os.path.isfile(proxy_file) or\
    chk.readListDelim(proxy_file, '\n', 0, m_proxy) == 0:
    m_proxy.append('')

chk.writeLog('log.txt', name, '', rep + '\n', 'wt')

# On the test mode, check only the 1st item in the list
if test == 1:
    del m_data[1::]

# Initialize the lists used in the loop
m_tr = [None] * tr_count
m_ss = [None] * tr_count
q = QList()

# List indexes
x = 0
y = 0
z = 0

for x in range(len(m_data)):
    status = False

    # Loop until there is a free thread slot or until all threads have been
    # processed
    while not status:
        c = 0 # Empty slot counter
        
        for i in range(tr_count):
            rst = 0
                    
            # Check if there is an empty thread slot
            if m_tr[i] == None:
                # Check if EOL was reached
                if x == len(m_data):
                    # Signal that the thread has finished
                    c = c + 1

                    # Check if all threads have already finished
                    if c == tr_count:
                        status = True

                    continue
                
                # Init a new requests session
                if m_ss[i] == None or ss_opt == 1:
                    # Generate a random index for the User-Agent
                    if ua_mtd == 'random':
                        seed()            
                        y = randint(0, len(m_uas)-1)  
            
                    # Generate a random index for the proxy
                    if proxy_mtd == 'random':
                        seed()     
                        z = randint(0, len(m_proxy)-1)
                        
                    m_ss[i] = chk.getSession(lib, m_ss[i], test, 
                                             m_uas[y], m_proxy[z])
                    rst = 1
                
                params = [m_ss[i], x, i, test, rst, captcha, m_data[x]]
                
                # Init the checker's main procedure in a new thread
                m_tr[i] = Thread(target = lambda q, 
                                 arg1: q.put(chkThreadProc(arg1)), 
                                 args=(q, params))
                m_tr[i].start()

                rep = '> BEGIN: i=' + str(i) + ' x=' + str(x) +\
                    ' [' + str(m_data[x]) + ']\n'
                chk.writeLog('log.txt', name, '', rep, 'at')

                if x != len(m_data)-1:
                    # Signal that a new thread was added to the list
                    status = True
                else:
                    # Signal that EOL has been reached
                    x = x + 1
                
                # Restart the loop
                break
            else:
                # If there is already a thread in the current slot,
                # check if it has already returned
                if m_tr[i].is_alive():
                    status == False
                    continue
                
                res = q.get()
                
                if res == None:
                    status == False
                    continue

                [r, log, j, k] = res            

                rep = '> OUTPUT: k=' + str(k) + " j=" + str(j) +\
                    ' [' + str(m_data[j]) + ']\n'
                chk.writeLog('log.txt', name, '', rep, 'at')

                # Check if an error occurred
                if r < 0:
                    # Check if the error is an unhandled exception
                    if r <= -200:
                        rep = '> [EXCEPTION] ' + str(log)
                        chk.writeLog('log.txt', name, '', rep + end, 'at')
                        print(rep)
                        sys.exit(0)
                    else:
                        rep = '> [ERROR ' + str(abs(r)) + '] ' + log
                        chk.writeLog('log.txt', name, '', rep + '\n', 'at')
                        print(rep) 
                        time.sleep(terr)

                    # Check if a new session should be started
                    if r <= -100 or ss_opt == 1:
                        # Generate a random index for the User-Agent
                        if ua_mtd == 'random':
                            seed()            
                            y = randint(0, len(m_uas)-1)  
            
                        # Generate a random index for the proxy
                        if proxy_mtd == 'random':
                            seed()     
                            z = randint(0, len(m_proxy)-1)
                        
                        m_ss[k] = chk.getSession(lib, m_ss[k], test, 
                                                 m_uas[y], m_proxy[z])
                        rst = 1
                    
                    params = [m_ss[k], j, k, test, rst, captcha, m_data[j]]
                    
                    # Restart the procedure in case of error
                    m_tr[k] = Thread(target = lambda q, 
                                     arg1: q.put(chkThreadProc(arg1)), 
                                     args=(q, params))
                    m_tr[k].start()
                    
                    rep = '> RESTART: k=' + str(k) + " j=" + str(j) +\
                        ' [' + str(m_data[j]) + ']\n'
                    chk.writeLog('log.txt', name, '', rep, 'at')
                else: 
                    file = 'log-' + str(r) + '.txt'
                    chk.writeLog('log.txt', name, '', '> ' + log + '\n', 'at')
                    chk.writeLog(file, name, '', log + '\n', 'at')

                    # Print and log the result
                    if r >= 0 and r < 100: # Unknown or not-applicable
                        print('> \x1b[1;33;40m' + log + '\x1b[0m')
                    elif r >= 100 and r < 200: # Good
                        print('> \x1b[1;32;40m' + log + '\x1b[0m')
                    elif r >= 200 and r < 300: # Bad
                        print('> \x1b[1;31;40m' + log + '\x1b[0m')
                    
                    if ss_opt == 1:
                        chk.closeSession(lib, m_ss[k])
                        m_ss[k] = None
                    
                    # Signal that the slot is again empty
                    m_tr[k] = None

        time.sleep(tlst)
    
    # Repeat the list if signaled 
    if list_opt == 1 and x == len(m_data):
        x = -1
    
    # Increment the lists' indexes
    if ua_mtd == 'list': y = y + 1
    if proxy_mtd == 'list': z = z + 1
            
    # Reset the indexes if EOL was reached
    y = 0 if y == len(m_uas) else y
    z = 0 if z == len(m_proxy) else z

chk.writeLog('log.txt', name, '', end, 'at')
