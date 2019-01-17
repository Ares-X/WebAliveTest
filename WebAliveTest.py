import requests
import sys
import threading
import queue

list_name = sys.argv[1]
num = int(sys.argv[2])
webPort=['',':81',':82',':8080',':7001',':7002',':8089',':9090',':4848',':1352',':10000']
quit = queue.Queue()
threading_num = num

url_list = open(list_name,'r')
lines = url_list.readlines()
url_list.close()
for line in lines:
    line = line.rstrip()
    quit.put(line)

def crawler():
    while not quit.empty():
        rawUrl = quit.get()
        for port in webPort:
            url=rawUrl+port
            if 'http' not in url:
                url='http://'+url
            try:
                requests.packages.urllib3.disable_warnings()
                content = requests.get(url, verify=False, allow_redirects=True, timeout=5)
                if content.status_code == 200:
                    print (url)
            except requests.RequestException as e:
                try:
                    requests.packages.urllib3.disable_warnings()
                    url=url.replace('http','https')
                    content = requests.get(url, verify=False, allow_redirects=True, timeout=5)
                    if content.status_code == 200:
                        print (url)
                except:
                    pass

if __name__ == '__main__':
    for i in range(threading_num):
        t = threading.Thread(target=crawler)
        t.start()