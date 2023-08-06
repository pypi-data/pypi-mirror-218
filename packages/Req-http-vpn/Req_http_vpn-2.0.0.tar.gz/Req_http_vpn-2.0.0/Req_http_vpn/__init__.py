#  ____                       _      _    _
# |  _ \   ___   __ _        | |__  | |_ | |_  _ __         __   __ _ __   _ __  
# | |_) | / _ \ / _` |       | '_ \ | __|| __|| '_ \        \ \ / /| '_ \ | '_ \ 
# |  _ < |  __/| (_| |       | | | || |_ | |_ | |_) |        \ V / | |_) || | | |
# |_| \_\ \___| \__, | _____ |_| |_| \__| \__|| .__/  _____   \_/  | .__/ |_| |_|
#                  |_||_____|                 |_|    |_____|       |_|

"""
Req_http_vpn Library
~~~~~~~~~~~~~~~~~~~~~

Req_http_vpn Library is an HTTP library, written in Python, for human beings.
Basic GET usage:

   >>> from Req_http_vpn import *
   >>> app = Requests_filter('Url')
   >>> data = app.filter_req_GET()[2]
   >>> print(data.status_code) # Print status_code
   
:Library used in the code: Requests
:Copyright: (c) 2023 Amin Rngbr.
:license: MIT
"""

import sys
sys.dont_write_bytecode = True

__version__ = ['1.0.0']

this : list = []

Req_Vpn_print = '0'

from typing import Any, overload
from requests import post, head, RequestException
import os
from ColorTER import *
from MusicBGX import *

class Requests_filter:
    """
    ## Requests_filter Class
    The Req_http_vpn library is a simple library for sending **http** requests to websites that are **filtered and blocked** by governments.
    ### How to create an object from this class:
    ```python
    from Req_http_vpn import *
    Req = Requests_filter('https://google.com')
    ```
    And this class has **three functions** >>>
    ```python
    filter_req_GET() #To send http request with GET method
    filter_req_POST() #To send http request with POST method
    filter_req_HEAD() #To send an http request to get website headers
    ```
    `The author and developer of this light and simple library:` َ**Amin Rngbr**
    **and over (:**
    
    **GitHub address**: [aminrngbr1122](https://github.com/aminrngbr1122)
    """
    
    def __init__(self, Url : str):
        self.url = Url
        global Req_Vpn_print
        if 'print_access_request_library_Req_http_vpn' not in os.environ:
            os.environ['print_access_request_library_Req_http_vpn'] = Req_Vpn_print
        if os.environ['print_access_request_library_Req_http_vpn'] == '0':
            Print.printY(f'You are using Req_http_vpn library :')
            Print.printM(f'\t version: {__version__[0]} (:')
            bgx = BackGround(paths=['ss.mp3'])
            bgx.play_background_music(Vol=50.0)
        
    # =======================================================================================
    
    @overload
    def filter_req_GET(
        self,
        Content_type : str = 'text/html',
        Headers : str  = '',
        Timeout : float = 500.5,
        Referer : str = 'https://google.com',
        UserAgent : str = 'Google Chrome',
        Stream : bool = False
        ) -> list[Any]: ...
    
    @overload
    def filter_req_POST(
        self,
        Data : str = 'login=...&pass=...',
        Content_type : str = 'text/html',
        Headers : str  = '',
        Timeout : float = 500.5,
        Referer : str = 'https://google.com',
        UserAgent : str = 'Google Chrome',
        Stream : bool = False
        ) -> list[Any]: ...
    
    @overload
    def filter_req_HEAD(
        self,
        Data : str = 'login=...&pass=...',
        Content_type : str = 'text/html',
        Timeout : float = 500.5,
        Headers : str  = '',
        Referer : str = 'https://google.com',
        UserAgent : str = 'Google Chrome',
        ) -> list[Any]: ...

    # =======================================================================================

    def filter_req_GET(
        self,
        Content_type : str = 'text/html',
        Headers : str  = '',
        Timeout : float = 500.5,
        Referer : str = 'https://google.com',
        UserAgent : str = 'Google Chrome',
        Stream : bool = False
        ) -> list[Any]:
        try:
            datas = {
                'UrlBox': f'{self.url}',
                'ContentTypeBox': f'{Content_type}',
                'ContentDataBox': '',
                'HeadersBox': f'{Headers}',
                'RefererBox': f'{Referer}',
                'AgentList': f'{UserAgent}',
                'VersionsList': 'HTTP/1.1',
                'MethodList': 'GET',
            }
            data = post('https://www.httpdebugger.com/Tools/ViewHttpHeaders.aspx', data=datas, timeout=Timeout, stream=Stream)
            return dict(
                headers= data.headers,
                content= data.content.decode('utf-8'),
                status_code= data.status_code
            )
        except Exception as e:
            return [e]
        
    def filter_req_POST(
        self,
        Data : str = 'login=...&pass=...',
        Content_type : str = 'text/html',
        Headers : str  = '',
        Timeout : float = 500.5,
        Referer : str = 'https://google.com',
        UserAgent : str = 'Google Chrome',
        Stream : bool = False
        ) -> list[Any]:
        try:
            datas = {
                'UrlBox': f'{self.url}',
                'ContentTypeBox': f'{Content_type}',
                'ContentDataBox': f'{Data}',
                'HeadersBox': f'{Headers}',
                'RefererBox': f'{Referer}',
                'AgentList': f'{UserAgent}',
                'VersionsList': 'HTTP/1.1',
                'MethodList': 'POST',
            }
            data = post('https://www.httpdebugger.com/Tools/ViewHttpHeaders.aspx', data=datas, timeout=Timeout, stream=Stream)
            return dict(
                headers= data.headers,
                content= data.content.decode('utf-8'),
                status_code= data.status_code
            )
        except Exception as e:
            return [e]

    def filter_req_HEAD(
        self,
        Data : str = 'login=...&pass=...',
        Content_type : str = 'text/html',
        Timeout : float = 500.5,
        Headers : str  = '',
        Referer : str = 'https://google.com',
        UserAgent : str = 'Google Chrome',
        ) -> list[Any]:
        try:
            datas = {
                'UrlBox': f'{self.url}',
                'ContentTypeBox': f'{Content_type}',
                'ContentDataBox': f'{Data}',
                'HeadersBox': f'{Headers}',
                'RefererBox': f'{Referer}',
                'AgentList': f'{UserAgent}',
                'VersionsList': 'HTTP/1.1',
                'MethodList': 'POST',
            }
            data = head('https://www.httpdebugger.com/Tools/ViewHttpHeaders.aspx', timeout=Timeout, data=datas)
            return dict(
                headers= data.headers,
                content= data.content.decode('utf-8'),
                status_code= data.status_code
            )
        except Exception as e:
            return [e]
        
    # =======================================================================================