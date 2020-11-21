# -*- coding: utf-8 -*-

"""
NAME:    chkutils.py
AUTHOR:  Ulyouth
VERSION: 1.0.0
DATE:    15.10.2020 
DESC:    A class containing auxiliary tools to be used by pybullet.py and 
         related scripts. 
"""

import os, json, time, socks
import requests as rq
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class ChkUtils:
    def grab(self, s, first, last):
        begin = s.find(first)
        
        if begin == -1:
            return ''
        
        begin = begin + len(first)
        end = s.find(last, begin)
    
        if end == -1:
            return ''
     
        return s[begin:end]

    def graball(self, s, first, last):
        data = []
        begin = 0
    
        while True:
            begin = s.find(first, begin)
        
            if begin == -1:
                break
        
            begin = begin + len(first)
            end = s.find(last, begin)
        
            if end == -1:
                break
        
            data.append(s[begin:end])
            begin = end + len(last)
    
        return data
  
    def writeLog(self, filename, name, log_id, data, mode):
        path = 'logs\\' + name + '\\'
    
        if len(log_id) != 0:
            path = path + log_id + '\\'
        
        os.path.normpath(path)
        
        if not os.path.isdir(path):
            os.makedirs(path)
    
        filename = path + filename      
        size = 0
        
        with open(filename, mode) as f:
            size = f.write(data)
        
        return size
    
    def readListDelim(self, filename, delim, align, m_data):
        j = align
        c = 0
    
        with open(filename) as f:
            # Read one line from the file at a time
            for line in f:
                # Make a list from the line using a character as delimiter
                v_data = line.split(delim)
            
                i = len(v_data) # Real list length
            
                # Delete newlines
                v_data[i-1] = v_data[i-1].replace('\r', '')
                v_data[i-1] = v_data[i-1].replace('\n', '')
            
                # Ignore blank lines
                if len(v_data[0]) == 0:
                    continue
            
                # Check if the list is a vector or matrix
                if delim == '\n':
                    # Case vector, keep it as vector
                    m_data.append(v_data[0])
                else:
                    # Check if only a partial list was passed
                    if i < j:
                        # Complete the rest of the list with blank values
                        for x in range(j-i):
                            v_data.append('') 
        
                    # Append the vector data to the matrix data
                    m_data.append(v_data)
            
                # Line count
                c = c + 1

        return c

    def findExecNWait(self, ss, target, *args, **kwargs):
        find = kwargs.get('find', None)
        cmd = kwargs.get('cmd', None)
        timeout = kwargs.get('timeout', 120)
        wait = kwargs.get('wait', 3)
        
        elm = None
        
        # Get the element object according to search item
        if find == 'id':
            elm = ss.find_element_by_id(target)
        elif find == 'class':
            elm = ss.find_element_by_class(target)
        elif find == 'name':
            elm = ss.find_element_by_name(target)
        elif find == 'tagname':
            elm = ss.find_element_by_tag(target)
        elif find == 'linktxt':
            elm = ss.find_element_by_link_text(target)      

        if elm == None or cmd == None:
            return elm

        # Obtain the current tag id
        old = old = ss.find_element_by_tag_name('html').id
        new = old

        # Perform the requested command
        if cmd == 'click':
            elm.click()
        else:
            return elm
        
        # Wait until the page has completely loaded or until timeout
        while new == old and timeout > 0:
            try:
                new = ss.find_element_by_tag_name('html').id
            except:
                time.sleep(wait)
                timeout = timeout - wait

        return elm
   
    def isJSON(self, s):
        try:
            json.loads(s)
        except: 
            return False
        
        return True
   
    def getUserAgent(self, ss):
        if isinstance(ss, rq.sessions.Session):
            return ss.headers['User-Agent'] if 'User-Agent' in ss.headers\
                else ''  
        elif isinstance(ss, webdriver.chrome.webdriver.WebDriver) or\
            isinstance(ss, webdriver.firefox.webdriver.WebDriver):
            return ss.execute_script('return navigator.userAgent')
        else:
            return ''
 
    def slmToRqCookie(self, cklist):
        ckdict = {}
        
        for cookie in cklist:
            ckdict[cookie['name']] = cookie['value']
        
        return ckdict
   
    def getProxy(self, ss):
        if isinstance(ss, socks.socksocket):
            [px_type, addr, port, rdns, user, pswd] = ss.proxy
            
            if px_type == None or addr == None or port == None:
                return ''
        
            prot = ''
            
            if px_type == socks.SOCKS4: prot = 'socks4'
            elif px_type == socks.SOCKS5: prot = 'socks5'
            else: prot = 'http'           
            
            return '{}://{}:{}'.format(prot, addr, port)
        elif isinstance(ss, rq.sessions.Session):
            return ss.proxies['http'] if 'http' in ss.proxies\
                else ''
        elif isinstance(ss, webdriver.chrome.webdriver.WebDriver) or\
            isinstance(ss, webdriver.firefox.webdriver.WebDriver):      
            return ss.capabilities['proxy']['httpProxy']\
                if 'proxy' in ss.capabilities and\
                    'httpProxy' in ss.capabilities['proxy']\
                        else ''
        else:
            return ''
       
    def parseProxyInfo(self, proxy):
        # <protocol>://<ip>:<port>
        i = proxy.find('://')
        
        if i == -1:
            return ['', '', 0]
        
        j = proxy.find(':', i+3)
        
        if j == -1:
            return ['', '', 0]
        
        return [proxy[0:i], proxy[i+3:j], int(proxy[j+1::])]

    def getSession(self, lib, ss, test, agent, proxy):
        if len(lib) == 0:
            return None
        elif lib == 'socks':
            # Close any previous session
            if ss != None:
                ss.close()
            
            ss = socks.socksocket()
            
            # Set the proxy to be used by the session
            if len(proxy) != 0:
                [prot, ip, port] = self.parseProxyInfo(proxy)
                
                if prot == 'socks4': px_type = socks.SOCKS4
                elif prot == 'socks5': px_type = socks.SOCKS5
                else: px_type = socks.HTTP
                
                ss.set_proxy(px_type, ip, port)
                    
            return ss       
        elif lib == 'requests':
            # Close any previous session
            if ss != None:
                ss.close()
            
            # Init new session
            ss = rq.session()
            
            # Set the default User-Agent for the session
            if len(agent) != 0:
                ss.headers.update({'User-Agent': agent})
            
            # Set the proxy to be used by the session
            if len(proxy) != 0:
                ss.proxies.update({'http': proxy, 'https': proxy})
            
            return ss
        elif lib == 'chrome':
            # Close any previous session
            if ss != None:
                ss.quit()
                
            opts = Options()
            opts.add_argument('--no-sandbox')
            opts.add_argument('--disable-gpu')
            opts.add_argument('--disable-software-rasterizer')
            opts.add_argument('--disable-notifications')
            opts.add_argument('--no-default-browser-check')
            opts.add_argument('--allow-running-insecure-content')
            opts.add_argument('--no-first-run')
    
            if test == 0:
                opts.add_argument('--headless') # No GUI
            
            # Set the default User-Agent for the session
            if len(agent) != 0:
                opts.add_argument('user-agent=' + agent)
            
            # Set the proxy to be used by the session
            if len(proxy) != 0:
                webdriver.DesiredCapabilities.CHROME['proxy'] = {
                    'httpProxy': proxy,
                    'ftpProxy': proxy,
                    'sslProxy': proxy,
                    'noProxy': None,
                    'proxyType': 'MANUAL',
                    'autodetect': False}
    
            return webdriver.Chrome(options = opts)
        else:
            return None

    def closeSession(self, lib, ss):
        if ss == None:
            return False

        if lib == 'socks' or lib == 'requests':
            ss.close()
            return True
        elif lib == 'chrome' or lib == 'firefox':
            ss.quit()
            return True
        else:
            return False

    def getnlog(self, ss, lnk, filename, name, log_id, *args, **kwargs):
        # Check if extra parameters were set
        headers = kwargs.get('headers', None)
        cookies = kwargs.get('cookies', None)
        tout = kwargs.get('timeout', 120)

        # Make the GET request depending on the lib selected
        if isinstance(ss, rq.sessions.Session):
            r = ss.get(lnk, headers = headers, cookies = cookies, 
                       timeout = tout)
            self.writeLog(filename, name, log_id, r.content, 'wb')

            return r # Return requests object          
        elif isinstance(ss, webdriver.chrome.webdriver.WebDriver) or\
            isinstance(ss, webdriver.firefox.webdriver.WebDriver):
            ss.set_page_load_timeout(tout)
            ss.get(lnk)
            src = ss.page_source
            self.writeLog(filename, name, log_id, src.encode(), 'wb')

            return src # Return page source
        else:
            return ''
     
    def postnlog(self, ss, lnk, filename, name, log_id, *args, **kwargs):
        # Check if extra parameters were set
        headers = kwargs.get('headers', None)
        cookies = kwargs.get('cookies', None)
        data = kwargs.get('data', None)
        json = kwargs.get('json', None)
        tout = kwargs.get('timeout', 120)

        # Make the POST request if 'ss' is a 'requests' object. There is
        # no POST method for selenium.
        if isinstance(ss, rq.sessions.Session):
            r = ss.post(lnk, headers = headers, cookies = cookies, 
                       data = data, json = json, timeout = tout)
            self.writeLog(filename, name, log_id, r.content, 'wb')
 
            return r # Return requests object
        else:
            return ''
    
