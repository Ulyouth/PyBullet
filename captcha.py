# -*- coding: utf-8 -*-

"""
NAME:    captcha.py
AUTHOR:  andre798
VERSION: 1.0.0
DATE:    15.10.2020 
DESC:    A class for captcha decoding using 2Captcha API. 
"""

import time
import requests as rq
from chkutils import ChkUtils

class Captcha(ChkUtils):
    def solveCaptcha(self, ss, test, data, name, log_id, *args, **kwargs):
        # Check if timeout was set
        tout = kwargs.get('timeout', 120)
        ss2 = ss
        
        # Check if 'ss' is a 'requests' object. If yes, use the current
        # session, otherwise create a new.
        if not isinstance(ss, rq.sessions.Session):
            ss2 = rq.session()
          
        # Request a response in JSON format
        data.update({'json':1})
        
        # Send a request to solve the captcha
        lnk = 'https://2captcha.com/in.php'
    
        r = self.postnlog(ss2, lnk, '2captcha_in.htm', name, log_id, 
                          data = data, timeout = tout) 

        if not self.isJSON(r.text): 
            return [0, 'Response in non-JSON format']
        
        rjs = r.json()
        status = rjs['status']
        req = rjs['request']
        
        if status != 1:
            return [status, req]
        
        if test == 1:
            print('> request: ' + req)

        # Give some time for the captcha to be solved  
        time.sleep(20)
    
        # Obtain the captcha's solution token
        lnk = 'https://2captcha.com/res.php?key=' + data['key'] +\
            '&json=1&action=get&id=' + req

        if test == 1:
            print('> Waiting for captcha response...')
        
        while True:
            r = self.getnlog(ss2, lnk, '2captcha_res.htm', name, log_id, 
                             timeout = tout)

            if not self.isJSON(r.text): 
                return [0, 'Response in non-JSON format']
            
            rjs = r.json()
            status = rjs['status']
            req = rjs['request']
            
            # Check if captcha is ready
            if status == 1:
                return [status, req]
            else:
                if req == 'CAPCHA_NOT_READY':
                    time.sleep(5)
                elif req == 'ERROR_NO_SLOT_AVAILABLE':
                    time.sleep(3)
                else:
                    return [status, req]